from typing import Callable
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from repositories.contact_repository import ContactRepository
from contact.contact import Contact
from contact.contact_validator import ContactValidator
from utils.exceptions import ValidationError, ContactAlreadyExistsError


class AddContactDialog(Popup):
    """Dialog for adding a new contact"""

    def __init__(
        self, repository: ContactRepository, on_success: Callable[[], None], **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.repository = repository
        self.validator = ContactValidator()
        self.on_success = on_success

        self.title = "Add New Contact"
        self.size_hint = (0.9, 0.7)

        # Build UI
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Name field
        layout.add_widget(
            Label(text="Name:", size_hint_y=None, height=30, halign="left")
        )
        self.name_input = TextInput(
            hint_text="Enter full name",
            multiline=False,
            size_hint_y=None,
            height=40,
            font_size="16sp",
        )
        layout.add_widget(self.name_input)

        # Phone field
        layout.add_widget(
            Label(text="Phone:", size_hint_y=None, height=30, halign="left")
        )
        self.phone_input = TextInput(
            hint_text="123-456-7890",
            multiline=False,
            size_hint_y=None,
            height=40,
            font_size="16sp",
        )
        layout.add_widget(self.phone_input)

        # Email field
        layout.add_widget(
            Label(text="Email (optional):", size_hint_y=None, height=30, halign="left")
        )
        self.email_input = TextInput(
            hint_text="name@example.com",
            multiline=False,
            size_hint_y=None,
            height=40,
            font_size="16sp",
        )
        layout.add_widget(self.email_input)

        # Error message label
        self.error_label = Label(
            text="", size_hint_y=None, height=30, color=(1, 0.3, 0.3, 1)
        )
        layout.add_widget(self.error_label)

        # Action buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)

        save_btn = Button(
            text="Save Contact", background_color=(0.2, 0.8, 0.2, 1), font_size="16sp"
        )
        save_btn.bind(on_press=self._save_contact)  # type: ignore

        cancel_btn = Button(
            text="Cancel", background_color=(0.5, 0.5, 0.5, 1), font_size="16sp"
        )
        cancel_btn.bind(on_press=self.dismiss)  # type: ignore

        button_layout.add_widget(save_btn)
        button_layout.add_widget(cancel_btn)

        layout.add_widget(button_layout)

        self.content = layout

    def _save_contact(self, instance) -> None:
        """Validate and save contact using backend"""
        try:
            # Get values
            name = self.name_input.text.strip()
            phone = self.phone_input.text.strip()
            email = self.email_input.text.strip() or None

            # Validate using backend validator
            valid_name = self.validator.validate_name(name)
            valid_phone = self.validator.validate_phone_num(phone)
            valid_email = self.validator.validate_email(email) if email else None

            # Create contact using backend
            contact = Contact(valid_name, valid_phone, valid_email)

            # Add using backend repository
            self.repository.add(contact)

            # Success - callback and close
            self.on_success()
            self.dismiss()

        except ValidationError as e:
            self.error_label.text = f"Validation Error: {str(e)}"
        except ContactAlreadyExistsError as e:
            self.error_label.text = f"Error: {str(e)}"
        except Exception as e:
            self.error_label.text = f"Error: {str(e)}"
