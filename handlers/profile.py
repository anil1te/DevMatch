from aiogram import Router, types
import os
from aiogram.filters import Command
from services.db import db

router = Router()

@router.message(Command("profile"))
async def show_profile(message: types.Message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    if not user:
        await message.answer("Профиль не найден. Пройдите регистрацию через /start.")
        return
    text = (
        f"👤 <b>{user['username']}</b>\n"
        f"🌍 Страна: {user['country']}\n"
        f"🏙 Город: {user['city']}\n"
        f"🎂 Возраст: {user['age']}\n"
        f"🧰 Стек: {user['stack']}\n"
        f"💫 Скиллы: {user['skills']}\n"
        f"📋 О себе: {user['descrip']}"
    )
    if user.get('photo_url') and os.path.exists(user['photo_url']):
        with open(user['photo_url'], 'rb') as photo:
            await message.answer_photo(photo, caption=text, parse_mode='HTML')
    else:
        await message.answer(text, parse_mode='HTML')
