"""Custom exceptions."""


class StudentSystemError(Exception):
    """Base exception for the whole project."""


class ValidationError(StudentSystemError):
    """Domain validation failed."""


class DuplicateError(StudentSystemError):
    """Student already exists."""


class NotFoundError(StudentSystemError):
    """Student not found."""


class ExternalServiceError(StudentSystemError):
    """External dependency failed."""