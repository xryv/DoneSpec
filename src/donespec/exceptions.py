class DoneSpecError(Exception):
    """Base DoneSpec exception."""


class SpecValidationError(DoneSpecError):
    """Raised when done.json is invalid."""
