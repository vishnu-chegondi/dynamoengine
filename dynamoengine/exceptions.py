class BaseException(Exception):

    def __init__(self, message):
        self.message = message
        self.return_dict = dict(message=self.message)

    def __str__(self):
        return str(self.return_dict)


class DynamoValueError(BaseException):

    def __init__(self, message="", solution=""):
        super().__init__(message)
        self.solution = solution
        self.return_dict.update({"solution": self.solution})
