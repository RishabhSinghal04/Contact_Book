from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from contact.contact import Contact


class ContactCard(BoxLayout):
    """Widget for displaying a single contact"""

    def __init__(self, contact: Contact, on_edit=None, on_delete=None, **kwargs):
        super().__init__(orientation="horizontal", padding=10, spacing=10, **kwargs)

        self.contact = contact
        self.size_hint_y = None
        self.height = 80
        self.on_edit = on_edit
        self.on_delete = on_delete

        # Avatar (first letter)
        avatar = Label(
            text=contact.name[0].upper(),
            size_hint_x=None,
            width=66,
            font_size="24sp",
            bold=True,
            color=(1, 1, 1, 1),
            halign="center",
            valign="middle",
            text_size=(66, None),  # ensures proper alignment
        )

        # Contact info layout
        info_layout = BoxLayout(orientation="vertical", padding=5)

        name_label = Label(
            text=contact.name,
            font_size="18sp",
            bold=True,
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=30,
            text_size=(None, None),  # auto-adjusts
        )

        details = f"Phone: {contact.phone_num}"
        if contact.email:
            details += f"  |  Email: {contact.email}"

        details_label = Label(
            text=details,
            font_size="14sp",
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=30,
            color=(0.7, 0.7, 0.7, 1),
            text_size=(None, None),
        )

        info_layout.add_widget(name_label)
        info_layout.add_widget(details_label)

        # Buttons layout
        button_layout = BoxLayout(
            orientation="horizontal", size_hint_x=None, width=150, spacing=5
        )

        edit_btn = Button(text="Edit", background_color=(0.2, 0.6, 1, 1))
        edit_btn.bind(on_press=self.handle_edit)  # type: ignore

        delete_btn = Button(text="Delete", background_color=(1, 0.3, 0.3, 1))
        delete_btn.bind(on_press=self.handle_delete)  # type: ignore

        button_layout.add_widget(edit_btn)
        button_layout.add_widget(delete_btn)

        # Build card
        self.add_widget(avatar)
        self.add_widget(info_layout)
        self.add_widget(button_layout)

    def handle_edit(self, instance) -> None:
        if self.on_edit:
            self.on_edit(self.contact)

    def handle_delete(self, instance) -> None:
        if self.on_delete:
            self.on_delete(self.contact)
