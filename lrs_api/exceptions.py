class InvalidStatementException(Exception):
    """Generic exception for errors in processing statements"""
    pass


class InvalidStatementJsonException(InvalidStatementException):
    """Raised when the statement can't be parsed as JSON"""
    pass


class InvalidStatementDateTimeException(InvalidStatementException):
    """Raised if we're unable to parse a datetime in the statement"""
    pass


class InvalidContextException(InvalidStatementException):
    """JSON that looks like Caliper, but the @context isn't right"""
    pass


class InvalidCaliperException(InvalidStatementException):
    """Generic exception for errors in processing Caliper statements"""
    pass


class MissingCaliperFieldException(InvalidCaliperException):
    """ Raised when a required field in the statement is missing"""
    pass


class InvalidXAPIException(InvalidStatementException):
    """Generic exception for errors in processing XAPI statements"""
    pass


class StatementExistsException(InvalidXAPIException):
    """Raised when a statement comes in with an ID,
       but that ID already exists"""
    pass


class MissingXAPIFieldException(InvalidXAPIException):
    """Raised if a required field in the statement is missing (like verb)"""
    pass


class MissingXAPIAttributeException(InvalidXAPIException):
    """Raised if a field is missing a required attribute (like id on verb)"""
    pass
