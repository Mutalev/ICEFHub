import telebot
import Conf1
import json
from telebot import types
from Dasboot import findGroups,findGroup1,findGroup2
from PDFslayer import *
from functools import partial

bot = telebot.TeleBot(Conf1.TOKEN)

users_who_clicked = set()

with open('database.json', encoding='UTF-8') as file:
    all_users_data1 = json.load(file)

with open('raffle.json', encoding='UTF-8') as file:
    participants1 = json.load(file)

all_users_data = {}
for i in all_users_data1:
    all_users_data[int(i)] = all_users_data1[i]

participants = {}
for i in participants1:
    participants[int(i)] = participants1[i]

def dc(n):
    s = ''
    f = 1
    c = 0
    for i, j  in n.items():
        if f < 151:
            if j is None:
                s += f'{f}. {i} @none\n'
            else:
                s += f'{f}. {i} @{j}\n'
            f += 1
        else:
            if f < 301:
                if c == 0:  
                    bot.send_message(1894542070, s)
                    c = 1
                    s = ''
                if j is None:
                    s += f'{f}. {i} @none\n'
                else:
                    s += f'{f}. {i} @{j}\n'
                f += 1
            else:
                if c == 1:  
                    bot.send_message(1894542070, s)
                    c = 2
                    s = ''
                if j is None:
                    s += f'{f}. {i} @none\n'
                else:
                    s += f'{f}. {i} @{j}\n'
                f += 1
    bot.send_message(1894542070, s)

def data(id, nickname):
    all_users_data[id] = nickname

def js(n):
    with open('database.json', 'w', encoding='UTF-8') as file:
        json.dump(n, file, indent=4)

def js_participants(n):
    with open('raffle.json', 'w', encoding='UTF-8') as file:
        json.dump(n, file, indent=4)

def ras(message):
    user_to_remove = []
    for i in all_users_data:
        try:
            bot.send_message(i, message.text)
        except Exception as e:
            user_to_remove.append(i)
    for i in user_to_remove:
        del all_users_data[i]

# def aip(message):
#     s = ''
#     response = g4f.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[{"role": "user", "content": message.text}],
#     stream=True,)
#     for i in response:
#         s += i
#     bot.send_message(message.chat.id, s)


# @bot.message_handler(commands=['ai'])
# def main(message):
#     bot.register_next_step_handler(message, aip)


@bot.message_handler(commands=['start'])
def main(message):
    data(message.from_user.id, message.from_user.username)
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('📊 Ваши Данные')
    btn4 = types.KeyboardButton('🗓 Получить расписание(pdf)')
    markup.row(btn1, btn4)
    btn2 = types.KeyboardButton('🤙🏻 Связь')
    btn3 = types.KeyboardButton('🗓 Расписание экзаменов')
    btn5 = types.KeyboardButton('ℹ️ Office hours')
    btn6 = types.KeyboardButton('🗓 Расписание факультативов(pdf)')
    markup.row(btn2, btn3)
    markup.row(btn5, btn6)
    text = """
    <b>Всем привет!</b> 

    📊 <b>Ваши Данные</b> - отпраялет файл с распределением по группам.

    🤙🏻 <b>Связь</b> - написать боту в одностороннем порядке.

    🗓 <b>Расписание экзаменов</b> - Расписание экзаменов.

    ℹ️ <b>Office hours</b> - Расписание ofiice hours.

    🗓 <b>Получть расписание(pdf)</b> - общее расписание в виде таблицы.

    🗓 <b>Расписание факультативов(pdf)</b> - расписапние всех факультативов в виде таблицы.

    🔧 <i>Если возникнут какие-то проблемы с ботом, сначала попробуйте перезапустить его</i> ( /start ).

    📝 <i>Если у вас есть идеи по добавлению в бота новых функций или вы нашли ошибку в расписании, то жмите</i> ( /help ).
    """
    bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)    # bot.register_next_step_handler(message, on_click)

def add_user(message):
    # s = findGroups(message.text).split()
    if (message.text != "🗓 Получить расписание(pdf)") and (message.text != "📊 Ваши Данные") and (message.text != "🗓 Расписание факультативов(pdf)") and (message.text != "🗓 Расписание экзаменов") and (message.text != "🤙🏻 Связь") and (message.text != "ℹ️ Инфа по Учителям(pdf)"):
        bot.send_message(1894542070, f'{message.text}\n@{message.from_user.username}\n{message.from_user.first_name, message.from_user.last_name}' )
    bot.send_message(message.chat.id, 'Сообщение принято')
    # if len(s) == 0:
    #     bot.send_message(message.chat.id, 'Проверьте верность введённых данных в формате (Фамилия Имя) или такого человека нет в МИЭФ 1й курс')
    # else:
    #     bot.send_message(message.chat.id, f"{s[0]}  <b>{s[1]}</b> \n{s[2]}   <b>{s[3]}</b>", parse_mode='html')
    #     markup = types.InlineKeyboardMarkup()
    #     datatosend = s[1] + ' ' + s[3]
    #     btn1 = types.InlineKeyboardButton('Моё расписание', callback_data=f'fac_{datatosend}')
    #     markup.row(btn1)
    #     bot.send_message(message.chat.id, 'Жми', reply_markup=markup)

    
