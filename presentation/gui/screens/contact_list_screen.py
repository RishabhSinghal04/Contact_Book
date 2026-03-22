from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from repositories.contact_repository import ContactRepository
from contact.contact import Contact

from presentation.gui.widgets.contact_card import ContactCard
from presentation.gui.dialogs.add_contact_dialog import AddContactDialog
from presentation.gui.dialogs.edit_contact_dialog import EditContactDialog
from presentation.gui.dialogs.delete_confirm_dialog import DeleteConfirmDialog


class ContactListScreen(BoxLayout):
    """Main screen for displaying contact list - ONLY handles screen layout and coordination"""

    def __init__(self, repository: ContactRepository, **kwargs) -> None:
        super().__init__(**kwargs)
        self.repository = repository
        self.orientation = "vertical"

        # Build UI
        self._build_header()
        self._build_search_bar()
        self._build_contact_list()
        self._build_status_bar()

        # Load initial data
        self.load_contacts()

    def _build_header(self) -> None:
        """Build header with title and add button"""
        header = BoxLayout(size_hint_y=None, height=60, padding=10, spacing=10)

        title = Label(text="Contact Book", font_size="24sp", bold=True, size_hint_x=0.6)

        add_btn = Button(
            text="Add Contact",
            size_hint_x=0.4,
            background_color=(0.2, 0.6, 1, 1),
            font_size="16sp",
        )
        add_btn.bind(on_press=self._show_add_dialog)  # type: ignore

        header.add_widget(title)
        header.add_widget(add_btn)

        self.add_widget(header)

    def _build_search_bar(self) -> None:
        """Build search bar with input and clear button"""
        search_layout = BoxLayout(size_hint_y=None, height=50, padding=10, spacing=10)

        self.search_input = TextInput(
            hint_text="Search contacts...",
            multiline=False,
            size_hint_x=0.8,
            font_size="16sp",
        )
        self.search_input.bind(text=self._on_search)  # type: ignore

        clear_btn = Button(
            text="Clear", size_hint_x=0.2, background_color=(0.5, 0.5, 0.5, 1)
        )
        clear_btn.bind(on_press=self._clear_search)  # type: ignore

        search_layout.add_widget(self.search_input)
        search_layout.add_widget(clear_btn)

        self.add_widget(search_layout)

    def _build_contact_list(self) -> None:
        """Build scrollable contact list"""
        scroll_view = ScrollView()

        self.contacts_layout = BoxLayout(
            orientation="vertical", size_hint_y=None, spacing=5, padding=10
        )
        self.contacts_layout.bind(minimum_height=self.contacts_layout.setter("height"))  # type: ignore

        scroll_view.add_widget(self.contacts_layout)
        self.add_widget(scroll_view)

    def _build_status_bar(self) -> None:
        """Build status bar"""
        self.status_label = Label(
            text="Ready",
            size_hint_y=None,
            height=30,
            font_size="14sp",
            color=(0.7, 0.7, 0.7, 1),
        )
        self.add_widget(self.status_label)

    def load_contacts(self, search_term: str = "") -> None:
        """Load and display contacts from repository"""
        # Clear existing
        self.contacts_layout.clear_widgets()

        # Get from backend
        contacts = self.repository.get_all()

        # Filter by search term
        if search_term:
            search_term = search_term.lower()
            contacts = [
                c
                for c in contacts
                if search_term in c.name.lower() or search_term in c.phone_num
            ]

        # Create contact cards
        for contact in contacts:
            card = ContactCard(
                contact,
                on_edit=self._show_edit_dialog,
                on_delete=self._show_delete_confirm,
            )
            self.contacts_layout.add_widget(card)

        # Update status
        self.status_label.text = f"{len(contacts)} contact(s)"

    def _on_search(self, instance, value: str) -> None:
        """Handle search input change"""
        self.load_contacts(value)

    def _clear_search(self, instance) -> None:
        """Clear search input"""
        self.search_input.text = ""

    def _show_add_dialog(self, instance) -> None:
        """Show add contact dialog"""
        dialog = AddContactDialog(self.repository, on_success=self.load_contacts)
        dialog.open()

    def _show_edit_dialog(self, contact: Contact) -> None:
        """Show edit contact dialog"""
        dialog = EditContactDialog(
            self.repository, contact, on_success=self.load_contacts
        )
        dialog.open()

    def _show_delete_confirm(self, contact: Contact) -> None:
        """Show delete confirmation dialog"""
        dialog = DeleteConfirmDialog(contact, on_confirm=self._delete_contact)
        dialog.open()

    def _delete_contact(self, contact: Contact) -> None:
        """Delete contact using repository"""
        try:
            self.repository.delete(contact)
            self.load_contacts()
        except Exception as e:
            error_popup = Popup(
                title="Error", content=Label(text=str(e)), size_hint=(0.8, 0.3)
            )
            error_popup.open()
