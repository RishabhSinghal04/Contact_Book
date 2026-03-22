import pytest
from contact.contact_validator import ContactValidator
from utils.exceptions import ValidationError


class TestContactValidator:

    @pytest.fixture
    def validator(self) -> ContactValidator:
        """Fixture to create validator instance"""
        return ContactValidator()

    # Name validation tests
    def test_validate_name_valid(self, validator: ContactValidator) -> None:
        """Test valid name passes validation"""
        result = validator.validate_name("John Doe")
        assert result == "John Doe"

    def test_validate_name_strips_whitespace(self, validator: ContactValidator) -> None:
        """Test that name whitespace is stripped"""
        result = validator.validate_name("  John Doe  ")
        assert result == "John Doe"

    def test_validate_name_empty_raises_error(
        self, validator: ContactValidator
    ) -> None:
        """Test that empty name raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_name("")

        assert "Name cannot be empty" in str(exc_info.value)

    def test_validate_name_whitespace_only_raises_error(
        self, validator: ContactValidator
    ) -> None:
        """Test that whitespace-only name raises ValidationError"""
        with pytest.raises(ValidationError):
            validator.validate_name("   ")

    def test_validate_name_too_long_raises_error(
        self, validator: ContactValidator
    ) -> None:
        """Test that too-long name raises ValidationError"""
        long_name = "A" * 30  # Exceeds max length

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_name(long_name)

        assert "too long" in str(exc_info.value).lower()

    # Phone validation tests
    def test_validate_phone_valid_digits(self, validator: ContactValidator) -> None:
        """Test valid phone number with only digits"""
        result = validator.validate_phone_num("1234567890")
        assert result == "1234567890"

    def test_validate_phone_with_dashes(self, validator: ContactValidator) -> None:
        """Test phone number with dashes is cleaned"""
        result = validator.validate_phone_num("123-456-7890")
        assert result == "1234567890"

    def test_validate_phone_with_spaces(self, validator: ContactValidator) -> None:
        """Test phone number with spaces is cleaned"""
        result = validator.validate_phone_num("123 456 7890")
        assert result == "1234567890"

    def test_validate_phone_with_parentheses(self, validator: ContactValidator) -> None:
        """Test phone number with parentheses is cleaned"""
        result = validator.validate_phone_num("(123) 456-7890")
        assert result == "1234567890"

    def test_validate_phone_with_letters_raises_error(
        self, validator: ContactValidator
    ) -> None:
        """Test phone with letters raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_phone_num("123abc7890")

        assert "only digits" in str(exc_info.value).lower()

    def test_validate_phone_too_short_raises_error(
        self, validator: ContactValidator
    ) -> None:
        """Test too-short phone raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_phone_num("123")

        assert "must be" in str(exc_info.value).lower()

    def test_validate_phone_too_long_raises_error(
        self, validator: ContactValidator
    ) -> None:
        """Test too-long phone raises ValidationError"""
        long_phone = "1" * 25  # Exceeds max

        with pytest.raises(ValidationError):
            validator.validate_phone_num(long_phone)

    # Email validation tests
    def test_validate_email_valid(self, validator: ContactValidator) -> None:
        """Test valid email passes"""
        result = validator.validate_email("test@example.com")
        assert result == "test@example.com"

    def test_validate_email_strips_whitespace(
        self, validator: ContactValidator
    ) -> None:
        """Test email whitespace is stripped"""
        result = validator.validate_email("  test@example.com  ")
        assert result == "test@example.com"

    def test_validate_email_no_at_raises_error(
        self, validator: ContactValidator
    ) -> None:
        """Test email without @ raises error"""
        with pytest.raises(ValidationError):
            validator.validate_email("test.example.com")

    def test_validate_email_no_domain_raises_error(
        self, validator: ContactValidator
    ) -> None:
        """Test email without domain raises error"""
        with pytest.raises(ValidationError):
            validator.validate_email("test@")

    def test_validate_email_no_dot_raises_error(
        self, validator: ContactValidator
    ) -> None:
        """Test email without dot in domain raises error"""
        with pytest.raises(ValidationError):
            validator.validate_email("test@example")

    # Parametrized tests (multiple inputs)
    @pytest.mark.parametrize(
        "phone,expected",
        [
            ("1234567890", "1234567890"),
            ("123-456-7890", "1234567890"),
            ("(123) 456-7890", "1234567890"),
            ("123 456 7890", "1234567890"),
        ],
    )
    def test_validate_phone_formats(
        self, validator: ContactValidator, phone, expected
    ) -> None:
        """Test multiple phone formats"""
        assert validator.validate_phone_num(phone) == expected

    @pytest.mark.parametrize(
        "email",
        [
            "test@example.com",
            "user.name@example.co.uk",
            "user+tag@example.com",
        ],
    )
    def test_validate_email_formats(self, validator: ContactValidator, email) -> None:
        """Test multiple valid email formats"""
        result = validator.validate_email(email)
        assert "@" in result
        assert "." in result
