"""Consumer contract ported from ML-Stock-Analysis aea0b510babae2b7de891e5fb5e67e0ec39e4f52.

Required wire fields have no defaults. Source membership needs a backend audit;
the client can validate only the emitted envelope and its internal consistency.
"""
from datetime import date
from typing import Annotated, Literal

from pydantic import (
    AfterValidator, BaseModel, BeforeValidator, ConfigDict, Field,
    StrictFloat, StrictInt, field_validator, model_validator,
)

ForecastType = Literal["5dd", "10dd"]
Ticker = Annotated[str, Field(pattern=r"^[A-Za-z]{4}$")]


def iso_date(value: str) -> str:
    date.fromisoformat(value)
    return value


def integer_constant(value):
    if type(value) is not int:
        raise ValueError("Contract integer constants must be JSON integers")
    return value


ISODate = Annotated[str, Field(pattern=r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"), AfterValidator(iso_date)]
Count = Annotated[int, Field(strict=True, ge=0)]
Number = StrictInt | Annotated[StrictFloat, Field(allow_inf_nan=False)] | None
Series = Annotated[list[Number], Field(min_length=3, max_length=3)]


def metadata_sources(forecast_type: ForecastType) -> list[tuple[str, str]]:
    windows = ("5dd",) if forecast_type == "5dd" else ("5dd", "10dd")
    return [(label, window) for window in windows for label in ("medianLoss", "medianGain")]


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class FeatureSource(ContractModel):
    label_type: Literal["medianLoss", "medianGain"]
    window: ForecastType


class FeatureFilter(ContractModel):
    source: Literal["model_metadata"]
    key: Literal["selected_features"]
    strategy: Literal["union"]
    model_version: Annotated[Literal[1], BeforeValidator(integer_constant)]
    sources: list[FeatureSource]
    selected_union_count: Count
    included_count: Annotated[int, Field(ge=1)]
    selected_unavailable_count: Count
    excluded_not_selected_count: Count

    @model_validator(mode="after")
    def validate_counts(self):
        if self.selected_union_count != self.included_count + self.selected_unavailable_count:
            raise ValueError("Selected union counts disagree")
        return self


class TechnicalQuality(ContractModel):
    request_date: ISODate
    data_age_calendar_days: Annotated[int, Field(ge=1)]
    freshness_status: Literal["unverified_without_exchange_calendar"]
    null_counts_by_session: Annotated[list[Count], Field(min_length=3, max_length=3)]


class TechnicalResponse(ContractModel):
    schema_version: Literal["2.0"]
    ticker: Ticker
    forecast_type: ForecastType
    market_timezone: Literal["Asia/Jakarta"]
    selection_policy: Literal["latest_available_before_request_date"]
    requested_sessions: Annotated[Literal[3], BeforeValidator(integer_constant)]
    returned_sessions: Annotated[Literal[3], BeforeValidator(integer_constant)]
    dates: Annotated[list[ISODate], Field(min_length=3, max_length=3)]
    order: Literal["oldest_to_newest"]
    data_as_of: ISODate
    quality: TechnicalQuality
    feature_filter: FeatureFilter
    feature_catalog_version: Literal["1.0"]
    indicators: dict[str, Series]

    @field_validator("indicators")
    @classmethod
    def validate_names(cls, value):
        if not value or any(not name or name != name.strip() or name == "Date" for name in value):
            raise ValueError("Indicator names must be nonempty exact feature names")
        return value

    @model_validator(mode="after")
    def validate_alignment(self):
        parsed = [date.fromisoformat(day) for day in self.dates]
        if any(left >= right for left, right in zip(parsed, parsed[1:])):
            raise ValueError("Dates must be unique and strictly increasing")
        if self.data_as_of != self.dates[-1]:
            raise ValueError("As-of must agree with the latest date")
        age = (date.fromisoformat(self.quality.request_date) - parsed[-1]).days
        if age < 1 or age != self.quality.data_age_calendar_days:
            raise ValueError("Age/cutoff must agree with server request date")
        if self.feature_filter.included_count != len(self.indicators):
            raise ValueError("Included count must agree with indicators")
        sources = [(source.label_type, source.window) for source in self.feature_filter.sources]
        if sources != metadata_sources(self.forecast_type):
            raise ValueError("Metadata sources must agree with forecast type")
        counts = [sum(values[i] is None for values in self.indicators.values()) for i in range(3)]
        if counts != self.quality.null_counts_by_session:
            raise ValueError("Null counts must agree with observations")
        return self


class TechnicalErrorDetail(ContractModel):
    code: str
    message: str
    ticker: Ticker
    forecast_type: ForecastType


class TechnicalErrorResponse(ContractModel):
    detail: TechnicalErrorDetail
