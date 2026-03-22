import pytest
import os
import tempfile
from contact.contact import Contact
from repositories.contact_repository import ContactRepository
from storage.json_storage import JsonStorage
from utils.exceptions import ContactAlreadyExistsError, ContactNotFoundError


class TestContactRepository:
    """Test suite for ContactRepository"""

    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage for testing"""
        # Create temp file
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)

        storage = JsonStorage(path)
        yield storage

        # Cleanup
        if os.path.exists(path):
            os.remove(path)

    @pytest.fixture
    def repository(self, temp_storage) -> ContactRepository:
        """Create repository with temp storage"""
        return ContactRepository(temp_storage)

    @pytest.fixture
    def sample_contact(self) -> Contact:
        """Create a sample contact"""
        return Contact("John Doe", "1234567890", "john@test.com")

    def test_repository_starts_empty(self, repository: ContactRepository) -> None:
        """Test that new repository is empty"""
        assert len(repository) == 0
        assert repository.get_all() == []

    def test_add_contact(self, repository: ContactRepository, sample_contact) -> None:
        """Test adding a contact"""
        repository.add(sample_contact)

        assert len(repository) == 1
        assert sample_contact in repository

    def test_add_duplicate_contact_raises_error(
        self, repository: ContactRepository, sample_contact
    ) -> None:
        """Test adding duplicate contact raises error"""
        repository.add(sample_contact)

        with pytest.raises(ContactAlreadyExistsError):
            repository.add(sample_contact)

    def test_delete_contact(
        self, repository: ContactRepository, sample_contact
    ) -> None:
        """Test deleting a contact"""
        repository.add(sample_contact)
        repository.delete(sample_contact)

        assert len(repository) == 0
        assert sample_contact not in repository

    def test_delete_nonexistent_contact_raises_error(
        self, repository: ContactRepository, sample_contact
    ) -> None:
        """Test deleting non-existent contact raises error"""
        with pytest.raises(ContactNotFoundError):
            repository.delete(sample_contact)

    def test_search_by_phone_found(
        self, repository: ContactRepository, sample_contact
    ) -> None:
        """Test searching by phone when contact exists"""
        repository.add(sample_contact)

        found = repository.search_by_phone("1234567890")

        assert found is not None
        assert found.name == "John Doe"

    def test_search_by_phone_not_found(self, repository: ContactRepository) -> None:
        """Test searching by phone when contact doesn't exist"""
        found = repository.search_by_phone("9999999999")
        assert found is None

    def test_search_by_name_found(
        self, repository: ContactRepository, sample_contact
    ) -> None:
        """Test searching by name when contact exists"""
        repository.add(sample_contact)

        found = repository.search_by_name("John Doe")

        assert found is not None
        assert found.phone_num == "1234567890"

    def test_search_by_name_case_insensitive(
        self, repository: ContactRepository, sample_contact
    ) -> None:
        """Test search is case-insensitive"""
        repository.add(sample_contact)

        found = repository.search_by_name("john doe")  # lowercase

        assert found is not None

    def test_update_changes_name_and_email(self, repository: ContactRepository) -> None:
        """Test updating name and email (same phone)"""
        old = Contact("John", "1234567890", "old@test.com")
        new = Contact("John Doe", "1234567890", "new@test.com")

        repository.add(old)
        repository.update(old, new)

        # Verify update
        found = repository.search_by_phone("1234567890")
        if found is not None:
            assert found.name == "John Doe"
            assert found.email == "new@test.com"

        # Both old and new are "equal" (same phone)
        assert old == new
        assert old in repository  # True because old == new and new is in repo

    def test_update_nonexistent_contact_raises_error(
        self, repository: ContactRepository
    ) -> None:
        """Test updating non-existent contact raises error"""
        old = Contact("John", "1234567890")
        new = Contact("John Doe", "1234567890", "new@test.com")

        # Don't add old contact
        with pytest.raises(ContactNotFoundError):
            repository.update(old, new)

    def test_update_with_recreated_old_contact(
        self, repository: ContactRepository
    ) -> None:
        """Test update works with recreated old_contact object"""
        # Add original
        original = Contact("John", "1234567890", "original@test.com")
        repository.add(original)

        # Create NEW objects (simulates real-world usage)
        old = Contact(
            "John", "1234567890", "different@test.com"
        )  # Email doesn't matter
        new = Contact("John Doe", "1234567890", "new@test.com")

        # Should work because phone is the identifier
        repository.update(old, new)

        # Verify
        found = repository.search_by_phone("1234567890")
        if found is not None:
            assert found.name == "John Doe"
            assert found.email == "new@test.com"

    def test_get_all_sorted(self, repository: ContactRepository) -> None:
        """Test get_all returns sorted contacts"""
        contact1 = Contact("Zoe", "1111111111")
        contact2 = Contact("Alice", "2222222222")
        contact3 = Contact("Mike", "3333333333")

        repository.add(contact1)
        repository.add(contact2)
        repository.add(contact3)

        contacts = repository.get_all()

        assert len(contacts) == 3
        assert contacts[0].name == "Alice"
        assert contacts[1].name == "Mike"
        assert contacts[2].name == "Zoe"

    def test_persistence(self, temp_storage) -> None:
        """Test that contacts persist across repository instances"""
        # Create repository and add contact
        repo1 = ContactRepository(temp_storage)
        contact = Contact("John", "1234567890")
        repo1.add(contact)

        # Create new repository instance with same storage
        repo2 = ContactRepository(temp_storage)

        # Contact should still be there
        assert len(repo2) == 1
        found = repo2.search_by_phone("1234567890")
        assert found is not None
        assert found.name == "John"
