class ApiError(Exception):
    """Base exception for errors when working with the MiHoMo API."""

    def __init__(self, code: int, message: str, status: int = 400) -> None:
        """Initialize the error with a code and message."""
        super().__init__(f"[{code}] {message} Status: {status}")
        self.code = code
        self.message = message
        self.status = status

class StarRailCardError(ApiError):
    """Exception specific to MiHoMo errors."""
    pass