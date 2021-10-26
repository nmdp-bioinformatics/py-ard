class PyArdError(Exception):
    """
    Base Class for All py-ard Errors
    """
    pass


class InvalidAlleleError(PyArdError):
    def __init__(self, message: str) -> None:
        self.message = message


class InvalidMACError(PyArdError):
    def __init__(self, message: str) -> None:
        self.message = message


class InvalidTypingError(PyArdError):
    def __init__(self, message: str) -> None:
        self.message = message
