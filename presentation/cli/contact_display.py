from core.interfaces import IOutputHandler
from repositories.contact_repository import ContactRepository


def contact_display(
    repository: ContactRepository, output_handler: IOutputHandler, border_char="*"
) -> None:
    """Display all contacts"""
    if len(repository) == 0:
        output_handler.display("No contacts found.")
        return

    heading_text = f"All Contacts ({len(repository)})"
    contacts = repository.get_all()

    max_contact_width = max((len(str(contact)) for contact in repository), default=0)
    heading = heading_text.center(max(len(heading_text), max_contact_width))
    output_handler.display(heading)

    border = border_char * max_contact_width
    output_handler.display(border)

    text_contacts = "\n".join(str(contact) for contact in contacts)
    output_handler.display(text_contacts)

    border = border_char * max_contact_width
    output_handler.display(border)
