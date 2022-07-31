import time
import mysql.connector
from private_variables import BOT_TOKEN
from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from strings import *

mydb = mysql.connector.connect(
    host="localhost",
    user="laziz",
    passwd="P@ssW0rd",
    database='telegram_bot'
)
mycursor = mydb.cursor()
bot = TeleBot(BOT_TOKEN)
user_ = None
user_id = None
lang_ = None
difficulty_ = None
temp_message = None
temp_markup = None
temp_text = None

available_languages = ['uz', 'en', 'ru']


# ==========database methods==========
def initialize_user(tg_user) -> None:
    global user_id
    user_id = tg_user.id
    if is_user_exist(user_id):
        exist_user()
    else:
        new_user(tg_user)


def exist_user() -> None:
    global user_, lang_, difficulty_
    mycursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    u = mycursor.fetchall()[0]
    user_ = {'id': u[0],
             'username': u[1],
             'first_name': u[2],
             'language': u[3],
             'difficulty': u[4]}
    lang_ = user_['language']
    difficulty_ = user_['difficulty']
    update_stats()


def new_user(u) -> None:
    global user_, stats_
    user_ = {'id': u.id,
             'username': u.username,
             'first_name': u.first_name,
             'language': u.language_code if u.language_code in available_languages else 'en',
             'difficulty': 'easy'}
    stats_db.update({'easy': [0, 0, 0],
                     'medium': [0, 0, 0],
                     'hard': [0, 0, 0]})
    mycursor.execute(
            """
    INSERT INTO users VALUES(%d, "%s", "%s", "%s", "%s")"""
            % (user_['id'], user_['username'], user_['first_name'],
                user_['language'], user_['difficulty']))
    mycursor.execute(f"INSERT INTO easy VALUES({user_}, 0, 0, 0)")
    mycursor.execute(f"INSERT INTO medium VALUES({user_}, 0, 0, 0)")
    mycursor.execute(f"INSERT INTO hard VALUES({user_}, 0, 0, 0)")
    mydb.commit()


def update_stats() -> None:
    mycursor.execute(f'SELECT win, draw, loose draw FROM easy WHERE id = {user_id}')
    _ = mycursor.fetchall()[0]
    print(_)
    stats_db.update({'easy': [_[0], _[1], _[2]]})
    mycursor.execute(f'SELECT win, draw, loose FROM medium WHERE id = {user_id}')
    _ = mycursor.fetchall()[0]
    print(_)
    stats_db.update({'medium': [_[0], _[1], _[2]]})
    mycursor.execute(f'SELECT win, draw, loose FROM hard WHERE id = {user_id}')
    _ = mycursor.fetchall()[0]
    print(_)
    stats_db.update({'hard': [_[0], _[1], _[2]]})
    change_stats()
    print(stats_txt[lang_])


def update_language(lng: str) -> None:
    global lang_
    mycursor.execute(f"UPDATE users SET language = '{lng}' WHERE id = {user_id}")
    mydb.commit()
    lang_ = lng


def update_difficulty(diff_) -> None:
    global difficulty_
    mycursor.execute(f"UPDATE users SET difficulty = '{diff_}' WHERE id = {user_id}")
    mydb.commit()
    difficulty_ = diff_


def update_result(result: str) -> None:
    mycursor.execute(f"UPDATE {difficulty_} SET {result} = {result} + 1 WHERE id = {user_id}")
    mydb.commit()
    update_stats()


def is_user_exist(id: int) -> bool:
    mycursor.execute(f'SELECT * FROM users where id = {id}')
    return bool(mycursor.fetchall())
# =================================================


# ==========static methods==========


def send_help(message):
    global temp_message, temp_text
    temp_message = bot.send_message(
        chat_id=message.chat.id,
        text=help_txt[lang_],
        reply_markup=help_markup(),
        parse_mode='markdown')
    temp_text = help_txt[lang_]


def wrong_message():
    global temp_message, temp_markup, temp_text
    bot.edit_message_text(
        text='↩️',
        chat_id=temp_message.chat.id,
        message_id=temp_message.id)

    temp_message = bot.send_message(
        chat_id=temp_message.chat.id,
        text=temp_text,
        reply_markup=temp_markup,
        parse_mode='markdown')


