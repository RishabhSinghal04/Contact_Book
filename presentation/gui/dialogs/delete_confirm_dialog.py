from typing import Callable
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from contact.contact import Contact


class DeleteConfirmDialog(Popup):
    """Confirmation dialog for deleting a contact"""

    def __init__(
        self, contact: Contact, on_confirm: Callable[[Contact], None], **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.contact = contact
        self.on_confirm = on_confirm

        self.title = "Confirm Delete"
        self.size_hint = (0.8, 0.4)

        # Build UI
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Confirmation message
        message = Label(
            text=f"Are you sure you want to delete\n'{contact.name}'?",
            font_size="18sp",
            halign="center",
        )
        layout.add_widget(message)

        # Action buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)

        delete_btn = Button(
            text="Delete", background_color=(1, 0.3, 0.3, 1), font_size="16sp"
        )
        delete_btn.bind(on_press=self._confirm_delete)  # type: ignore

        cancel_btn = Button(
            text="Cancel", background_color=(0.5, 0.5, 0.5, 1), font_size="16sp"
        )
        cancel_btn.bind(on_press=self.dismiss)  # type: ignore

        button_layout.add_widget(delete_btn)
        button_layout.add_widget(cancel_btn)

        layout.add_widget(button_layout)

        self.content = layout

    def _confirm_delete(self, instance) -> None:
        """Execute deletion callback and close"""
        self.on_confirm(self.contact)
        self.dismiss()
