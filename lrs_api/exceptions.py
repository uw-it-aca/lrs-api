class InvalidXAPIException(Exception):
    """Generic exception for errors in processing statement JSON"""
    pass


class StatementExistsException(InvalidXAPIException):
    """Raised when a statement comes in with an ID,
       but that ID already exists"""
    pass


class InvalidXAPIJsonException(InvalidXAPIException):
    """Raised when the statement can't be parsed as JSON"""
    pass


class MissingXAPIFieldException(InvalidXAPIException):
    """Raised if a required field in the statement is missing (like verb)"""
    pass


class MissingXAPIAttributeException(InvalidXAPIException):
    """Raised if a field is missing a required attribute (like id on verb)"""
    pass
