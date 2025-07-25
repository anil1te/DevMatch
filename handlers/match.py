from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("match"))
async def match_command(message: types.Message):
    await message.answer("🔍 Ищем для тебя пару...")