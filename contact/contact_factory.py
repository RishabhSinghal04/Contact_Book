from core.interfaces import IOutputHandler
from core.contact_constants import CONSTRAINTS

from contact.contact import Contact
from contact.contact_validator import ContactValidator

from presentation.input_handler import UserInputHandler
from presentation.confirmation import confirm_action


class ContactFactory:
    """Create a validated contact from user input"""

    @classmethod
    def create_contact(
        cls, input_handler: UserInputHandler, output_handler: IOutputHandler
    ) -> Contact:
        """
        Prompt the user for contact details, validate them, and return a Contact object.

        Args:
            input_handler (UserInputHandler): Handles user input prompts.
            output_handler (IOutputHandler): Handles output display.

        Returns:
            Contact: A fully validated Contact object containing name, phone number, and optionally email.

        Raises:
            ValidationError: If any of the validator methods 
            (`validate_name`, `validate_phone_num`, `validate_email`) detect invalid input.
        """
        validator = ContactValidator()

        name = input_handler.get_string("Name: ", CONSTRAINTS.name_max_length)
        phone_num = input_handler.get_string(
            "Phone Number: ", CONSTRAINTS.phone_input_max_length
        )

        valid_name = validator.validate_name(name)
        valid_phone_num = validator.validate_phone_num(phone_num)

        output_handler.display("Email:-")
        email_choice = confirm_action(input_handler, output_handler)
        valid_email = None

        if email_choice:
            email = input_handler.get_string("Email: ", CONSTRAINTS.email_max_length)
            valid_email = validator.validate_email(email)

        return Contact(valid_name, valid_phone_num, valid_email)
