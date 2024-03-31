import logging
from telebot import types

def system(sub, lev):
    system_content = (f"Вы преподаватель по предмету: {sub}, вам нужно объяснить вопросы, которые пользователь будет задавать максимально информативно на русском языке. пользователь имеет определенный уровень знаний: {lev}")
    return system_content


#функции бля текста:
def say_hello(message):
    text = (f'<b>Привет {message.chat.first_name}👋,\n</b>'
            'Я бот-мультипомощник и я могу помочь с такими предметами как: математика, программирование, орфография\n'
            'как и новичку так и профи.\n'
            'введи /menu чтобы узнать что-то')
    return text

def Profile(message, sub, lev, req):
    info = ('<b>Твой профиль👤\n\n</b>'
              f'<b>Имя:</b> {message.chat.first_name}\n'
              f'<b>Предмет:</b> {sub}\n'
              f'<b>Уровень:</b> {lev}\n'
              f'<b>Кол-запросов:</b> {req}\n'
              '<b>Примечание: \n</b>'
              '<i>Если вы не настроите GPT\n'
              'под себя, ваши настройки \n'
              'по умолчанию будут</i> <b>"математика\n'
              'с базовым уровнем"</b>.')
    return info

def answer(question1, result):
    answer1 = ('<b>Твой вопрос: \n</b>'
                f'<i>{question1}</i>\n'
                f'<b>Ответ:\n</b>'
                f'<i>{result.text}</i>')
    return answer1

#всевозможные ошибки:

logging.basicConfig(filename='errors.cod.log', level=logging.ERROR, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def error_gpt(resp, data):
    if resp.status_code < 200 or resp.status_code >= 300:
        error = 'Произошла ошибка'
        logging.error(str(resp.status_code))
        return error
    if 'error' in data:
        error0 = 'Произошла ошибка на стороне сервера.'
        logging.error(str(f'{data["error"]}'))
        return error0

error_1 = ('<b>Состояние: Превышено\n'
          'количество символов❗️️️️️️️️️️️</b>\n'
          '<i>Пожалуйста задайте новый\n'
          'вопрос, это обнулит ваш\n'
          'предыдущий диалог.</i>') #error

error_2 = ('<b>Состояние: Нет вопроса❗️</b>\n'
          '<i>Вы не можете продолжить\n'
          'ответ, так как вы не задали\n'
          'вопрос который нужно\n'
          'продолжить.😢</i>') #error1

error_3 = 'Произошла неизвестная ошибка!' #error3

error_4 = ('‼️Произошла непредвиденная ошибка.\n'
          'Попробуйте позже, если проблема остается,\n'
          'обратитесь за помощью!\n') #error5