@bot.message_handler(commands=['admin1234'])
def main(message):
    if message.from_user.id == 1894542070:
        bot.register_next_step_handler(message, ras)

@bot.message_handler(commands=['admin'])
def main(message):
    if message.from_user.id == 1894542070:
        dc(all_users_data)

@bot.message_handler(commands=['help'])
def main(message):
    data(message.from_user.id, message.from_user.username)
    bot.send_message(message.chat.id, '<b>Памагите</b>\n Пиши: @Popuskinmutabor', parse_mode='html')

@bot.message_handler(commands=['info'])
def main(message):
    data(message.from_user.id, message.from_user.username)
    text = """
    📊 <b>Ваши Данные</b> - Рсапределение по группам.
    🤙🏻 <b>Связь</b> - написать боту в одностороннем порядке.
    🗓 <b>Расписание экзаменов</b> - Расписание экзаменов.
    ℹ️ <b>Office hours</b> - офисные часы.
    🗓 <b>Получть расписание(pdf)</b> - общее расписание в виде таблицы.
    🔧 <i>Если возникнут какие-то проблемы с ботом, сначала попробуйте перезапустить его</i> ( /start ).
    📝 <i>Если у вас есть идеи по добавлению в бота новых функций или вы нашли ошибку в расписании, то жмите</i> ( /help ).
    """
    bot.send_message(message.chat.id, text, parse_mode='HTML')

def ref(message):
    r = int(message.text)
    if r > 11 or r  < 0:
        bot.send_message(message.chat.id, 'Их всего 11, бро)')
    else:
        bot.send_message(message.chat.id, 'Введите день недели')
        bot.register_next_step_handler(message, partial(fr, r=r))

def ref1(message):
    r = int(message.text)
    if r > 14 or r  < 0:
        bot.send_message(message.chat.id, 'Их всего 14, бро)')
    else:
        bot.send_message(message.chat.id, 'Введите день недели')
        bot.register_next_step_handler(message, partial(fr1, r=r))

def fr(message, r):
    message1 = message
    if type(message1) != str:
        message1 = str(message1.text)
    if message1.lower() == 'понедельник':
        bot.send_message(message.chat.id, f'Академ группа: \n{dMonday[r]}')
    if message1.lower() == 'вторник':
        bot.send_message(message.chat.id, f'Академ группа: \n{dTuseday[r]}')
    if message1.lower() == 'среда':
        bot.send_message(message.chat.id, f'Академ группа: \n{dWednesday[r]}')
    if message1.lower() == 'четверг':
        bot.send_message(message.chat.id, f'Академ группа: \n{dThursday[r]}')
    if message1.lower() == 'пятница':
        bot.send_message(message.chat.id, f'Академ группа: \n{dFriday[r]}')
    if message1.lower() == 'суббота':
        bot.send_message(message.chat.id, f'Академ группа: \n{dSaturday[r]}')



def fr1(message, r):
    message1 = message
    if type(message1) != str:
        message1 = str(message1.text)
    if message1.lower() == 'понедельник':
        bot.send_message(message.chat.id, f'Англ группа: \n {daMonday[r]}')
    if message1.lower() == 'вторник':
        bot.send_message(message.chat.id, f'Англ группа: \n {daTuseday[r]}')
    if message1.lower() == 'среда':
        bot.send_message(message.chat.id, f'Англ группа: \n {daWednesday[r]}')
    if message1.lower() == 'четверг':
        bot.send_message(message.chat.id, f'Англ группа: \n {daThursday[r]}')
    if message1.lower() == 'пятница':
        bot.send_message(message.chat.id, f'Англ группа: \n {daFriday[r]}')
    if message1.lower() == 'суббота':
        bot.send_message(message.chat.id, f'Англ группа: \n {daSaturday[r]}')

def graf(message):
    r = int(message.text)
    if r > 11 or r  < 0:
        bot.send_message(message.chat.id, 'Их всего 11, бро)')
    else:
        bot.send_message(message.chat.id, findGroup1(r))

