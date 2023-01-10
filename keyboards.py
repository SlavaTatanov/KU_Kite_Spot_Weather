from telebot import types


def spot_list_keyboard(spot_lst):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*spot_lst, "Отмена", row_width=1)
    return keyboard


def cancel_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("Отмена")
    return keyboard


