from dataclasses import dataclass


@dataclass(frozen=True)
class ContactConstraints:
    name_min_length = 1
    name_max_length = 20

    phone_num_min_length = 7
    phone_num_max_length = 15

    phone_input_max_length = 30

    email_max_length = 254


CONSTRAINTS = ContactConstraints()
