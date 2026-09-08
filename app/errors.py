from app.models.quota import QuotaStatus


class InvalidChatMessageError(ValueError):
    """Raised when a chat message violates service-level validation."""


class QuotaExceededError(RuntimeError):
    """Raised when the Organizer denies a chat request."""

    def __init__(self, quota: QuotaStatus) -> None:
        super().__init__("Chat quota is exhausted")
        self.quota = quota


class OrganizerAuthorizationError(RuntimeError):
    """Raised when the Organizer rejects the caller's bearer token."""

    def __init__(self, status_code: int) -> None:
        super().__init__("Organizer rejected the authorization token")
        self.status_code = status_code


class QuotaServiceUnavailableError(RuntimeError):
    """Raised when quota state cannot be checked or consumed safely."""


class QuotaConsumptionRejectedError(RuntimeError):
    """Raised when an atomic consume loses a concurrent quota race."""


class CodexExecutionError(RuntimeError):
    """Raised when Codex cannot produce a valid final response."""


class CodexTimeoutError(CodexExecutionError):
    """Raised when Codex exceeds the configured execution timeout."""
