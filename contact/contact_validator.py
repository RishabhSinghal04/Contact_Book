import re
from email.utils import parseaddr
from functools import lru_cache

from utils.exceptions import ValidationError
from utils.logger import get_logger

from core.contact_constants import CONSTRAINTS

logger = get_logger(__name__)


class ContactValidator:
    """
    Utility class for validating contact details such as name, phone number,
    and email address. Raises ValidationError when inputs are invalid.
    """

    @staticmethod
    def validate_name(name: str) -> str:
        """
        Validate a contact's name.

        Args:
            name (str): The name to validate.

        Returns:
            str: A cleaned and validated name string.

        Raises:
            ValidationError: If the name is empty or exceeds the maximum length.
        """
        if not name or not name.strip():
            logger.warning("Attempted to create contact with empty name")
            raise ValidationError("Name cannot be empty")
        if len(name) > CONSTRAINTS.name_max_length:
            raise ValidationError(
                f"Name too long (max {CONSTRAINTS.name_max_length} characters)"
            )
        return name.strip()

    @staticmethod
    def validate_phone_num(phone_num: str) -> str:
        """
        Validate a contact's phone number.

        Args:
            phone_num (str): The phone number to validate.
            min_digits (int, optional): Minimum required digits. Defaults to 7.
            max_digits (int, optional): Maximum allowed digits. Defaults to 20.

        Returns:
            str: A cleaned phone number containing only digits.

        Raises:
            ValidationError: If the phone number contains non-digit characters or does not meet length requirements.
        """
        pattern = ContactValidator._get_phone_num_clean_pattern()
        cleaned = pattern.sub("", phone_num)

        if not cleaned.isdigit():
            logger.warning(f"Invalid phone number format: {phone_num}")
            raise ValidationError("Phone number must contain only digits")
        if not (
            CONSTRAINTS.phone_num_min_length
            <= len(cleaned)
            <= CONSTRAINTS.phone_num_max_length
        ):
            raise ValidationError(
                f"Phone number must be {CONSTRAINTS.phone_num_min_length}-{CONSTRAINTS.phone_num_max_length} digits"
            )
        return cleaned

    @staticmethod
    def validate_email(email: str) -> str:
        """
        Validate a contact's email address.

        Args:
            email (str): The email address to validate.

        Returns:
            str: A cleaned and validated email address.

        Raises:
            ValidationError: If the email format is invalid.
        """
        _, address = parseaddr(email)

        if not bool(address and "@" in address and "." in address.split("@")[-1]):
            logger.warning(f"Invalid email format: {email}")
            raise ValidationError("Invalid email format")
        return address.strip()

    @staticmethod
    @lru_cache(maxsize=1)
    def _get_phone_num_clean_pattern() -> re.Pattern[str]:
        return re.compile(r"[\s()+\-]")
