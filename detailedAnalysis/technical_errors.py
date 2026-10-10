"""Failures that must stop technical analysis before Codex starts."""


class TechnicalIntegrationError(RuntimeError):
    category = "integration"

    def __init__(self, message: str, *, status_code: int | None = None,
                 reason_code: str | None = None, ticker: str | None = None,
                 forecast_type: str | None = None, validation_details=None):
        self.status_code = status_code
        self.reason_code = reason_code
        self.ticker = ticker
        self.forecast_type = forecast_type
        self.validation_details = validation_details
        context = f"{ticker}/{forecast_type}: " if ticker else ""
        status = f" (HTTP {status_code})" if status_code is not None else ""
        code = f" [{reason_code}]" if reason_code else ""
        super().__init__(f"{context}{self.category}{code}{status}: {message}")


class TechnicalInputError(TechnicalIntegrationError):
    category = "input"


class TechnicalTransportError(TechnicalIntegrationError):
    category = "transport"


class TechnicalAPIError(TechnicalIntegrationError):
    category = "api"


class TechnicalServiceError(TechnicalIntegrationError):
    category = "service"


class TechnicalContractError(TechnicalIntegrationError):
    category = "contract"


class TechnicalFreshnessError(TechnicalIntegrationError):
    category = "freshness"
