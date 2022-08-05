import time
import mysql.connector
from private_variables import BOT_TOKEN
from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from strings import *
from random import choice

mydb = mysql.connector.connect(
    host="localhost",
    user="laziz",
    passwd="P@ssW0rd",
    database='telegram_bot'
)
board = {
    1: '⬜', 2: '⬜', 3: '⬜',
    4: '⬜', 5: '⬜', 6: '⬜',
    7: '⬜', 8: '⬜', 9: '⬜'}
mycursor = mydb.cursor()
bot = TeleBot(BOT_TOKEN)
player = None
computer = None
game_running = True
user_ = None
user_id = None
chat_id = None
lang_ = None
difficulty_ = None
random_ = False
temp_message = None
temp_markup = None
temp_text = None
compMove = None

available_languages = ['uz', 'en', 'ru']


# ==========database methods==========
def initialize_user(tg_user) -> None:
    global user_id, compMove
    user_id = tg_user.id
    if is_user_exist(user_id):
        exist_user()
    else:
        new_user(tg_user)
    comp_move_difficulty('easy')



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
    global user_, stats_, difficulty_
    difficulty_ = 'easy'
    user_ = {'id': u.id,
             'username': u.username,
             'first_name': u.first_name,
             'language': u.language_code if u.language_code in available_languages else 'en',
             'difficulty': difficulty_}
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
    stats_db.update({'easy': [_[0], _[1], _[2]]})
    mycursor.execute(f'SELECT win, draw, loose FROM medium WHERE id = {user_id}')
    _ = mycursor.fetchall()[0]
    stats_db.update({'medium': [_[0], _[1], _[2]]})
    mycursor.execute(f'SELECT win, draw, loose FROM hard WHERE id = {user_id}')
    _ = mycursor.fetchall()[0]
    stats_db.update({'hard': [_[0], _[1], _[2]]})
    change_stats()


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
def comp_move_difficulty(diff):
    global compMove
    if diff == 'easy':
        compMove = Easy.compMove
    elif diff == 'medium':
        compMove = Medium.compMove
    else:
        compMove = Hard.compMove


def send_board():
    global temp_message, temp_text
    temp_text = f"{difficulty_btn[lang_][difficulty_]}\n{board_txt[lang_] + player}"
    temp_message = bot.edit_message_text(
        message_id=temp_message.id,
        chat_id=chat_id,
        text=temp_text,
        reply_markup=board_markup())


def send_help():
    global temp_message, temp_text
    temp_text = help_txt[lang_]
    temp_message = bot.send_message(
        chat_id=chat_id,
        text=temp_text,
        reply_markup=help_markup(),
        parse_mode='markdown')



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
# =================================================


# ==========markup methods==========
def update_board_markup(message):
    global temp_message
    temp_message = bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=message.id,
        reply_markup=board_markup())


def choose_letter_markup():
    global temp_markup
    menu = InlineKeyboardMarkup(row_width=2)
    menu.add(InlineKeyboardButton(text='❌', callback_data='❌'),
             InlineKeyboardButton(text='⭕️', callback_data='⭕️'))
    temp_markup = menu
    return menu


def board_markup():
    global temp_markup
    menu = InlineKeyboardMarkup(row_width=3)
    menu.add(InlineKeyboardButton(text=board[1], callback_data='1'),
             InlineKeyboardButton(text=board[2], callback_data='2'),
             InlineKeyboardButton(text=board[3], callback_data='3'),
             InlineKeyboardButton(text=board[4], callback_data='4'),
             InlineKeyboardButton(text=board[5], callback_data='5'),
             InlineKeyboardButton(text=board[6], callback_data='6'),
             InlineKeyboardButton(text=board[7], callback_data='7'),
             InlineKeyboardButton(text=board[8], callback_data='8'),
             InlineKeyboardButton(text=board[9], callback_data='9'))
    temp_markup = menu
    return menu


