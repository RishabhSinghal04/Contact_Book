from kivy.app import App
from repositories.contact_repository import ContactRepository
from presentation.gui.screens.contact_list_screen import ContactListScreen


class ContactBookApp(App):
    """Main Kivy application - ONLY handles app initialization"""

    def __init__(self, repository: ContactRepository, **kwargs) -> None:
        super().__init__(**kwargs)
        self.repository = repository

    def build(self) -> ContactListScreen:
        """Build and return root widget"""
        return ContactListScreen(self.repository)
