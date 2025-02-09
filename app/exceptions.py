class InvalidGroupException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class LemmatizationError(Exception):
    pass