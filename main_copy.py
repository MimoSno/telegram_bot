import sqlite3
import time
# Импорты из aiogram'а
from aiogram import Bot, Dispatcher, executor, types
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, CallbackQuery

from config import TOKEN, connect, cursor

bot = Bot(TOKEN)

loop = asyncio.get_event_loop()

dp = Dispatcher(bot, loop=loop)

name = None
surname = None
user_age = None
edit = "no"
black_list_counter = 5
user_black_list_counter = 0


def reset():
    global name
    global surname
    global user_age
    name = None
    surname = None
    user_age = None


@dp.message_handler(content_types=['text'])
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global name, surname, user_age
    if message.text == '/start':
        # Эти переменные нужны для корректной работы с Базой Данных

        global user_id
        user_id = message.from_user.id
        

        cursor.execute(f"SELECT user_id FROM data WHERE user_id = {user_id}")
        if cursor.fetchone() is None:
            global name, surname, user_age

            cursor.execute(f"INSERT INTO data VALUES(?,?,?,?)", (user_id, name, surname, user_age))
            connect.commit()  # Сохранение изменений
            await bot.send_message(message.from_user.id, "Как тебя зовут?")
            await bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name
        else:
            await bot.send_message(message.from_user.id, 'Вы уже проводили регистрацию')

            # Все эти махинации нужны для корректного отображения данных
            # Извлечение данных из БД
            cursor.execute(f"SELECT * FROM data WHERE user_id={user_id}")
            db_data = list(cursor.fetchone())
            print(db_data)
            name = db_data[1]
            print(name)
            surname = db_data[2]
            print(surname)
            user_age = db_data[3]
            print(user_age)

            # Требуется для подтверждения данных
            keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
            key_yes = types.InlineKeyboardButton(text='✅Да', callback_data='yes')  # кнопка «Да»
            keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
            key_no = types.InlineKeyboardButton(text='❌Нет', callback_data='no')
            keyboard.add(key_no)
            question = 'Тебе ' + str(user_age) + ' лет, тебя зовут ' + str(name) + ' ' + str(surname) + '?'
            await bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
            reset()

    else:
        await bot.send_message(message.from_user.id, 'Напиши /start')


async def get_name(message: types.Message):  # получаем фамилию
    global name
    name = message.text
    # Эти переменные нужны для корректной работы с Базой Данных

    if edit == "yes":
        global edit_name
        edit_name = message.text
        cursor.execute(f"UPDATE data SET user_name = ? WHERE user_id = ?", (edit_name, user_id))
        connect.commit()
        edit_name = None
        await bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
        await bot.register_next_step_handler(message, get_surname)
    else:
        cursor.execute(f"SELECT user_name FROM data WHERE user_id = {user_id}")
        print(cursor.fetchone())
        print(type(cursor.fetchone()))
        if cursor.fetchone() is None:
            cursor.execute(f"UPDATE data SET user_name = ? WHERE user_id = ?", (name, user_id))
            connect.commit()  # Сохранение изменений
        name = ""
        await bot.send_message(message.from_user.id, 'Какая у тебя фамилия?')
        await bot.register_next_step_handler(message, get_surname)


async def get_surname(message: types.Message):
    global surname
    surname = message.text
    # Эти переменные нужны для корректной работы с Базой Данных

    if edit == "yes":
        global edit_surname
        edit_surname = message.text
        cursor.execute(f"UPDATE data SET user_surname = ? WHERE user_id = ?", (edit_surname, user_id))
        connect.commit()
        edit_surname = None
        await bot.send_message(message.from_user.id, "Сколько тебе лет?")
        await bot.register_next_step_handler(message, get_age)
    else:
        cursor.execute(f"SELECT user_surname FROM data WHERE user_id = {user_id}")
        print(cursor.fetchone())
        print(type(cursor.fetchone()))
        if cursor.fetchone() is None:
            cursor.execute(f"UPDATE data SET user_surname = ? WHERE user_id = ?", (surname, user_id))
            connect.commit()  # Сохранение изменений
        surname = ""
        await bot.send_message(message.from_user.id, "Сколько тебе лет?")
        await bot.register_next_step_handler(message, get_age)


