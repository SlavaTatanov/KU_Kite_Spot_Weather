from telebot import TeleBot
import telebot.types
import os
from weather import Spots, Weather
from keyboards import spot_list_keyboard, cancel_keyboard
from AdminAccessTelegramBots import admin_access

bot = TeleBot(os.getenv("TOKEN"))

"""Регистрируем в телеграм боте команды меню"""
bot.set_my_commands([telebot.types.BotCommand("/weather", "Текущая погода"),
                     telebot.types.BotCommand("/weekend_weather", "Погода на выходные"),
                     telebot.types.BotCommand("/5_day_weather", "Погода на 5 дней"),
                     telebot.types.BotCommand("/add_spot", "Добавить место"),
                     telebot.types.BotCommand("/del_spot", "Удалить место")])

"""Создаем экземпляр класса с местами"""
spots = Spots("spots.json")


def cancel_option(func):
    """Определения декоратора для очистки ожидающих функций"""
    def wrapped(message, *args):
        if message.text == "Отмена":
            bot.clear_step_handler(message)
            return
        return func(message, *args)
    return wrapped


@bot.message_handler(commands=["weather", "5_day_weather", "weekend_weather"])
def weather_init(message):
    """
    При вызове команды weather пользователю предлагается выбрать место из списка
    или отправить свою текущую гео-позицию
    """
    bot.send_message(message.chat.id,
                     "Выберете из место из списка или отправите гео-позицию",
                     reply_markup=spot_list_keyboard(spots.all_spots_names(message.from_user.id)))
    weather_type = message.text
    bot.register_next_step_handler(message, weather_info, weather_type)


@cancel_option
def weather_info(message, weather_type):
    """
    Данная функция запрашивает погоду на текущий день и отправляет пользователю сформированное сообщение
    """
    if message.text not in spots.all_spots_names(message.from_user.id):
        bot.send_message(message.chat.id,
                         "Указанное место отсутствует",
                         reply_markup=spot_list_keyboard(spots.all_spots_names(message.from_user.id)))
        bot.register_next_step_handler(message, weather_info, weather_type)
    else:
        if message.location:
            coord = f"latitude={message.location.latitude}&longitude={message.location.longitude}"
            name = "в указанном месте"
        else:
            coord = spots.spot_coord(message.from_user.id, message.text)
            name = message.text
        answer = Weather(coord, name)
        if weather_type == "/weather":
            answer = answer.weather()
        elif weather_type == "/5_day_weather":
            answer = answer.five_day_weather()
        elif weather_type == "/weekend_weather":
            answer = answer.weekend_weather()
        bot.send_message(message.chat.id,
                         f"{answer}",
                         reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=["add_spot"])
def add_spot_init(message):
    """
    При вызове команды add_spot декоратор проверяет что пользователь админ и просит его ввести место
    и переходит к ожиданию следующей функции
    """
    bot.send_message(message.chat.id,
                     "Введите название места", reply_markup=cancel_keyboard())
    bot.register_next_step_handler(message, add_spot_name)


@cancel_option
def add_spot_name(message):
    """
    Принимает от пользователя название места и просит ввести координаты
    сохраняет название места в переменную spot_name и передает его в следующую функцию
    """
    spot_name = message.text
    bot.send_message(message.chat.id,
                     "Отправьте гео-позицию места")
    bot.register_next_step_handler(message, add_spot_coord, spot_name)


@cancel_option
def add_spot_coord(message, spot_name):
    """
    Проверяет верность ввода координат (пока это далеко не идеальный вариант, просто длина)
    Если координаты не верного формата просит их ввести заново
    Если координаты верных передает аргументы spot_name и spot_coord для записи нового места в JSON файл
    """
    if not message.location:
        bot.send_message(message.chat.id,
                         "❗ ЧТО ТО НЕ ТАК СО ВВОДОМ ❗\n\nОтправьте гео-позицию")
        bot.register_next_step_handler(message, add_spot_coord, spot_name)
    else:
        spot_coord = f"latitude={message.location.latitude}&longitude={message.location.longitude}"
        spots.add_spot(message.from_user.id, spot_name, spot_coord)
        bot.send_message(message.chat.id, "Выполнено")


@bot.message_handler(commands=["del_spot"])
def del_spot_init(message):
    bot.send_message(message.chat.id,
                     "Выберете место которое необходимо удалить",
                     reply_markup=spot_list_keyboard(spots.all_spots_names(message.from_user.id)))
    bot.register_next_step_handler(message, del_spot)


@cancel_option
def del_spot(message):
    try:
        spots.del_spot(message.from_user.id, message.text)
        bot.send_message(message.chat.id,
                         "Успешно",
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    except ValueError:
        bot.send_message(message.chat.id,
                         "❗ ЧТО ТО НЕ ТАК СО ВВОДОМ ❗",
                         reply_markup=spot_list_keyboard(spots.all_spots_names(message.from_user.id)))
        bot.register_next_step_handler(message, del_spot)


bot.polling(non_stop=True)
