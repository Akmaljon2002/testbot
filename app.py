import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from models import User, Comment
from database import get_db, Base, engine

bot = Bot(token="7845434411:AAEqMOvvfWcZjyX3LiLiO2wSv_a2Z7wJM1E")
dp = Dispatcher()

class UserState(StatesGroup):
    fullname = State()
    telefon = State()

@dp.message(CommandStart())
async def start_func(message: Message, state: FSMContext):
    user_id = message.from_user.id
    with get_db() as database:
        user = database.query(User).filter(User.user_id == user_id).first()
        if user:
            await message.answer("Xush kelibsiz!, siz allaqachon ro'yhatdan o'tgansiz.")
        else:
            await message.answer("Ism va familiyangizni kiriitng!")
            await state.set_state(UserState.fullname)

@dp.message(UserState.fullname)
async def fullname_func(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer("Telefon raqamingizni kiriting!")
    await state.set_state(UserState.telefon)

@dp.message(UserState.telefon)
async def telefon_func(message: Message, state: FSMContext):
    await state.update_data(telefon=message.text)
    data = await state.get_data()
    fullname = data['fullname']
    telefon = data['telefon']
    with get_db() as database:
        user_id = message.from_user.id
        new_user = User(
            user_id=user_id,
            fullname=fullname,
            telefon=telefon
        )
        database.add(new_user)
        database.commit()
        await message.answer("Sizning malumotlaringiz saqlandi!")
        await state.clear()


class CommentState(StatesGroup):
    text = State()

@dp.message(Command('comment'))
async def comment_func(message: Message, state: FSMContext):
    await message.answer("Izohingizni yozing!")
    await state.set_state(CommentState.text)

@dp.message(CommentState.text)
async def text_func(message: Message, state: FSMContext):
    text = message.text
    with get_db() as database:
        new_comment = Comment(
            user_id=message.from_user.id,
            text=text
        )
        database.add(new_comment)
        database.commit()
        await message.answer("Sizning commentingiz saqlandi")
        await state.clear()

@dp.message(Command('izohlar'))
async def izohlar_func(message: Message):
    user_id = message.from_user.id
    with get_db() as db:
        izohlar = db.query(Comment).filter(Comment.user_id == user_id).all()
        for izoh in izohlar:
            await message.answer(f"{izoh.text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    asyncio.run(main())