from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from colorama import init, Fore

from config.settings import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

init()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("👋 Привет, скрипткидди! Давай найдем тебе пару!")
    

if __name__ == "__main__":
    print(Fore.GREEN + "Я запустився")
    dp.run_polling(bot)