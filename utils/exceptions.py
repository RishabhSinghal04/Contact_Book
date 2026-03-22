class ContactRepositoryError(Exception):
    """Base exception for Contact Book."""

    pass


class ContactNotFoundError(ContactRepositoryError):
    """Raised when contact is not found."""

    pass


class ContactAlreadyExistsError(ContactRepositoryError):
    """Raised when trying to add duplicate contact."""

    pass


class ValidationError(ContactRepositoryError):
    """Raised when validation fails."""

    pass


class StorageError(ContactRepositoryError):
    """Raised when file operations fail."""

    pass
