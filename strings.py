stats_db = {}
a = 9
pwb_btn = {'en': '❌ Play with bot 🤖', 'uz': "❌ Bot bilan o'ynash 🤖", 'ru': "❌ Играть с ботом 🤖"}
choose_letter_txt = {'en': '\nChoose your side:', 'uz': '\nBelgini tanlang:', 'ru': '\nВыбери свою сторону:'}

board_txt = {'en': 'You are playing as ', 'uz': 'Sizning belgingiz ', 'ru': 'Вы играете как '}
pwf_btn = {'en': '👥 Play with friend ⭕', 'uz': "👥 Do'stingiz bilan o'ynash ⭕", 'ru': "👥 Играй с другом ⭕"}

diff_btn = {'en': '👶 Difficulty 😈', 'uz': '👶 Qiyinchilik 😈', 'ru': '👶 Сложность 😈'}
difficulty_txt = {'en': "Choose difficulty\n\nCurrent difficulty:",
                  'uz': "Qiyinlikni tanlang\n\nHozirgi qiyinlik",
                  'ru': "Выберите сложность\n\nТекущая сложность:"}

difficulty_btn = {'en': {'easy': '🐣 Easy 👶', 'medium': '👩 Medium 👱', 'hard': '💀 Hard 😈'},
                  'uz': {'easy': '🐣 Oson 👶', 'medium': "👩 O'rtacha 👱", 'hard': '💀 Qiyin 😈'},
                  'ru': {'easy': '🐣 Легкий 👶', 'medium': '👩 Средний 👱', 'hard': '💀 Сложный 😈'}}

not_empty_txt = {'en': '🚫 This spot is not empty 🚫', 'uz': "🚫 Bu joy bo'sh emas 🚫", 'ru': '🚫 Это место не пусто 🚫'}
result_txt = {'en':
                  {'win': "🏆 You won! 🏆", 'loose': "😭 You lost! 😭", 'draw': "⚖️ Draw! ⚖️"},
              'uz':
                  {'win': "🏆 Siz yutdingiz! 🏆", 'loose': "😭 Siz yutqazdingiz! 😭", 'draw': "⚖️ Durang! ⚖️"},
              'ru':
                  {'win': "🏆 Вы выиграл! 🏆", 'loose': "😭 Вы проиграл! 😭", 'draw': "⚖️ Ничья! ⚖️"}, }

lang_btn = {'en': '🇺🇿 Language 🇺🇿', 'uz': '🇺🇿 Til 🇺🇿', 'ru': '🇺🇿 Язык 🇺🇿'}
lang_text = {'en': 'Choose language', 'uz': "Tilni tanlang", 'ru': 'Выберите язык'}

stats_btn = {'en': '🆔 Stats 📊 ', 'uz': '🆔 Statistika 📊 ', 'ru': '🆔 Статистика 📊'}
stats_txt = {}

help_btn = {'en': 'ℹ️ Help ℹ️', 'uz': 'ℹ️ Yordam ℹ️', 'ru': 'ℹ️ Помощь ℹ️'}
help_txt = {'en': """<b>Controls</b>
Interact with the bot only via a received keyboard.

<b>How-to play</b>
During a game you will get a keyboard with buttons which represent board squares. Press ⬜️ to make turn.

<b>Multiplayer</b>
After 5 minutes the game will become expired and the message will be replaced by ⌛️

<b>About</b>
We don't store chat history, so if you have questions or comments text me @lazizkhan1""", 'uz': """<b>O'ynash</b>
Bot bilan faqat berilgan klaviaturada ishlatishingiz mumkin.

<b>Qanday o'ynash</b>
O'yin paytida sizga katakchalarga mos tugmachalar beriladi. Yurish uchun ⬜️ tugmasini bosing.

<b>Multiplyer</b>
Agar o'yin 5-minut ichida tugamasa o'yin o'chiriladi, xabarlar esa boshqaga almashtirildi.

<b>Bot haqida</b>
Biz yozilgan xabarlarni saqlamaymiz, agar savolingiz bo'lsa menga yozing @lazizkhan1

""", 'ru': """<b>Управление</b>
Взаимодействуйте с ботом только через полученную клавиатуру.

<b>Как играть</b>
Во время игры вы получите клавиатуру с кнопками, которые представляют собой квадраты доски. Нажмите ⬜️, чтобы повернуть.

<b>Мультиплеер</b>
Через 5 минут срок действия игры истечет, а сообщение будет заменено на ⌛️

<b>О боте</b>
Мы не храним историю чатов, поэтому, если у вас есть вопросы или комментарии, напишите мне @lazizkhan1"""}


def change_stats() -> dict:
    global stats_txt
    stats_txt.update({
        'en': """
<code>       Stats

     🏆     ⚖️     😭
👶:{:>4}{:>4}{:>4}
👱:{:>4}{:>4}{:>4}
😈:{:>4}{:>4}{:>4}</code>
""".format(stats_db['easy'][0], stats_db['easy'][1], stats_db['easy'][2],
       stats_db['medium'][0], stats_db['medium'][1], stats_db['medium'][2],
       stats_db['hard'][0], stats_db['hard'][1], stats_db['hard'][2]),

        'uz': """
<code>       Statistika

     🏆     ⚖️     😭
👶:{:>4}{:>4}{:>4}
👱:{:>4}{:>4}{:>4}
😈:{:>4}{:>4}{:>4}</code>
""".format(stats_db['easy'][0], stats_db['easy'][1], stats_db['easy'][2],
       stats_db['medium'][0], stats_db['medium'][1], stats_db['medium'][2],
       stats_db['hard'][0], stats_db['hard'][1], stats_db['hard'][2]),

        'ru': """
<code>       Статистка

     🏆     ⚖️     😭
👶:{:>4}{:>4}{:>4}
👱:{:>4}{:>4}{:>4}
😈:{:>4}{:>4}{:>4}</code>
""".format(stats_db['easy'][0], stats_db['easy'][1], stats_db['easy'][2],
       stats_db['medium'][0], stats_db['medium'][1], stats_db['medium'][2],
       stats_db['hard'][0], stats_db['hard'][1], stats_db['hard'][2])})
