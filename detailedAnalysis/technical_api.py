"""Single technical retrieval path; no retries or response cache."""
import logging
import math
import os
import re
import time
from dataclasses import dataclass

import httpx
from pydantic import ValidationError

from detailedAnalysis.helper import build_technical_url, normalize_technical_ticker
from detailedAnalysis.technical_contract import TechnicalErrorResponse, TechnicalResponse
from detailedAnalysis.technical_errors import (
    TechnicalAPIError, TechnicalContractError, TechnicalFreshnessError,
    TechnicalInputError, TechnicalServiceError, TechnicalTransportError,
    TechnicalIntegrationError,
)
from detailedAnalysis.technical_json import load_json

logger = logging.getLogger(__name__)
DOMAIN_STATUS = {
    "technical_data_missing": 404,
    "no_eligible_sessions": 404,
    "ohlcv_data_missing": 409,
    "insufficient_sessions": 409,
    "feature_filter_unavailable": 409,
    "no_eligible_indicators": 409,
    "invalid_technical_data": 500,
    "invalid_model_metadata": 500,
    "internal_error": 500,
}


@dataclass(frozen=True)
class TechnicalConfig:
    timeout_seconds: float = 30.0
    max_data_age_calendar_days: int | None = None

    def __post_init__(self):
        if (type(self.timeout_seconds) not in (int, float)
                or not math.isfinite(self.timeout_seconds) or self.timeout_seconds <= 0):
            raise TechnicalInputError("Technical API timeout must be positive and finite")
        age = self.max_data_age_calendar_days
        if age is not None and (type(age) is not int or age < 1):
            raise TechnicalInputError("Technical maximum data age must be a positive integer")

    @classmethod
    def from_environment(cls, timeout: float = 30.0):
        raw_timeout = os.environ.get("TECHNICAL_API_TIMEOUT_SECONDS")
        raw_age = os.environ.get("TECHNICAL_MAX_DATA_AGE_CALENDAR_DAYS")
        try:
            configured_timeout = float(raw_timeout) if raw_timeout is not None else timeout
            if raw_age is not None and not re.fullmatch(r"[0-9]+", raw_age):
                raise ValueError("Invalid age")
            age = int(raw_age) if raw_age is not None else None
        except ValueError as exc:
            raise TechnicalInputError("Invalid technical timeout or maximum-age configuration") from exc
        return cls(configured_timeout, age)


class TechnicalAPIClient:
    def __init__(self, base_url: str,
                 config: TechnicalConfig | None = None, *, client: httpx.Client | None = None):
        self.base_url = base_url
        self.config = config if config is not None else TechnicalConfig()
        self.client = client

    def retrieve(self, ticker: str, forecast_type: str) -> TechnicalResponse:
        started = time.perf_counter()
        try:
            result = self._retrieve(ticker, forecast_type)
        except TechnicalIntegrationError as exc:
            # Only validated identities and recognized codes enter diagnostics.
            logger.warning("technical_failure ticker=%s horizon=%s category=%s status=%s code=%s latency_ms=%.1f",
                           exc.ticker, exc.forecast_type, exc.category, exc.status_code,
                           exc.reason_code, (time.perf_counter() - started) * 1000)
            raise
        logger.info("technical_latency ticker=%s horizon=%s latency_ms=%.1f",
                    result.ticker, result.forecast_type,
                    (time.perf_counter() - started) * 1000)
        return result

    def _retrieve(self, ticker: str, forecast_type: str) -> TechnicalResponse:
        try:
            ticker = normalize_technical_ticker(ticker)
            url = build_technical_url(self.base_url, ticker, forecast_type)
        except ValueError as exc:
            raise TechnicalInputError("Invalid technical ticker, forecast type, or base URL") from exc
        context = {"ticker": ticker, "forecast_type": forecast_type}
        try:
            if self.client is not None:
                response = self.client.get(url, timeout=self.config.timeout_seconds,
                                           headers={"Accept": "application/json"})
            else:
                with httpx.Client(follow_redirects=False) as client:
                    response = client.get(url, timeout=self.config.timeout_seconds,
                                          headers={"Accept": "application/json"})
        except httpx.RequestError as exc:
            raise TechnicalTransportError("Technical service request failed", **context) from exc
        if response.status_code != 200:
            self._raise_http_failure(response, context)
        try:
            envelope = TechnicalResponse.model_validate(load_json(response.content))
        except (ValueError, ValidationError) as exc:
            raise TechnicalContractError("Invalid technical schema 2.1 response", **context) from exc
        if envelope.ticker != ticker or envelope.forecast_type != forecast_type:
            raise TechnicalContractError("Response identity does not match request", **context)
        age = envelope.quality.data_age_calendar_days
        budget = self.config.max_data_age_calendar_days
        if budget is not None and age > budget:
            raise TechnicalFreshnessError(
                f"Calendar age {age} exceeds configured budget {budget}", **context)
        logger.info(
            "technical_retrieval ticker=%s horizon=%s as_of=%s age=%s included=%s "
            "unavailable=%s null_counts=%s ohlcv_null_counts=%s bytes=%s",
            ticker, forecast_type, envelope.data_as_of, age,
            envelope.feature_filter.included_count,
            envelope.feature_filter.selected_unavailable_count,
            envelope.quality.null_counts_by_session,
            envelope.quality.ohlcv_null_counts_by_session, len(response.content),
        )
        return envelope

    @staticmethod
    def _raise_http_failure(response: httpx.Response, context: dict):
        status = response.status_code
        try:
            body = load_json(response.content)
        except ValueError as exc:
            raise TechnicalServiceError("Unrecognized service error body", status_code=status, **context) from exc
        if status == 422 and isinstance(body, dict) and isinstance(body.get("detail"), list):
            # Keep diagnostics separate; never put raw input/body into user-facing logs.
            diagnostics = [
                {key: item[key] for key in ("type", "loc", "msg") if key in item}
                for item in body["detail"] if isinstance(item, dict)
            ]
            raise TechnicalInputError("Service rejected request inputs", status_code=status,
                                      validation_details=diagnostics, **context)
        try:
            detail = TechnicalErrorResponse.model_validate(body).detail
        except ValidationError as exc:
            raise TechnicalServiceError("Unrecognized service error shape", status_code=status, **context) from exc
        if (detail.ticker != context["ticker"] or detail.forecast_type != context["forecast_type"]
                or DOMAIN_STATUS.get(detail.code) != status):
            raise TechnicalServiceError("Unrecognized service status/code or identity", status_code=status, **context)
        # Codes are recognized locally. Server messages are retained in the typed
        # HTTP body only, never interpolated as trusted instructions or log text.
        raise TechnicalAPIError("Technical data retrieval failed", status_code=status,
                                reason_code=detail.code, **context)
