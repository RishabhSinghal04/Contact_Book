from typing import Optional, Iterator

from core.interfaces import IStorageBackend

from contact.contact import Contact
from contact.contact_serializer import ContactSerializer
from contact.contact_validator import ContactValidator

from storage.json_storage import JsonStorage

from utils.exceptions import ContactNotFoundError, ContactAlreadyExistsError
from utils.decorators import log_execution, handle_exception
from utils.logger import get_logger

logger = get_logger(__name__)


class ContactRepository:
    """
    Manages contacts with CRUD(Create, Read, Update and Delete) operations.
    Uses Set for O(1) lookups and Storage for persistence.
    """

    def __init__(self, storage: Optional[IStorageBackend] = None) -> None:
        """
        Initialize contact book.

        Args:
            storage: Optional storage handler. If None, defaults to a JsonStorage instance.

        Raises:
            StorageError: If the storage file or directory cannot be created.
        """
        self._contacts: set[Contact] = set()
        self._storage = storage or JsonStorage()
        self._load_contacts()

    @log_execution
    @handle_exception
    def add(self, contact: Contact) -> None:
        """
        Add a new contact.

        Args:
            contact: Contact to add

        Raises:
            ContactAlreadyExistsError: If a contact with the same name or phone number already exists.
            ValidationError: If the contact fails validation checks.
        """
        self._validate_contact(contact)
        if contact in self._contacts:
            logger.warning(
                f"Attempted to add duplicate contact with same phone number: "
                f"name='{contact.name}' phone_num='{contact.phone_num}'"
            )
            raise ContactAlreadyExistsError(
                f"Contact with {contact.phone_num} already exists"
            )
        self._contacts.add(contact)
        self.save_all()
        logger.info(f"Added contact: {str(contact)}")

    @log_execution
    @handle_exception
    def delete(self, contact: Contact) -> None:
        """
        Delete a contact.

        Args:
            contact: Contact to delete

        Raises:
            ContactNotFoundError: If contact doesn't exist in the repository.
        """
        if contact not in self._contacts:
            logger.warning(
                f"Attempted to delete non-existant contact: "
                f"name='{contact.name}' phone_num='{contact.phone_num}'"
            )
            raise ContactNotFoundError(
                f"Contact with {contact.name} or {contact.phone_num} does not exists"
            )
        self._contacts.discard(contact)
        self.save_all()
        logger.info(f"Deleted contact: {str(contact)}")

    @log_execution
    def search_by_phone(self, phone_num: str) -> Optional[Contact]:
        """
        Find a contact by phone number.

        Args:
            phone_num (str): The phone number to search for.

        Returns:
            Optional[Contact]: The matching contact if found, otherwise None.

        Raises:
            ValidationError: If the phone number format is invalid.
        """
        cleaned = ContactValidator.validate_phone_num(phone_num)
        for contact in self._contacts:
            if contact.phone_num == cleaned:
                logger.debug(f"Contact found: {contact}")
                return contact
        logger.debug(f"Contact not found with phone_num='{phone_num}'")
        return None

    @log_execution
    def search_by_name(self, name: str) -> Optional[Contact]:
        """
        Find a contact by name (case-insensitive).

        Args:
            name (str): The name to search for.

        Returns:
            Optional[Contact]: The matching contact if found, otherwise None.
        """
        target = name.lower()
        for contact in self._contacts:
            if contact.name.lower() == target:
                logger.debug(f"Contact found: {contact}")
                return contact

        logger.debug(f"Contact not found with name='{name}'")
        return None

    @log_execution
    @handle_exception
    def update(self, old_contact: Contact, new_contact: Contact) -> None:
        """
        Update a contact (replace old with new).

        Args:
            old_contact: Existing contact
            new_contact: Updated contact

        Raises:
            ContactNotFoundError: If old contact doesn't exist in the repository.
        """
        if old_contact not in self._contacts:
            logger.warning(f"Attempted to update non-existent contact")
            raise ContactNotFoundError("Contact not found")

        self._contacts.discard(old_contact)
        self._contacts.add(new_contact)
        self.save_all()
        logger.info(f"Updated contact: {str(new_contact)}")

    def get_all(self) -> list[Contact]:
        """
        Retrieve all contacts sorted alphabetically by name.

        Returns:
            list[Contact]: Sorted list of all contacts.
        """
        return sorted(self._contacts, key=lambda c: c.name)

    @log_execution
    @handle_exception
    def save_all(self) -> None:
        """
        Persist all contacts to the storage backend.

        Raises:
            StorageError: If writing to storage fails.
        """
        data = [ContactSerializer.to_dict(contact) for contact in self._contacts]
        self._storage.write(data)
        logger.info(f"Saved {len(self._contacts)} contacts")

    @log_execution
    def _load_contacts(self) -> None:
        """
        Load contacts from the storage backend during initialization.

        Notes:
            - If loading fails, initializes with an empty set.
        """
        try:
            data = self._storage.read()
            self._contacts = {ContactSerializer.from_dict(item) for item in data}
            logger.info(f"Loaded {len(self._contacts)} contacts from storage")
        except Exception as e:
            logger.warning(f"Could not load contacts: {e}")
            # Start with empty set if load fails
            self._contacts = set()

    @log_execution
    @handle_exception
    def _validate_contact(self, contact) -> None:
        """
        Ensure the provided object is a valid Contact instance.

        Args:
            contact (Contact): The contact to validate.

        Raises:
            TypeError: If the object is not a Contact.
        """
        if not isinstance(contact, Contact):
            logger.warning(f"Invalid type: {type(contact).__name__}")
            raise TypeError("Expected Contact object")

    def __iter__(self) -> Iterator[Contact]:
        return iter(sorted(self._contacts, key=lambda c: c.name))

    def __len__(self) -> int:
        """Get total number of contacts."""
        return len(self._contacts)

    def __contains__(self, contact: Contact) -> bool:
        return isinstance(contact, Contact) and contact in self._contacts

    def __str__(self) -> str:
        """String representation."""
        return f"Contact Book: ({len(self._contacts)} contacts)"

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"ContactBook(contacts={len(self._contacts)})"
