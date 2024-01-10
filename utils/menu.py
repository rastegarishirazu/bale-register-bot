from bale import User, MenuKeyboardMarkup, MenuKeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from content import RegisterMode, register_mode_fild_name, MENU_LIST


def create_menu():
    menu = MenuKeyboardMarkup()
    for fild , i in zip(MENU_LIST, range(len(MENU_LIST))):
        menu.add(MenuKeyboardButton(text=fild), row=i//2+1)
    return menu


def edit_menu():
    menu = InlineKeyboardMarkup()
    for fild, i in zip(register_mode_fild_name, range(len(register_mode_fild_name))):
        menu.add(InlineKeyboardButton(text=register_mode_fild_name[fild], callback_data=f'{fild.value}:edit'),
                 row=i // 2 + 1)
    return menu