def graf1(message):
    r = int(message.text)
    if r > 14 or r < 1:
        bot.send_message(message.chat.id, 'Их всего 14, бро)')
    else:
        bot.send_message(message.chat.id, findGroup2(r))


def combined_function(message, r1, r2):
    fr(message, int(r1))
    fr1(message, int(r2))

def comfunc1(mes, r1, r2, chat_id):
    s = '\n\n'.join([far(mes, int(r1), chat_id), far1(mes, int(r2), chat_id)])
    return s

def far(mes, r1, chat_id):
    if mes.lower() == 'понедельник':
        return(f'Академ группа: \n{dMonday[r1]}')
    if mes.lower() == 'вторник':
        return(f'Академ группа: \n{dTuseday[r1]}')
    if mes.lower() == 'среда':
        return(f'Академ группа: \n{dWednesday[r1]}')
    if mes.lower() == 'четверг':
        return(f'Академ группа: \n{dThursday[r1]}')
    if mes.lower() == 'пятница':
        return(f'Академ группа: \n{dFriday[r1]}')
    if mes.lower() == 'суббота':
        return(f'Академ группа: \n{dSaturday[r1]}')




def far1(mes, r2, chat_id):
    if mes.lower() == 'понедельник':
        return(f'Англ группа: \n{daMonday[r2]}')
    if mes.lower() == 'вторник':
        return(f'Англ группа: \n{daTuseday[r2]}')
    if mes.lower() == 'среда':
        return(f'Англ группа: \n{daWednesday[r2]}')
    if mes.lower() == 'четверг':
        return(f'Англ группа: \n{daThursday[r2]}')
    if mes.lower() == 'пятница':
        return(f'Англ группа: \n{daFriday[r2]}')
    if mes.lower() == 'суббота':
        return(f'Англ группа: \n{daSaturday[r2]}')


@bot.callback_query_handler(lambda callback: True)
def callback_message(callback):
    data(callback.from_user.id, callback.from_user.username)
    js(all_users_data)
    if '-' in callback.data:
        command, data_received, global_chat_id = callback.data.split('-')
        a = data_received.split()
        d = {
            'Monday':'Понедельник',
            'Tuseday':'Вторник',
            'Wednesday':'Среда',
            'Thursday':'Четверг',
            'Friday':'Пятница',
            'Sunday':'Суббота'
        }
        bot.send_message(callback.message.chat.id, comfunc1(d[command], a[0], a[1], global_chat_id))
    if '_' in callback.data:
        command, data_received = callback.data.split('_')
        global_chat_id = callback.message.chat.id
        if command == "fac":
            a = data_received.split()
            data_to = a[0] + ' ' + a[1]
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton('Понедельник', callback_data=f'Monday-{data_to}-{global_chat_id}')
            btn2 = types.InlineKeyboardButton('Вторник', callback_data=f'Tuseday-{data_to}-{global_chat_id}')
            btn3 = types.InlineKeyboardButton('Среда', callback_data=f'Wednesday-{data_to}-{global_chat_id}')
            btn4 = types.InlineKeyboardButton('Четверг', callback_data=f'Thursday-{data_to}-{global_chat_id}')
            btn5 = types.InlineKeyboardButton('Пятница', callback_data=f'Friday-{data_to}-{global_chat_id}')
            btn6 = types.InlineKeyboardButton('Суббота', callback_data=f'Sunday-{data_to}-{global_chat_id}')
            markup.row(btn1, btn2, btn3)
            markup.row(btn4, btn5, btn6)
            bot.send_message(callback.message.chat.id, 'Выберите день недели', reply_markup=markup)
            # bot.register_next_step_handler(callback.message, partial(combined_function, r1=a[0], r2=a[1]))
    else:
        if callback.data == 'gaf':
            bot.send_message(callback.message.chat.id, 'Введите номер группы' )
            bot.register_next_step_handler(callback.message, graf)
        if callback.data == 'gaf1':
            bot.send_message(callback.message.chat.id, 'Введите номер группы' )
            bot.register_next_step_handler(callback.message, ref)
        if callback.data == 'fac':
            bot.register_next_step_handler(callback.message, ref)
        if callback.data == 'gaf2':
            bot.send_message(callback.message.chat.id, 'Введите номер группы' )
            bot.register_next_step_handler(callback.message, graf1)
        if callback.data == 'gaf3':
            bot.send_message(callback.message.chat.id, 'Введите номер группы' )
            bot.register_next_step_handler(callback.message, ref1)






