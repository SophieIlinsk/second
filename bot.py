from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup
from gpt import *
from functions import *
from SQL3 import *
from googletrans import Translator
from transformers import AutoTokenizer

bot = TeleBot(TOKEN)
MAX_LETTERS = MAX_TOKENS


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="log_file.txt",
    filemode="w",
)


 # приветливость
bot.message_handler(content_types=['text'])
def ansvers (message):
    if "прив" in message.text.lower():
        bot.reply_to(message,  text=f"приветики!")
    elif "пока" in message.text.lower():
        bot.reply_to(message,  text=f"пока-пока")
    elif "кто" and "ты" in message.text.lower():
        bot.reply_to(message,  text=f"ты можешь нажать на /menu и узнать кто я!")
    elif "как" and "дела" in message.text.lower():
        bot.reply_to(message, text=f"Спасибо, что спросил_а! Дела отлично!")


def create_keyboard(buttons_list): #Функция для создания клавиатуры с нужными кнопочками
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons_list)
    return keyboard

@bot.message_handler(commands=['start']) #Функция приветствия
def handler_start(message):
    logging.info("Отправка приветственного сообщения")
    start = say_hello(message)
    try:
        db_user = Database()
        if not db_user.check_user_exists(message.chat.id, message.chat.first_name):
            db_user.add_user(message.chat.id, message.chat.first_name)
            bot.send_message(message.chat.id, start, parse_mode='html',
                             reply_markup=create_keyboard(["Выбор с чем помочь📋", 'Выбор уровня🔋', '👤Профиль']))
        else:
            bot.send_message(message.chat.id, start, parse_mode='html',
                             reply_markup=create_keyboard(["Выбор с чем помочь📋", 'Выбор уровня🔋', '👤Профиль']))
            db_user.close()
    except Exception as e:
        bot.send_message(message.chat.id, error_4)
        logging.error(str(e))


@bot.message_handler(commands=['help'])
def support(message):
    logging.info("Отправка help сообщения")
    bot.send_message(message.from_user.id,
                     text=say_hello,
                     reply_markup=create_keyboard(["/solve_task"]))


@bot.message_handler(func=lambda message: message.text == "Выбор с чем помочь📋")
def subject_selection(message):
    bot.send_message(message.chat.id, 'У тебя есть выбор, с чем помочь, между: математикой, программированием, орфографией',
                     parse_mode='html', reply_markup=create_keyboard(["Математика", "Программирование", "Орфография"]))
    bot.register_next_step_handler(message, subject_selection2)

def subject_selection2(message):
    conn = sqlite3.connect('bot_users.db')
    user_id = message.from_user.id
    new_subject = message.text
    update_subject(conn, user_id, new_subject)
    conn.close()
    bot.reply_to(message, text=f" так и запишу, ты выбрал «{message.text}»")
    bot.send_message(message.chat.id, "что далее?", parse_mode='html',
                     reply_markup=create_keyboard(["Выбор уровня🔋", 'Задать вопрос gpt❓', '👤Профиль']))



@bot.message_handler(func=lambda message: message.text == "Выбор уровня🔋")
def level_selection(message):
    bot.send_message(message.chat.id, 'У тебя есть выбор уровней: Базовый, Экспертный',
                     parse_mode='html', reply_markup=create_keyboard(["Базовый", "Экспертный"]))
    bot.register_next_step_handler(message, level_selection2)

def level_selection2(message):
    conn = sqlite3.connect('bot_users.db')
    user_id = message.from_user.id
    new_subject = message.text
    update_subject(conn, user_id, new_subject)
    conn.close()
    bot.reply_to(message, text=f" так и запишу, ты выбрал «{message.text}»")
    bot.send_message(message.chat.id, "что далее?", parse_mode='html',
                     reply_markup=create_keyboard(["Выбор с чем помочь📋", 'Задать вопрос gpt❓', '👤Профиль']))


@bot.message_handler(func=lambda message: message.text == 'Задать вопрос❓')
def promt_message(message):
    try:
        promt = message.text
        bot.send_message(message.chat.id, '<b>Напиши свой вопрос:</b>',
                           parse_mode='html', reply_markup=create_keyboard(["Нажми Продолжить✏️"]))

        def promt_user(message):
            tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
            if len(tokenizer.encode(message.text)) > MAX_TOKENS:
                bot.send_message(message.chat.id, "Текст задачи слишком длинный. Пожалуйста, попробуй его укоротить.")
                logging.info(f"TELEGRAM BOT: Input: {message.text}\nOutput: Текст задачи слишком длинный")
                return
            message1 = bot.send_message(message.chat.id, '<b>Генерирую ответ...⏳</b>', parse_mode='html')
            user_id = message.chat.id
            system_content = promt_db(promt, user_id)
            translator = Translator()
            result1 = translator.translate(f'{promt}', src='ru', dest='en')
            g = Question_gpt2()
            n1 = g.promt(result1, system_content)
            result = translator.translate(f'{n1}', src='en', dest='ru')
            add = promt_add(n1, user_id, result)
            bot.edit_message_text(chat_id=message.chat.id, message_id=message1.message_id, text=
            add, parse_mode='html')
            bot.send_message(message.chat.id,'Нажми Продолжить✏️\n'
                                                'если нужны еще подробности.',
                             reply_markup=create_keyboard(["Нажми Продолжить✏️"]))
            Quantity(user_id)
        bot.register_next_step_handler(message, promt_user)
    except Exception as e:
        bot.send_message(message.chat.id, error_4)
        logging.error(str(e))


@bot.message_handler(func=lambda message: message.text == 'Продолжить✏️')
def promt_continue(message):
    try:
        user_id = message.from_user.id
        promt1 = Continue(user_id)
        if not promt1:
            bot.send_message(message.chat.id, error_2, parse_mode='html')
            return
        if len(promt1) >= 1000:
            bot.send_message(message.chat.id, error_1, parse_mode='html')
            return

        message2 = bot.send_message(message.chat.id, '<b>Генерирую продолжение...⏳</b>', parse_mode='html')
        user_id = message.chat.id
        system_content = contine_db(user_id)
        n = Continue_text_gpt()
        n1 = n.gpt(promt1,system_content)
        translator = Translator()
        result = translator.translate(f'{n1}', src='en', dest='ru')
        r = promt1 + n1
        user_id = message.chat.id
        add_contine_promt(r, user_id)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message2.message_id, text=f'{result.text}')

    except Exception as e:
        bot.send_message(message.chat.id, error_4)
        logging.error(str(e))




@bot.message_handler(func=lambda message: message.text == '👤Профиль')
def house(message):
    user_id = message.chat.id
    info1 = info_db(user_id, message.chat.first_name)
    bot.send_message(message.chat.id, info1, parse_mode='html')



@bot.message_handler(commands=['debug'])
def send_logs(message):
    with open("log_file.txt", "rb") as f:
        bot.send_document(message.chat.id, f)

bot.polling()