def difficulty_markup():
    global temp_markup
    menu = InlineKeyboardMarkup(row_width=1)
    menu.add(InlineKeyboardButton(text=difficulty_btn[lang_]['easy'], callback_data='easy'),
             InlineKeyboardButton(text=difficulty_btn[lang_]['medium'], callback_data='medium'),
             InlineKeyboardButton(text=difficulty_btn[lang_]['hard'], callback_data='hard'), )
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
    menu.add(InlineKeyboardButton(text=pwb_btn[lang_], callback_data='pwb'),
             InlineKeyboardButton(text=pwf_btn[lang_], callback_data='pwf'),
             InlineKeyboardButton(text=diff_btn[lang_], callback_data='diff'),
             InlineKeyboardButton(text=lang_btn[lang_], callback_data='lang'),
             InlineKeyboardButton(text=stats_btn[lang_], callback_data='stats'))
    temp_markup = menu
    return menu


def stats_markup():
    global temp_markup
    menu = InlineKeyboardMarkup(row_width=1)
    menu.add(InlineKeyboardButton(text=pwb_btn[lang_], callback_data='pwb'),
             InlineKeyboardButton(text=pwf_btn[lang_], callback_data='pwf'),
             InlineKeyboardButton(text=diff_btn[lang_], callback_data='diff'),
             InlineKeyboardButton(text=lang_btn[lang_], callback_data='lang'),
             InlineKeyboardButton(text=help_btn[lang_], callback_data='help'))

    temp_markup = menu
    return menu
# =================================================


# ==========Tic-tac-toe logic==========
class Easy:
    @staticmethod
    def compMove():
        rand_turn = choice(list(board.keys()))
        while not is_space_empty(rand_turn):
            rand_turn = choice(list(board.keys()))
        insertLetter(computer, rand_turn)



class Hard:
    @staticmethod
    def compMove():
        bestScore = -800
        bestMove = 0
        for key in board.keys():
            if board[key] == '⬜':
                board[key] = computer
                score = minimax(board, False)
                board[key] = '⬜'
                if score > bestScore:
                    bestScore = score
                    bestMove = key
        insertLetter(computer, bestMove)


class Medium(Hard, Easy):
    @staticmethod
    def compMove():

        global random_
        if not random_:
            Hard.compMove()
        else:
            Easy.compMove()
        random_ = not random_


def minimax(board, isMaximizing):
    if check_win(computer):
        return 1
    elif check_win(player):
        return -1
    elif checkDraw():
        return 0
    if isMaximizing:
        bestScore = -800
        for key in board.keys():
            if board[key] == '⬜':
                board[key] = computer
                score = minimax(board, False)
                board[key] = '⬜'
                if score > bestScore:
                    bestScore = score
        return bestScore
    else:
        bestScore = 800
        for key in board.keys():
            if board[key] == '⬜':
                board[key] = player
                score = minimax(board, True)
                board[key] = '⬜'
                if score < bestScore:
                    bestScore = score
        return bestScore


def is_space_empty(key):
    return board[key] == '⬜'


def insertLetter(letter, position):
    board[position] = letter
    update_board_markup(temp_message)

    if check_win(letter):
        send_result(letter=letter)
    elif checkDraw():
        send_result(draw=True)



def check_win(mark):
    if board[1] == board[2] and board[1] == board[3] and board[1] == mark:
        return True
    elif board[4] == board[5] and board[4] == board[6] and board[4] == mark:
        return True
    elif board[7] == board[8] and board[7] == board[9] and board[7] == mark:
        return True
    elif board[1] == board[4] and board[1] == board[7] and board[1] == mark:
        return True
    elif board[2] == board[5] and board[2] == board[8] and board[2] == mark:
        return True
    elif board[3] == board[6] and board[3] == board[9] and board[3] == mark:
        return True
    elif board[1] == board[5] and board[1] == board[9] and board[1] == mark:
        return True
    elif board[7] == board[5] and board[7] == board[3] and board[7] == mark:
        return True
    else:
        return False


def send_result(letter=None, draw=False):
    global temp_message, game_running
    game_running = False
    text = ""

    if draw:
        text = result_txt[lang_]['draw']
        update_result('draw')
    else:
        if computer == letter:
            text = result_txt[lang_]['loose']
            update_result('loose')
        else:
            text = result_txt[lang_]['win']
            update_result('win')

    bot.edit_message_text(
        chat_id=temp_message.chat.id,
        message_id=temp_message.id,
        text=f"{difficulty_btn[lang_][difficulty_]}\n\n{board[1] + board[2] + board[3]}\n{board[4] + board[5] + board[6]}\n{board[7] + board[8] + board[9]}\n\n{text} ")

    clear_board()
    temp_message = None
    stats_menu(0)

