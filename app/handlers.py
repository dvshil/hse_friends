import asyncio
import re

from re import match

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.database.orm import SyncORM, AsyncORM


import app.keyboards as kb
import app.database.requests as rq


router = Router()


class Register(StatesGroup):
    name = State()
    age = State()
    birthday = State()
    zodiac = State()
    group = State()
    hobbies = State()
    contact = State()
    photo_id = State()



@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Я помогу найти тебе друзей😇', reply_markup=kb.start)


@router.message(F.text == 'Давай начнем😜')
async def reg_start(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введи фамилию и имя', reply_markup=ReplyKeyboardRemove())


@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer('Сколько тебе лет?')


@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.birthday)
    await message.answer('Укажи дату рождения')


@router.message(Register.birthday)
async def register_birthday(message: Message, state: FSMContext):
    await state.update_data(birthday=message.text)
    await state.set_state(Register.zodiac)
    await message.answer('Кто ты по знаку зодиака?')


@router.message(Register.zodiac)
async def register_zodiac(message: Message, state: FSMContext):
    await state.update_data(zodiac=message.text)
    await state.set_state(Register.group)
    await message.answer('Из какой ты группы?', reply_markup=kb.group)

@router.message(Register.group)
async def register_group(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    await state.set_state(Register.hobbies)
    await message.answer('Расскажи о себе и кого хочешь найти',
                         reply_markup=ReplyKeyboardRemove())


@router.message(Register.hobbies)
async def register_hobbies(message: Message, state: FSMContext):
    await state.update_data(hobbies=message.text)
    await state.set_state(Register.contact)
    await message.answer('Как с тобой связаться?')

@router.message(Register.contact)
async def register_contact(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await state.set_state(Register.photo_id)
    await message.answer('Теперь пришли фото')

@router.message(Register.photo_id)
async def register_photo(message: Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    await message.answer('Фото загружено')
    await message.answer('Так выглядит твоя анкета:')
    data = await state.get_data()

    curr = await AsyncORM.insert_users(str(data["contact"]))
    pk = curr[0].model_dump()

    await AsyncORM.insert_profiles(str(data["name"]), int(data["age"]), str(data["birthday"]), str(data["zodiac"]),
                                   str(data["group"]),
                                   str(data["hobbies"]), str(data["contact"]), str(data["photo_id"]), int(pk["id"]))
    await message.answer_photo(photo=data["photo_id"], caption=f'{data["name"]}, '
                                                            f'{data["age"]} лет\n{data["birthday"]}, {data["zodiac"]}\n'
                                                               f'{data["hobbies"]}\n'
                                                            f'{data["group"]}\n{data["contact"]}')
    await state.clear()

    await message.answer('1. Смотреть анкеты.\n2. Заполнить анкету заново.\n3. Изменить фото/видео.\n'
                         '4.Изменить текст анкеты.', reply_markup=kb.action)


@router.message(F.text.contains('1') | F.text.contains('👎'))
async def see_profiles(message: Message):
    data = await AsyncORM.convert_users_to_dto() #start sending profiles
    # data_photo = await AsyncORM.convert_photo_to_dto()
    user_dto = data[0].model_dump()
    # photo_dto = data_photo[0].model_dump()
    await message.answer_photo(photo=user_dto["photo_id"], caption=f'{user_dto["name"]}, '
                                                            f'{user_dto["age"]} лет\n{user_dto["birthday"]}\n{user_dto["hobbies"]}\n'
                                                            f'{user_dto["group"]}\n{user_dto["contact"]}',
                               reply_markup=kb.profile_view)


@router.message(F.text == '2')
async def restart_reg(message: Message, state: FSMContext):
    await reg_start(message, state)


@router.message(F.text == '3')
async def edit_photo(message: Message, state: FSMContext):
    await message.answer('Теперь пришли фото')


@router.message(F.text == '4')
async def edit_hobbies(message: Message, state: FSMContext):
    await message.answer('Расскажи о себе и кого хочешь найти')



# @router.message(F.photo)
# async def send_photo(message: Message):
#     ph_id = str(message.photo[-1].file_id)
#     await AsyncORM.insert_photo(ph_id)
#     await message.answer_photo(photo=ph_id, caption='Photo successfully saved! Appreciate you')

@router.message(F.text == 'pk')
async def print_get(message: Message):
    curr = await AsyncORM.insert_users("@imukuev")
    pk = curr.model_dump()
    print(pk)





@router.message(Command('myprofile'))
async def my_profile(message: Message):
    await message.answer('send profile')