def difficulty_markup():
    global temp_markup
    menu = InlineKeyboardMarkup(row_width=1)
    menu.add(InlineKeyboardButton(text=diff_btn[lang_]['easy'], callback_data='easy'),
             InlineKeyboardButton(text=diff_btn[lang_]['medium'], callback_data='medium'),
             InlineKeyboardButton(text=diff_btn[lang_]['hard'], callback_data='hard'), )
    temp_markup = menu
    return menu


def language_markup():
    global temp_markup
    menu = InlineKeyboardMarkup(row_width=2)
    menu.add(InlineKeyboardButton(text='🇺🇿', callback_data='uz'),
             InlineKeyboardButton(text='🇺🇸 / 🇬🇧', callback_data='en'),
             InlineKeyboardButton(text='🇷🇺', callback_data='ru'))
    temp_markup = menu
    return menu


def help_markup():
    global temp_markup
    menu = InlineKeyboardMarkup(row_width=1)
    menu.add(InlineKeyboardButton(text=pwb[lang_], callback_data='pwb'),
             InlineKeyboardButton(text=pwf[lang_], callback_data='pwf'),
             InlineKeyboardButton(text=diff[lang_], callback_data='diff'),
             InlineKeyboardButton(text=lang[lang_], callback_data='lang'),
             InlineKeyboardButton(text=stats__[lang_], callback_data='stats'))
    temp_markup = menu
    return menu


def stats_markup():
    global temp_markup
    menu = InlineKeyboardMarkup(row_width=1)
    menu.add(InlineKeyboardButton(text=pwb[lang_], callback_data='pwb'),
             InlineKeyboardButton(text=pwf[lang_], callback_data='pwf'),
             InlineKeyboardButton(text=diff[lang_], callback_data='diff'),
             InlineKeyboardButton(text=lang[lang_], callback_data='lang'),
             InlineKeyboardButton(text=help__[lang_], callback_data='help'))

    temp_markup = menu
    return menu
# =================================================


# ==========telegram methods==========
@bot.callback_query_handler(func=lambda call: call.data == 'diff')
def difficulty(call):
    global temp_message, temp_text
    temp_message = bot.edit_message_text(
        text=difficulty_text[lang_] + diff_btn[lang_][difficulty_],
        chat_id=temp_message.chat.id,
        message_id=temp_message.id,
        reply_markup=difficulty_markup(),
        parse_mode='markdown'
    )
    temp_text = difficulty_text[lang_] + diff_btn[lang_][difficulty_]


@bot.callback_query_handler(func=lambda call: call.data in ['easy', 'medium', 'hard'])
def change_difficulty(call):
    global difficulty_
    difficulty_ = call.data
    update_difficulty(call.data)
    stats_menu(0)


@bot.callback_query_handler(func=lambda call: call.data == 'lang')
def language(call):
    global temp_message, temp_text
    temp_message = bot.edit_message_text(
        chat_id=temp_message.chat.id,
        message_id=temp_message.id,
        text=lang_text[lang_],
        reply_markup=language_markup())
    temp_text = lang_text[lang_]


@bot.callback_query_handler(func=lambda call: call.data in ['uz', 'en', 'ru'])
def change_lang(call):
    update_language(call.data)
    help_menu(0)


@bot.callback_query_handler(func=lambda call: call.data == 'stats')
def stats_menu(call):
    global temp_message, temp_text
    temp_message = bot.edit_message_text(
        chat_id=temp_message.chat.id,
        message_id=temp_message.id,
        text=stats_txt[lang_],
        reply_markup=stats_markup())
    temp_text = stats_txt[lang_]


@bot.callback_query_handler(func=lambda call: call.data == 'help')
def help_menu(call):
    global temp_message, temp_text
    temp_message = bot.edit_message_text(
        chat_id=temp_message.chat.id,
        message_id=temp_message.id,
        text=help_txt[lang_],
        reply_markup=help_markup(),
        parse_mode='markdown')
    temp_text = help_txt[lang_]



@bot.message_handler(func=lambda message: True)
def send_message(message):

    if user_ is None:
        initialize_user(message.from_user)

    if temp_message is None:
        send_help(message)
    else:
        wrong_message()
# =================================================


bot.infinity_polling()