@bot.message_handler(content_types=['text'])
def on_click(message):
    data(message.from_user.id, message.from_user.username)
    js(all_users_data)
    s = str(message.from_user.last_name) + ' ' + str(message.from_user.first_name)
    if message.text == '📊 Ваши Данные':
        with open('Распределение_студентов_по_группам_на_2_курс_2024_.xlsx', 'rb') as f:
            bot.send_document(message.chat.id, f)
    #     bot.send_message(message.chat.id, 'Не в ресурсе(' )
    #     bot.send_message(message.chat.id, 'Введите: Фамилию Имя' )
    #     bot.register_next_step_handler(message, add_user )
    if message.text == '🤙🏻 Связь':
        bot.register_next_step_handler(message, add_user)
        # markup = types.InlineKeyboardMarkup()
        # btn1 = types.InlineKeyboardButton('Участники группы', callback_data='gaf')
        # btn2 = types.InlineKeyboardButton('Расписание группы', callback_data='gaf1')
        # markup.row(btn1,btn2)
        # bot.send_message(message.chat.id, 'Выберете действие', reply_markup=markup)
    if message.text == '🗓 Расписание экзаменов':
        with open('Расписание экзаменов.pdf', 'rb') as f:
            bot.send_document(message.chat.id, f)
        with open('Распределение_студентов_3_курса_по_аудиториям_на_зимнюю_сессию.xlsx', 'rb') as g:
            bot.send_document(message.chat.id, g)
        bot.send_message(1894542070, f'_ @{message.from_user.username}')
        # markup = types.InlineKeyboardMarkup()
        # btn1 = types.InlineKeyboardButton('Участники группы', callback_data='gaf2')
        # btn2 = types.InlineKeyboardButton('Расписание группы', callback_data='gaf3')
        # markup.row(btn1,btn2)
        # bot.send_message(message.chat.id, 'Выберете действие', reply_markup=markup)
    if message.text == '🗓 Получить расписание(pdf)':
        with open('3-курс-23.03-28.03.pdf', 'rb') as f:
            bot.send_document(message.chat.id, f)
        # if message.from_user.id == 584787190:
        #     bot.send_message(message.chat.id, 'Купи билет в Ереван Лёвчику')
        bot.send_message(1894542070, f'@{message.from_user.username}')
    if message.text == '🗓 Получть расписание(pdf)':
        with open('3-курс-23.03-28.03.pdf', 'rb') as f:
            bot.send_document(message.chat.id, f)
        bot.send_message(1894542070, f'@{message.from_user.username}')
    if message.text == 'ℹ️ Office hours':
        with open('Office Hours - 3 year 2 семестр.pdf', 'rb') as f:
            bot.send_document(message.chat.id, f)
    if message.text == '🗓 Расписание факультативов(pdf)':
        with open('List of Optional courses_2025-2026.pdf', 'rb') as f:
            bot.send_document(message.chat.id, f)
        # if message.chat.id in participants:
        #     bot.send_message(message.chat.id, f'Вы <b>уже</b> учавствуете в розыгрыше на <b>Monasterio</b> в святыне - <b>Mutabor</b> .\n\nКоличество участников: <b>{len(participants)}</b>\n\nВероятность обратиться в технокобру: <b>{1/len(participants):.2g}</b>', parse_mode='HTML')
        # else:
        #     participants[message.chat.id] = message.from_user.username
        #     bot.send_message(message.chat.id, f'Тепер вы учавствуете в розыгрыше на <b>Monasterio</b> в святыне - <b>Mutabor</b>.\n\nКоличество участников: <b>{len(participants)}</b>\n\nВероятность обратиться в технокобру: <b>{1/len(participants):.2g}</b>', parse_mode='HTML')
        # bot.send_message(1894542070, '\n'.join(f'{i + 1}. {j} @{participants[j]}' for i, j in enumerate(participants)))
        # js_participants(participants)
    if message.text == 'Розыгрыш билета на тусич':
        bot.send_message(message.chat.id, 'Жми: /start' )
        # user_nickname = message.from_user.username
        # if user_nickname not in users_who_clicked:
        #     users_who_clicked.add(user_nickname)
        #     bot.send_message(message.chat.id, f'Вы учавствуете в розыгрыше, колличество участников: <b>{str(len(users_who_clicked))}</b>, верятность победы: <b>{1/len(users_who_clicked):.2g}</b>', parse_mode='HTML' )
        # else:
        #     bot.send_message(message.chat.id, f'Вы <b>уже</b> учавствуете в розыгрыше, колличество участников: <b>{str(len(users_who_clicked))}</b>, верятность победы: <b>{1/len(users_who_clicked):.2g}</b>', parse_mode='HTML')
        # bot.send_message(1894542070, '\n'.join(f'{i + 1}. {j}' for i, j in enumerate(users_who_clicked)))
        # print(users_who_clicked)


bot.polling(non_stop=True)
