from typing import Optional, Callable

from core.interfaces import IOutputHandler
from core.contact_constants import CONSTRAINTS

from contact.contact import Contact
from repositories.contact_repository import ContactRepository
from contact.contact_factory import ContactFactory
from utils.exceptions import (
    ValidationError,
    ContactNotFoundError,
    ContactAlreadyExistsError,
)

from presentation.input_handler import UserInputHandler
from presentation.cli.options_display import options_display
from presentation.cli.contact_display import contact_display
from presentation.confirmation import confirm_action
from presentation.key_map import (
    MENU_KEY_MAP,
    SEARCH_BY_KEY_MAP,
    menu_key_map,
    search_by_key_map,
)


class Menu:
    def __init__(
        self,
        repository: ContactRepository,
        input_handler: UserInputHandler,
        output_handler: IOutputHandler,
    ) -> None:
        self._input_handler = input_handler
        self._output_handler = output_handler
        self._repository = repository

    def menu(self) -> None:
        while True:
            self._output_handler.display("\nCONTACT BOOK MENU")
            options_display(menu_key_map, self._output_handler)

            choice = self._input_handler.get_action("\nEnter choice: ", menu_key_map)

            match choice:
                case MENU_KEY_MAP.EXIT.value:
                    self._output_handler.display("exit")
                    break
                case MENU_KEY_MAP.ADD_CONTACT.value:
                    self._safe_execute(self.add_contact)
                case MENU_KEY_MAP.UPDATE_CONTACT.value:
                    self._safe_execute(self.update_contact)
                case MENU_KEY_MAP.SEARCH_CONTACT.value:
                    self._safe_execute(self.search_contact)
                case MENU_KEY_MAP.VIEW_CONTACTS.value:
                    self._safe_execute(self.view_contacts)
                case MENU_KEY_MAP.DELETE_CONTACT.value:
                    self._safe_execute(self.delete_contact)
                case _:
                    self._output_handler.display("Invalid")

    def add_contact(self) -> None:
        contact = ContactFactory.create_contact(
            self._input_handler, self._output_handler
        )
        self._repository.add(contact)
        self._output_handler.display(f"Added: {contact.name}")

    def delete_contact(self) -> None:
        self._output_handler.display("\n--- Delete Contact ---")
        contact = self.search_contact()

        if not contact:
            self._output_handler.display(f"Contact not found")
            return

        self._output_handler.display(f"Contact: {str(contact)}")

        if confirm_action(
            self._input_handler,
            self._output_handler,
            "Do you wnat to delele the contact? ",
        ):
            self._repository.delete(contact)
            self._output_handler.display(f"Deleted {str(contact)}")

    def update_contact(self) -> None:
        self._output_handler.display("\n--- Update Contact ---")
        old_contact = self.search_contact()

        if not old_contact:
            self._output_handler.display(f"Contact not found")
            return

        self._output_handler.display(f"Current: {old_contact}")
        self._output_handler.display("Enter new details:-")
        try:
            new_contact = ContactFactory.create_contact(
                self._input_handler, self._output_handler
            )
            self._repository.update(old_contact, new_contact)
            self._output_handler.display(f"Updated: {new_contact.name}")
        except ValidationError as e:
            self._output_handler.display(f"{e}")

    def search_contact(self) -> Optional[Contact]:
        self._output_handler.display("\n--- Search Contact ---")
        options_display(
            search_by_key_map, self._output_handler, " " * len(search_by_key_map)
        )

        while True:
            choice = self._input_handler.get_action(
                "Select an option: ", search_by_key_map
            )
            if choice == SEARCH_BY_KEY_MAP.BACK.value:
                return None

            contact = self._handle_search_choice(choice)
            if contact:
                self._output_handler.display(f"Found {contact}")
                return contact
            else:
                self._output_handler.display("Contact not found. Try again.")

    def view_contacts(self) -> None:
        contact_display(self._repository, self._output_handler)

    def _safe_execute(self, action: Callable) -> None:
        try:
            action()
        except (ValidationError, ContactNotFoundError, ContactAlreadyExistsError) as e:
            self._output_handler.display(f"{e}")
        except Exception as e:
            self._output_handler.display(f"Unexpected error: {e}")

    def _handle_search_choice(self, choice) -> Optional[Contact]:
        """Handle search by name or phone"""
        if choice == SEARCH_BY_KEY_MAP.SEARCH_BY_NAME.value:
            name = self._input_handler.get_string(
                "Enter name: ", CONSTRAINTS.name_max_length
            )
            return self._repository.search_by_name(name)
        elif choice == SEARCH_BY_KEY_MAP.SEARCH_BY_PHONE_NUM.value:
            phone_num = self._input_handler.get_string(
                "Enter phone number: ", CONSTRAINTS.phone_num_max_length
            )
            return self._repository.search_by_phone(phone_num)
        return None
