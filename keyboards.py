from telebot import types


def spot_list_keyboard(spot_lst):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*spot_lst, row_width=1)
    return keyboard
