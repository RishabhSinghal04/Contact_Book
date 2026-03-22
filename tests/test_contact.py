import pytest

from contact.contact import Contact


class TestContact:
    def test_create_contact_with_all_fields(self) -> None:
        name = "John Doe"
        phone_num = "1234567890"
        email = "john@test.com"
        contact = Contact(name, phone_num, email)

        assert contact.name == name
        assert contact.phone_num == phone_num
        assert contact.email == email

    def test_create_contact_without_email(self) -> None:
        name = "Jane Doe"
        phone_num = "9876543210"
        contact = Contact(name, phone_num)

        assert contact.name == name
        assert contact.phone_num == phone_num
        assert contact.email is None

    def test_contact_equality_same_phone(self) -> None:
        contact1 = Contact("John", "1234567890", "john@test.com")
        contact2 = Contact("John", "1234567890", "john2@test.com")

        assert contact1 == contact2

    def test_contact_equality_different_phone(self) -> None:
        contact1 = Contact("John", "1234567890")
        contact2 = Contact("John", "9999999999")

        assert contact1 != contact2

    def test_contact_hash_consistency(self) -> None:
        contact1 = Contact("John", "1234567890")
        contact2 = Contact("John", "9999999999")
        contact3 = Contact("John", "1234567890")  # Duplicate of contact1

        contacts = {contact1, contact2, contact3}
        assert len(contacts) == 2  # Only 2 unique contacts

    def test_contact_str_with_email(self) -> None:
        contact = Contact("John Doe", "1234567890", "john@test.com")
        assert str(contact) == "John Doe: 1234567890 | john@test.com"

    def test_contact_str_without_email(self) -> None:
        contact = Contact("John Doe", "1234567890")
        assert str(contact) == "John Doe: 1234567890"

    def test_contact_repr(self) -> None:
        """Test repr representation"""
        contact = Contact("John", "1234567890", "john@test.com")

        expected = "Contact(name='John', phone_num='1234567890', email='john@test.com')"
        print(repr(contact))
        print(expected)
        assert repr(contact) == expected
