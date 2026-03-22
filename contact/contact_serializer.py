from contact.contact import Contact


class ContactSerializer:
    @staticmethod
    def to_dict(contact: Contact) -> dict:
        return {
            "name": contact.name,
            "phone_num": contact.phone_num,
            "email": contact.email,
        }

    @classmethod
    def from_dict(cls, data: dict) -> Contact:
        return Contact(
            name=data["name"], phone_num=data["phone_num"], email=data.get("email")
        )
