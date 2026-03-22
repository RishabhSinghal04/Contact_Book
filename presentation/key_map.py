from enum import IntEnum


class CONFIRMATION_KEY_MAP(IntEnum):
    YES = 1
    NO = 0


confirmation_key_map = {e.value: e.name.lower() for e in CONFIRMATION_KEY_MAP}


class MENU_KEY_MAP(IntEnum):
    ADD_CONTACT = 1
    UPDATE_CONTACT = 2
    SEARCH_CONTACT = 3
    VIEW_CONTACTS = 4
    DELETE_CONTACT = 5
    EXIT = 0


menu_key_map = {e.value: e.name.lower() for e in MENU_KEY_MAP}


class SEARCH_BY_KEY_MAP(IntEnum):
    SEARCH_BY_NAME = 1
    SEARCH_BY_PHONE_NUM = 2
    BACK = 0


search_by_key_map = {e.value: e.name.lower() for e in SEARCH_BY_KEY_MAP}
