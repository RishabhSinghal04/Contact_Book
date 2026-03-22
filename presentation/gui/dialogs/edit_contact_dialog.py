from typing import Callable
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from repositories.contact_repository import ContactRepository
from contact.contact import Contact
from contact.contact_validator import ContactValidator
from utils.exceptions import ValidationError, ContactNotFoundError


class EditContactDialog(Popup):
    """Dialog for editing an existing contact"""

    def __init__(
        self,
        repository: ContactRepository,
        contact: Contact,
        on_success: Callable[[], None],
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.repository = repository
        self.contact = contact
        self.validator = ContactValidator()
        self.on_success = on_success

        self.title = f"Edit Contact: {contact.name}"
        self.size_hint = (0.9, 0.7)

        # Build UI
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Name field
        layout.add_widget(
            Label(text="Name:", size_hint_y=None, height=30, halign="left")
        )
        self.name_input = TextInput(
            text=contact.name,
            multiline=False,
            size_hint_y=None,
            height=40,
            font_size="16sp",
        )
        layout.add_widget(self.name_input)

        # Phone field (read-only)
        layout.add_widget(
            Label(
                text="Phone (cannot be changed):",
                size_hint_y=None,
                height=30,
                halign="left",
                color=(0.7, 0.7, 0.7, 1),
            )
        )
        phone_display = Label(
            text=contact.phone_num,
            size_hint_y=None,
            height=40,
            font_size="16sp",
            color=(0.5, 0.5, 0.5, 1),
            halign="left",
        )
        layout.add_widget(phone_display)

        # Email field
        layout.add_widget(
            Label(text="Email (optional):", size_hint_y=None, height=30, halign="left")
        )
        self.email_input = TextInput(
            text=contact.email or "",
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
            text="Save Changes", background_color=(0.2, 0.8, 0.2, 1), font_size="16sp"
        )
        save_btn.bind(on_press=self._save_changes)  # type: ignore

        cancel_btn = Button(
            text="Cancel", background_color=(0.5, 0.5, 0.5, 1), font_size="16sp"
        )
        cancel_btn.bind(on_press=self.dismiss)  # type: ignore

        button_layout.add_widget(save_btn)
        button_layout.add_widget(cancel_btn)

        layout.add_widget(button_layout)

        self.content = layout

    def _save_changes(self, instance) -> None:
        """Validate and update contact using backend"""
        try:
            # Get values
            name = self.name_input.text.strip()
            email = self.email_input.text.strip() or None

            # Validate using backend validator
            valid_name = self.validator.validate_name(name)
            valid_email = self.validator.validate_email(email) if email else None

            # Create updated contact (phone stays same)
            new_contact = Contact(valid_name, self.contact.phone_num, valid_email)

            # Update using backend repository
            self.repository.update(self.contact, new_contact)

            # Success - callback and close
            self.on_success()
            self.dismiss()

        except ValidationError as e:
            self.error_label.text = f"Validation Error: {str(e)}"
        except ContactNotFoundError as e:
            self.error_label.text = f"Error: {str(e)}"
        except Exception as e:
            self.error_label.text = f"Error: {str(e)}"
