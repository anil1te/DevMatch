from aiogram import Bot, Dispatcher
from colorama import Fore

from handlers import routers

from config.settings import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher()


for router in routers:
    dp.include_router(router)


if __name__ == "__main__":
    print(Fore.GREEN + "Я запустився")
    dp.run_polling(bot)