def checkDraw():
    for key in board.keys():
        if board[key] == '⬜':
            return False
    return True


def clear_board():
    for key in board.keys():
        board[key] = '⬜'


def randomMove():
    rand_turn = choice(board.keys())
    if is_space_empty(rand_turn):
        insertLetter(computer, choice(board.keys()))

# =================================================


# ==========telegram methods==========
#primary_method
@bot.callback_query_handler(func=lambda call: call.data == 'pwb')
def play_with_bot(call):
    global temp_message, temp_text
    temp_text = difficulty_btn[lang_][difficulty_] + choose_letter_txt[lang_]
    temp_message = bot.edit_message_text(
        text=temp_text,
        chat_id=temp_message.chat.id,
        message_id=temp_message.id,
        reply_markup=choose_letter_markup())


@bot.callback_query_handler(func=lambda call: call.data in ['❌', '⭕️'])
def assign_letters(call):
    global player, computer, game_running, random_, compMove
    game_running = True

    if call.data == '❌':
        player, computer = '❌', '⭕️'
        random_ = True
    else:
        computer, player = '❌', '⭕️'
        compMove()
        comp_move_difficulty(difficulty_)
    send_board()


@bot.callback_query_handler(func=lambda call: call.data in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] and call.message.id == temp_message.id)
def update_board(call):
    key = int(call.data)
    if is_space_empty(key):
        insertLetter(player, key)
        if game_running:
            compMove()
    else:
        bot.answer_callback_query(call.id, text=not_empty_txt[lang_], show_alert=True)


#primary_method
@bot.callback_query_handler(func=lambda call: call.data == 'diff')
def difficulty(call):
    global temp_message, temp_text
    temp_text = difficulty_txt[lang_] + difficulty_btn[lang_][difficulty_]
    temp_message = bot.edit_message_text(
        text=temp_text,
        chat_id=temp_message.chat.id,
        message_id=temp_message.id,
        reply_markup=difficulty_markup(),
        parse_mode='markdown'
    )


@bot.callback_query_handler(func=lambda call: call.data in ['easy', 'medium', 'hard'])
def change_difficulty(call):
    global difficulty_, compMove
    difficulty_ = call.data
    comp_move_difficulty(difficulty_)
    update_difficulty(difficulty_)
    stats_menu(0)


#primary_method
@bot.callback_query_handler(func=lambda call: call.data == 'lang')
def language(call):
    global temp_message, temp_text
    temp_text = lang_text[lang_]
    temp_message = bot.edit_message_text(
        chat_id=temp_message.chat.id,
        message_id=temp_message.id,
        text=temp_text,
        reply_markup=language_markup())



@bot.callback_query_handler(func=lambda call: call.data in ['uz', 'en', 'ru'])
def change_lang(call):
    update_language(call.data)
    help_menu(0)


#primary_method
@bot.callback_query_handler(func=lambda call: call.data == 'stats')
def stats_menu(call):
    global temp_message, temp_text
    temp_text = stats_txt[lang_]
    if temp_message is None:
        temp_message = bot.send_message(
            chat_id=chat_id,
            text="    " + temp_text,
            reply_markup=stats_markup(),
            parse_mode='HTML')
    else:
        temp_message = bot.edit_message_text(
            chat_id=temp_message.chat.id,
            message_id=temp_message.id,
            text="    " + temp_text,
            reply_markup=stats_markup(),
            parse_mode='HTML')


#primary_method
@bot.callback_query_handler(func=lambda call: call.data == 'help')
def help_menu(call):
    global temp_message, temp_text
    temp_text = help_txt[lang_]
    temp_message = bot.edit_message_text(
        chat_id=temp_message.chat.id,
        message_id=temp_message.id,
        text=temp_text,
        reply_markup=help_markup(),
        parse_mode='markdown')


@bot.message_handler(func=lambda message: True)
def send_message(message):
    global chat_id
    chat_id = message.chat.id
    if user_ is None:
        initialize_user(message.from_user)

    if temp_message is None:
        send_help()
    else:
        wrong_message()
# =================================================


bot.infinity_polling()
