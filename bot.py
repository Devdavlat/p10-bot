import telebot
from telebot import types
from environs import Env
from utils import WriteCSV
from datetime import datetime
from translate import to_latin, to_cyrillic

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['age'])
def get_age(message):
    msg = bot.reply_to(message, "Tug'ilgan yilingizni kiriting.")
    bot.register_next_step_handler(msg, get_age_func)


def get_age_func(message):
    current_year = int(datetime.now().strftime('%Y'))
    try:
        player_year = int(message.text)
    except Exception as e:
        bot.reply_to(message, "Iltimos tog'ilgan yilingizni to'g'ri kiriting")
    else:
        if player_year < current_year:
            text = f"Siz {current_year - player_year} yoshda siz."
            bot.reply_to(message, text)
        else:
            bot.reply_to(message, "Iltimos tog'ilgan yilingizni to'g'ri kiriting")


# /start
@bot.message_handler(commands=['start'])
def welcome_message(message):
    # msg = bot.reply_to(message, 'salom')
    # bot.register_next_step_handler(msg, process_name_step)

    # header = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # task_manager = types.InlineKeyboardButton(text='Task Manager')
    # weather = types.InlineKeyboardButton(text='Weather Info')
    # header.add(task_manager, weather)

    chat_id = message.from_user.id
    text = f"Assalomu alaykum p10 test botga xush kelibsiz.\n" \
           f"Quyidagi tugmalardan birini tanlang"
    bot.send_message(chat_id, text)


# /tasks
@bot.message_handler(commands=['list_of_tasks'])
def list_of_tasks(message):
    print('add task is working')
    user_id = message.from_user.id
    if not WriteCSV.check_user_from_tasks_list(user_id):
        bot.send_message(message.chat.id, f"Sizda hali tasklar ro'yxati shakllanmagan.\n/task tugmasini bosing")
    else:
        tasks_list = [i for i in enumerate(WriteCSV.read_tasks_by_user_id(user_id), 1)]
        for i in tasks_list:
            bot.send_message(user_id, str(i))


# /task
@bot.message_handler(commands=['task'])
def add_task(message):
    user_id = message.from_user.id
    doc = f"<b>Yo'riqnoma.</b>\n" \
          f"Har bir task yozish uchun /task ni boshqatdan ishga tushiring.\n" \
          f"Tasklar ro'yxatini ko'rish uchun /tasks ni ishga tushuring"
    bot.send_message(user_id, f"{doc}", parse_mode='HTML')
    bot.register_next_step_handler(message, make_data_for_write_csv)


def make_data_for_write_csv(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    task = message.text
    task_obj = WriteCSV(user_id, first_name, task)
    task_obj.write_csv()


# /latin_kiril
@bot.message_handler(commands=['latin_kiril'])
def latin_to_kiril(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Lotin harflaridan foydalaning.\nMasalan:Assalomu alaykum.')
    bot.register_next_step_handler(message, to_kiril)


def to_kiril(message):
    text = to_cyrillic(message.text)
    bot.reply_to(message, text)


@bot.message_handler(commands=['kiril_latin'])
def kiril_to_latin(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Кирил ҳарфларидан фойдаланинг.\нМасалан:Aссалому алайкум')
    bot.register_next_step_handler(message, to_latin_)


def to_latin_(message):
    text = to_latin(message.text)
    bot.reply_to(message, text)


# / /info
@bot.message_handler(commands=['info'])
def get_tasks(message):
    user_id = message.from_user.id
    user = message.from_user
    bot.send_message(user_id, f'<b>ID</b> : {str(user_id)}\n'
                              f'<b>First Name</b> : {str(user.first_name)}\n'
                              f'<b>Last Name</b> {str(user.last_name)}\n'
                              f'<b>Username</b> : @{str(user.username)}', parse_mode='HTML')


def my_commands():
    return [
        types.BotCommand('/start', 'start bot.'),
        types.BotCommand('/info', 'get may info.'),
        types.BotCommand('/list_of_tasks', 'list of tasks.'),
        types.BotCommand('/age', 'calculating age by birth year.'),
        types.BotCommand('/task', 'add task'),
        types.BotCommand('/latin_kiril', 'conversion from Latin to Cyrillic'),
        types.BotCommand('/kiril_latin', 'conversion from Cyrillic to Latin')
    ]


if __name__ == "__main__":
    print('run is working.')
    bot.set_my_commands(commands=my_commands())
    bot.infinity_polling()
