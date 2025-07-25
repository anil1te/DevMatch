from aiogram import Router, types, F
import os
import random
import aiofiles
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services.db import db

router = Router()

class Registration(StatesGroup):
    country = State()
    city = State()
    age = State()
    photo = State()
    description = State()
    skills = State()
    stack = State()

@router.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    if await db.is_banned(user_id):
        await message.answer("❌ Ваш аккаунт заблокирован.")
        return
    
    if await db.check_user_exists(user_id):
        await message.answer("👋 С возвращением! Используйте /match для поиска.")
        return
    
    await message.answer(
        "📝 Давайте создадим ваш профиль!\n"
        "Введите вашу страну:"
    )
    await state.set_state(Registration.country)

@router.message(Registration.country)
async def process_country(message: types.Message, state: FSMContext):
    await state.update_data(country=message.text)
    await message.answer("🏙 Введите ваш город:")
    await state.set_state(Registration.city)

@router.message(Registration.city)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("🎂 Введите ваш возраст:")
    await state.set_state(Registration.age)

@router.message(Registration.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("🏞️ Скиньте фото")
    await state.set_state(Registration.photo)
    
@router.message(Registration.photo, F.photo)
async def process_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    random_num = random.randint(100000, 999999)
    dir_path = f"img/{user_id}"
    os.makedirs(dir_path, exist_ok=True)
    file_path = f"{dir_path}/{random_num}.jpg"
    file_data = await message.bot.download_file(file.file_path)
    async with aiofiles.open(file_path, 'wb') as out_file:
        await out_file.write(file_data.read())
    await state.update_data(photo=file_path)
    await message.answer("🧰 Расскажите о своём стеке: ")
    await state.set_state(Registration.stack)
    
@router.message(Registration.stack)
async def process_stack(message: types.Message, state: FSMContext):
    await state.update_data(skills=message.text)
    await message.answer("💫 Расскажите о своих скиллах: ")
    await state.set_state(Registration.skills)
    
@router.message(Registration.skills)
async def process_skills(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("📋 Расскажите о себе: ")
    await state.set_state(Registration.description)
    
    
@router.message(Registration.description)
async def process_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_data = {
        'telegram_id': message.from_user.id,
        'username': message.from_user.username or str(message.from_user.id),
        'country': data['country'],
        'city': data['city'],
        'age': data['age'],
        'photo_url': data.get('photo'),
        'descrip': data.get('description'),
        'skills': data.get('skills'),
        'stack': message.text
    }
    
    if await db.add_user(user_data):
        await message.answer("✅ Профиль успешно создан! Используйте /match для поиска.")
    else:
        await message.answer("❌ Ошибка при создании профиля. Попробуйте позже.")
    
    await state.clear()