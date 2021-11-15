class PyArdError(Exception):
    """
    Base Class for All py-ard Errors
    """
    pass


class InvalidAlleleError(PyArdError):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return f"Invalid Allele: {self.message}"


class InvalidMACError(PyArdError):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return f"Invalid MAC Code: {self.message}"


class InvalidTypingError(PyArdError):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return f"Invalid HLA Typing: {self.message}"
