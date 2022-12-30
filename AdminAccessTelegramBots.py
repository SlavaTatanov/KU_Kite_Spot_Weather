from os import getenv

ADMIN = int(getenv("ADMIN"))


def admin_access(bot):
    def admin_access_decorator(func):
        def wrapped(message):
            if message.from_user.id != ADMIN:
                bot.send_message(message.chat.id, "Доступ запрещен")
                return
            return func(message)
        return wrapped
    return admin_access_decorator
