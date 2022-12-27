from telebot import TeleBot
import telebot.types
import os
from weather import Spots
from keyboards import spot_list_keyboard

bot = TeleBot(os.getenv("TOKEN"))

bot.set_my_commands([telebot.types.BotCommand("/weather", "Текущая погода"),
                     telebot.types.BotCommand("/weekend_weather", "Погода на выходные"),
                     telebot.types.BotCommand("/5_day_weather", "Погода на 5 дней"),
                     telebot.types.BotCommand("/add_spot", "Добавить место")])

spots = Spots("spots.json")


@bot.message_handler(commands=["weather"])
def weather_init(message):
    bot.send_message(message.chat.id,
                     "Выберете из место из списка или отправите геопозицию",
                     reply_markup=spot_list_keyboard(spots.all_spots_names()))
    bot.register_next_step_handler(message, weather_info)


def weather_info(message):
    bot.send_message(message.chat.id,
                     "Погода",
                     reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=["add_spot"])
def add_spot_init(message):
    if str(message.chat.id) == os.getenv("ADMIN"):
        bot.send_message(message.chat.id,
                         "Введите название места")
        bot.register_next_step_handler(message, add_spot_name)
    else:
        bot.send_message(message.chat.id,
                         "Недостаточно прав")


def add_spot_name(message):
    spot_name = message.text
    bot.send_message(message.chat.id,
                     "Введите координаты по типу хх.хх хх.хх")
    bot.register_next_step_handler(message, add_spot_coord, spot_name)


def add_spot_coord(message, spot_name):
    if len(message.text) != 11:
        bot.send_message(message.chat.id,
                         "❗ ЧТО ТО НЕ ТАК СО ВВОДОМ ❗\n\nПовторите ввод (хх.хх хх.хх)")
        bot.register_next_step_handler(message, add_spot_coord, spot_name)
    else:
        spots.add_spot(spot_name, spot_coord=message.text)
        bot.send_message(message.chat.id, "Выполнено")


bot.polling(non_stop=True)
