# tests/conftest.py
import pytest
import tempfile
import os
from contact.contact import Contact
from repositories.contact_repository import ContactRepository
from storage.json_storage import JsonStorage


@pytest.fixture
def temp_json_file():
    """Create a temporary JSON file"""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def clean_storage(temp_json_file) -> JsonStorage:
    """Create clean storage"""
    return JsonStorage(temp_json_file)


@pytest.fixture
def clean_repository(clean_storage) -> ContactRepository:
    """Create clean repository"""
    return ContactRepository(clean_storage)


@pytest.fixture
def sample_contacts() -> list[Contact]:
    """Create list of sample contacts"""
    return [
        Contact("Alice", "1111111111", "alice@test.com"),
        Contact("Bob", "2222222222", "bob@test.com"),
        Contact("Charlie", "3333333333"),
    ]


@pytest.fixture
def populated_repository(
    clean_repository: ContactRepository, sample_contacts
) -> ContactRepository:
    """Create repository with sample contacts"""
    for contact in sample_contacts:
        clean_repository.add(contact)
    return clean_repository
