stats_db = {}
a = 9
pwb = {'en': '❌ Play with bot 🤖', 'uz': "❌ Bot bilan o'ynash 🤖", 'ru': "❌ Играть с ботом 🤖"}

pwf = {'en': '👥 Play with friend ⭕', 'uz': "👥 Do'stingiz bilan o'ynash ⭕", 'ru': "👥 Играй с другом ⭕"}

diff = {'en': '👶 Difficulty 😈', 'uz': '👶 Qiyinchilik 😈', 'ru': '👶 Сложность 😈'}
difficulty_text = {'en': "Choose difficulty\n\n*Current difficulty:*",
                   'uz': "Qiyinlikni tanlang\n\n*Hozirgi qiyinlik*",
                   'ru': "Выберите сложность\n\n*Текущая сложность:*"}

diff_btn = {'en': {'easy': '👶 Easy 👶', 'medium': '👱 Medium 👱', 'hard': '😈 Hard 😈'},
            'uz': {'easy': '👶 Oson 👶', 'medium': "👱 O'rtacha 👱", 'hard': '😈 Qiyin 😈'},
            'ru': {'easy': '👶 Легкий 👶', 'medium': '👱 Средний 👱', 'hard': '😈 Сложный 😈'}}


lang = {'en': '🇺🇿 Language 🇺🇿', 'uz': '🇺🇿 Til 🇺🇿', 'ru': '🇺🇿 Язык 🇺🇿'}
lang_text = {'en': 'Choose language', 'uz': "Tilni tanlang", 'ru': 'Выберите язык'}

stats__ = {'en': '🆔 Stats 📊 ', 'uz': '🆔 Statistika 📊 ', 'ru': '🆔 Статистика 📊'}
stats_txt = {}

help__ = {'en': 'ℹ️ Help ℹ️', 'uz': 'ℹ️ Yordam ℹ️', 'ru': 'ℹ️ Помощь ℹ️'}
help_txt = {'en': """*Controls*
Interact with the bot only via a received keyboard.

*How-to play*
During a game you will get a keyboard with buttons which represent board squares. Press ⬜️ to make turn.

*Multiplayer*
After 5 minutes the game will become expired and the message will be replaced by ⌛️

*About*
We don't store chat history, so if you have questions or comments text me @lazizkhan1""", 'uz': """*O'ynash*
Bot bilan faqat berilgan klaviaturada ishlatishingiz mumkin.

*Qanday o'ynash*
O'yin paytida sizga katakchalarga mos tugmachalar beriladi. Yurish uchun ⬜️ tugmasini bosing.

*Multiplyer*
Agar o'yin 5-minut ichida tugamasa o'yin o'chiriladi, xabarlar esa boshqaga almashtirildi.

*Bot haqida*
Biz yozilgan xabarlarni saqlamaymiz, agar savolingiz bo'lsa menga yozing @lazizkhan1

""", 'ru': """*Управление*
Взаимодействуйте с ботом только через полученную клавиатуру.

*Как играть*
Во время игры вы получите клавиатуру с кнопками, которые представляют собой квадраты доски. Нажмите ⬜️, чтобы повернуть.

*Мультиплеер*
Через 5 минут срок действия игры истечет, а сообщение будет заменено на ⌛️

*О боте*
Мы не храним историю чатов, поэтому, если у вас есть вопросы или комментарии, напишите мне @lazizkhan1"""}


def change_stats() -> dict:
    global stats_txt
    stats_txt.update({
    'en':  """
        Stats
      🏆     ⚖️     😭
👶: %s        %s        %s
👱: %s        %s        %s
😈: %s        %s        %s
""" % (stats_db['easy'][0], stats_db['easy'][1], stats_db['easy'][2],
       stats_db['medium'][0], stats_db['medium'][1], stats_db['medium'][2],
       stats_db['hard'][0], stats_db['hard'][1], stats_db['hard'][2]),

    'uz':  """
        Statistika
      🏆     ⚖️     😭
👶: %s        %s        %s
👱: %s        %s        %s
😈: %s        %s        %s
""" % (stats_db['easy'][0], stats_db['easy'][1], stats_db['easy'][2],
       stats_db['medium'][0], stats_db['medium'][1], stats_db['medium'][2],
       stats_db['hard'][0], stats_db['hard'][1], stats_db['hard'][2]),

'ru':  """
        Статистка
      🏆     ⚖️     😭
👶: %s        %s        %s
👱: %s        %s        %s
😈: %s        %s        %s
""" % (stats_db['easy'][0], stats_db['easy'][1], stats_db['easy'][2],
       stats_db['medium'][0], stats_db['medium'][1], stats_db['medium'][2],
       stats_db['hard'][0], stats_db['hard'][1], stats_db['hard'][2]),


})