async def get_age(message: types.Message):
    global user_age
    if edit == "yes":

        global edit_age
        edit_age = message.text
        cursor.execute(f"UPDATE data SET user_age = ? WHERE user_id = ?", (edit_age, user_id))
        connect.commit()
        edit_age = None
        await bot.send_message(message.from_user.id, "Данные успешно изменены")
        await bot.send_message(message.from_user.id, "Выберите действие, которое вы хотите сделать, с вашими данными")
        await dp.register_message_handler(message, result)
    else:

        user_age = message.text
        cursor.execute(f"SELECT user_age FROM data WHERE user_id = {user_id}")
        print(cursor.fetchone())
        if cursor.fetchone() is None:
            cursor.execute(f"UPDATE data SET user_age = ? WHERE user_id = ?", (user_age, user_id))
            connect.commit()  # Сохранение изменений
        user_age = 0

        # Извлечение данных из БД
        cursor.execute(f"SELECT * FROM data WHERE user_id={user_id}")
        db_data_2 = list(cursor.fetchone())
        question_name = db_data_2[1]
        question_surname = db_data_2[2]
        question_user_age = db_data_2[3]
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_yes = types.InlineKeyboardButton(text='✅Да', callback_data='yes')  # кнопка «Да»
        keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
        key_no = types.InlineKeyboardButton(text='❌Нет', callback_data='no')
        keyboard.add(key_no)
        question = 'Тебе ' + str(question_user_age) + ' лет, тебя зовут ' + str(question_name) + ' ' + str(
            question_surname) + '?'
        question_name = None
        question_surname = None
        question_user_age = None
        await bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@dp.callback_query_handler()
async def callback_worker(call: types.CallbackQuery):
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Ваш ответ: Да")
        await bot.send_message(call.message.chat.id, 'Запомню : )')
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        data_delete = types.KeyboardButton('🗑Удалить')
        data_edit = types.KeyboardButton('✍Изменить')
        user_exit = types.KeyboardButton('🔚Выйти')
        markup_reply.add(data_edit, data_delete, user_exit)
        await bot.send_message(call.message.chat.id, "Выберите действие, которое вы хотите сделать, с вашими данными",
                               reply_markup=markup_reply)
        await bot.register_next_step_handler(call.message, result)
    elif call.data == "no":
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Ваш ответ: Нет")
        reset()
        await bot.send_message(call.message.chat.id, 'Для повторной регистрации напишите /start')


async def result(message: types.Message):
    global name
    global surname
    global user_age
    if message.text == '🗑Удалить':
        await bot.send_message(message.from_user.id, "Началась процедура удаления данных...")

        cursor.execute(f"DELETE FROM data WHERE user_id = {user_id}")
        connect.commit()

        time.sleep(1.3)
        await bot.send_message(message.from_user.id, "Данные удалены")
    elif message.text == '✍Изменить':
        global edit
        edit = "yes"

        await bot.send_message(message.from_user.id, "Началась процедура переписывания данных...")
        time.sleep(1.3)
        await bot.send_message(message.from_user.id, "Запрос Данных у пользователя...")
        time.sleep(1.3)
        await bot.send_message(message.from_user.id, "Как тебя зовут?")
        await bot.register_next_step_handler(message, get_name)

    elif message.text == '🔚Выйти':
        await bot.send_message(message.from_user.id, "Начата процедура выхода...")
        time.sleep(1.3)
        await bot.send_message(message.from_user.id, "Вы успешно вышли")
        await bot.register_next_step_handler(message, start)
    else:
        await bot.send_message(message.from_user.id, 'Команда введена неверно')
        await bot.register_next_step_handler(message, result)


executor.start_polling(dp)
