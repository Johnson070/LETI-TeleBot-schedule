#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import menu
import settings
import functions as func
import telebot
import requests
from telebot import types,apihelper
import time
import datetime
import random
import requests
from operator import itemgetter
import jsonpickle
import shutil
import threading
import asyncio

catalog_dict = {}
product_dict = {}
download_dict = {}
balance_dict = {}
admin_sending_messages_dict = {}
update_mode = False

def start_bot():
    bot = telebot.TeleBot(settings.bot_token)

    # def startTimer(waitForSeconds):
    #     loop = asyncio.new_event_loop()
    #     threading.Thread(daemon=True, target=loop.run_forever).start()
    #     async def sleep_and_run():
    #         while True:
    #             await asyncio.sleep(waitForSeconds)
    #             await myAsyncFunc()
    #     asyncio.run_coroutine_threadsafe(sleep_and_run(), loop)

    # async def myAsyncFunc():
    #     if datetime.datetime.now().hour == 0: #and datetime.datetime.now().minute > 21 and datetime.datetime.now().minute < 23
    #         conn = sqlite3.connect(settings.sqlite_file)
    #         cursor = conn.cursor()

    #         row = cursor.execute(f'SELECT * FROM users').fetchone()
    #         cursor.close()
    #         conn.close()
    #         print(row)

    #         for i in row:
    #             print(i)
    #             if '-' in i[0]:
    #                 try:
    #                     print(row)
    #                     if not func.check_channel(i[0]):
    #                         bot.send_message(i[0],"Бот не настроен на автоматическую рассылку!")
    #                     bot.send_message(i[0],get_schedule(i[1],0,channel=True))
    #                 except Exception as e:
    #                     print(e)


    # startTimer(5)

    def get_emoji(start_time, end_time):
        start_time = datetime.datetime.now().replace(hour=start_time[0],minute=start_time[1])
        end_time = datetime.datetime.now().replace(hour=end_time[0],minute=end_time[1])

        time = datetime.datetime.now()

        if time < start_time:
            return '❗'
        elif time >= start_time and time < end_time:
            return '🟢'
        elif time >= end_time:
            return '🔴'

    def get_schedule(chat_id,type,channel = False):
        weekday = datetime.datetime.now()

        user_group = 0
        week = 0
        if not channel:
            user = func.get_user(chat_id)
            user_group = user.group
            week = user.week
        else:
            if not func.check_channel(chat_id):
                return "Бот не настроен!"
            channel = func.get_channel(chat_id)
            week = channel[0]
            user_group = channel[1]

        if type < 2:
            if type == 1:
                weekday += datetime.timedelta(days=1)
            weekday_str = weekday.strftime("%a").upper()

            id_group = func.get_group_data(user_group).id_sys

            schedule = func.get_schedule(id_group,weekday_str, func.get_week_type(week,weekday))
            schedule = sorted(schedule, key = itemgetter(1))
            #print(schedule)

            if len(schedule) == 0:
                text = f'Расписание на {weekday.strftime("%d-%m-%y %a")} {"⬆️" if func.get_week_type(week,weekday) == 1 else "⬇️"}\n\n'
                text += '✅ Занятий нету)'
                return text
            else:
                text = f'Расписание на {weekday.strftime("%d-%m-%y %a")} {"⬆️" if func.get_week_type(week,weekday) == 1 else "⬇️"}\n\n'
                for i in schedule:
                    time_start = [int(i) for i in (func.time_schedule[int(i[1])]).split(':')]
                    time_end = [int(i) for i in (func.time_schedule[int(i[2])]).split(':')]
                    emoji = '▫'
                    if type == 0:
                        emoji = get_emoji(time_start,time_end)

                    if i[5] == 'None':
                        text += f'{emoji} {func.time_schedule[int(i[1])]} по {func.time_schedule[int(i[2])]} ➖ {i[0]}\n'\
                        '\tДИСТАНТ\n'\
                        f'\tУч. {i[6] if i[6] != "" else "не известно"}\n\n'
                    else:
                        text += f'{emoji} {func.time_schedule[int(i[1])]} по {func.time_schedule[int(i[2])]} ➖ {i[0]}\n'\
                        f'\tКаб. {i[5] if i[5] != "3300" else "не известно"}\n'\
                        f'\tУч. {i[6] if i[6] != "" else "не известно"}\n\n'
                return text
        else:
            text = '' #❌❗🔴🟢⬇️

            weekday = datetime.datetime.now()
            weekday += datetime.timedelta(days=7)
            for j in range(0,7):
                weekday -= datetime.timedelta(days=1)
                weekday_str = weekday.strftime("%a").upper()

                id_group = func.get_group_data(user_group).id_sys

                schedule = func.get_schedule(id_group,weekday_str, func.get_week_type(week,weekday))
                schedule = sorted(schedule, key = itemgetter(1))

                if len(schedule) == 0:
                    text += f'Расписание на {weekday.strftime("%d-%m-%y %a")} {"⬆️" if func.get_week_type(week,weekday) == 1 else "⬇️"}\n\n'
                    text += '✅ Занятий нету)\n\n'
                else:
                    text += f'Расписание на {weekday.strftime("%d-%m-%y %a")} {"⬆️" if func.get_week_type(week,weekday) == 1 else "⬇️"}\n\n'
                    for i in schedule:
                        time_start = [int(i) for i in (func.time_schedule[int(i[1])]).split(':')]
                        time_end = [int(i) for i in (func.time_schedule[int(i[2])]).split(':')]
                        emoji = '▫'
                        #emoji = get_emoji(time_start,time_end)

                        if i[5] == 'None':
                            text += f'{emoji} {func.time_schedule[int(i[1])]} по {func.time_schedule[int(i[2])]} ➖ {i[0]}\n'\
                            '\tДИСТАНТ\n'\
                            f'\tУч. {i[6] if i[6] != "" else "не известно"}\n\n'
                        else:
                            text += f'{emoji} {func.time_schedule[int(i[1])]} по {func.time_schedule[int(i[2])]} ➖ {i[0]}\n'\
                            f'\tКаб. {i[5] if i[5] != "3300" else "не известно"}\n'\
                            f'\tУч. {i[6] if i[6] != "" else "не известно"}\n\n'
                text += '➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n'

            return text



    def main_menu_send(chat_id,message_id=''):
        if message_id == '':
            bot.send_message(chat_id, get_schedule(chat_id,0),reply_markup=menu.main_menu)
        else:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=get_schedule(chat_id,0),
                reply_markup=menu.main_menu)

    @bot.channel_post_handler(commands=['start'])
    def handler_start_channel(message):
        chat_id = message.chat.id
        if message.chat.type == "channel":
            func.first_join_channel(chat_id)
            bot.send_message(chat_id,
                    "Добро пожаловать!" \
                    "\n" \
                    "Это бот вам поможет узнать нужную информацию, но перед этим" \
                    "Вам нужно настроить номер группы и тип недели.\n\n" \
                    "/help")

    @bot.channel_post_handler(commands=['help'])
    def help_channel(message):
        chat_id = message.chat.id
        if message.chat.type == "channel":
            bot.send_message(chat_id,
                "1) /help - Вывести все команды\n" \
                "2) /set_group 0000 - Настроить группу\n" \
                "3) /set_week [1,2]- Настроить тип недели(1 - верхняя,2-нижняя)\n" \
                "4) /schedule - Получить расписание на сегодня\n" \
                "5) /schedule_next - Получить расписание на завтра\n" \
                "6) /schedule_all - Получить полное расписание на неделю\n" \
                "7) /enable - ВКЛ/ВЫКЛ автоматическую ежедневную рассылку")

    @bot.channel_post_handler(commands=['schedule','schedule_next','schedule_all','enable'])
    def help_channel(message):
        chat_id = message.chat.id
        command = [i for i in message.text.split(' ')][0]
        if message.chat.type == "channel":
            if command == '/schedule':
                bot.send_message(chat_id,
                    get_schedule(chat_id,0,channel=True))
            if command == '/schedule_next':
                bot.send_message(chat_id,
                    get_schedule(chat_id,1,channel=True))
            if command == '/schedule_all':
                bot.send_message(chat_id,
                    get_schedule(chat_id,2,channel=True))
            if command == '/enable':
                enable = func.get_channel(chat_id)[2]
                enable = '1' if enable == '0' else '0'
                
                func.first_join_channel(chat_id,enabled=enable)
                bot.send_message(chat_id, f"Автоматическая рассылка {'ВЫКЛ' if enable == '0' else 'ВКЛ'}")

    @bot.message_handler(commands=['start'])
    def handler_start(message):
        chat_id = message.chat.id

        user = func.get_user(chat_id)

        if user != False and user.week != '' and user.group != '':
            main_menu_send(chat_id)
        else:
            func.first_join(chat_id, datetime.datetime.now(), message.from_user.username)

            bot.send_message(chat_id,
                "Добро пожаловать!" \
                "\n" \
                "Это бот вам поможет узнать нужную информацию, но перед этим" \
                "Вам нужно написать номер своей группы и тип недели.")

            msg = bot.send_message(chat_id, "Отправте номер своей группы")
            bot.register_next_step_handler(msg, group_number)


    # Command admin
    @bot.message_handler(commands=['admin'])
    def handler_admin(message):
        chat_id = message.chat.id
        if chat_id == settings.admin_id_1 or chat_id == settings.admin_id_2:
            bot.send_message(chat_id, 'Вы перешли в меню админа', reply_markup=menu.admin_menu)

    @bot.message_handler(commands=['reboot'])
    def handler_admin(message):
        chat_id = message.chat.id
        if chat_id == settings.admin_id_1 or chat_id == settings.admin_id_2:
            print(chat_id)
            sys.exit()
            exit()

    # Обработка данных
    @bot.channel_post_handler(commands=['set_group'])
    def parse_channel_group_number(message):
        chat_id = message.chat.id
        message_group = [i for i in message.text.split(' ')]
        if len(message_group) < 2:
            bot.send_message(chat_id,
                "Произошла ошибка!")
        else:
            if func.check_group(message_group[1]):
                func.first_join_channel(chat_id, group_id=message_group[1])
                bot.send_message(chat_id,
                    "Номер группы сохранён")
            else:
                bot.send_message(chat_id,
                "Такой группы не существует")

    @bot.channel_post_handler(commands=['set_week'], regexp="\d")
    def parse_channel_group_number(message):
        chat_id = message.chat.id
        message_group = [i for i in message.text.split(' ')]
        if len(message_group) < 2 or (int(message_group[1]) > 2 or int(message_group[1]) < 1):
            bot.send_message(chat_id,
                "Произошла ошибка!")
        else:
            func.first_join_channel(chat_id, type_week=message_group[1])
            bot.send_message(chat_id,
                "Тип недели сохранён сохранён")



    @bot.callback_query_handler(func=lambda call: True)
    def handler_call(call):
        global update_mode
        chat_id = call.message.chat.id
        message_id = call.message.message_id

        if update_mode:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text="Бот обновляет расписание...\n\nСкоро он заработает",
                reply_markup=menu.main_menu)
        else:
            if call.data == 'teachers_group':
                user = func.get_user(chat_id)
                user_group = user.group

                id_group = func.get_group_data(user_group).id_sys
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=func.get_teachers_group(id_group),
                    reply_markup=menu.main_menu_4,
                    parse_mode='HTML')


            if call.data == 'mail_to':
                if chat_id == settings.admin_id_1 or chat_id == settings.admin_id_2:
                    msg = bot.send_message(
                        chat_id,
                        "Напишите текст рассылки",
                        reply_markup=menu.back_to_admin_menu
                    )
                    bot.register_next_step_handler(msg, send_mail)

            if call.data == 'requests_view':
                if chat_id == settings.admin_id_1 or chat_id == settings.admin_id_2:
                    bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=func.get_requests(),
                        reply_markup=menu.back_to_admin_menu
                        )

            if call.data == 'links':
                bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=func.get_links(),
                        reply_markup=menu.main_menu_3,
                        parse_mode='HTML')

            if call.data == 'reset':
                msg = bot.send_message(chat_id, "Отправте номер своей группы")
                bot.register_next_step_handler(msg, group_number)

            if call.data == 'profile':
                user = func.get_user(chat_id)
                group = func.get_group_data(user.group)
                bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=settings.profile.format(
                            data=user.group,
                            fac=group.facultu,
                            type=group.EDType,
                            level=group.level,
                            week='Верхняя(нечетная)' if user.week == '1' else 'Нижняя(чётная)'),
                        reply_markup=menu.profile)

            if call.data == 'schedule_full':
                bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=get_schedule(chat_id,2),
                        reply_markup=menu.main_menu_2)

            if call.data == 'schedule_next':
                bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=get_schedule(chat_id,1),
                        reply_markup=menu.main_menu_1)

            if call.data == 'schedule_now':
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=get_schedule(chat_id,0),
                    reply_markup=menu.main_menu)
                


            if call.data == 'week_1':
                func.update_user(chat_id,week=1)

                main_menu_send(chat_id,message_id)

            if call.data == 'week_2':
                func.update_user(chat_id,week=2)

                main_menu_send(chat_id,message_id)

            if call.data == 'requests':
                msg = bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text='Напишите что хотите добавить, исправить и т.п',
                    reply_markup=menu.nazad
                )
                bot.register_next_step_handler(msg, request_wait)


            if call.data == 'send_request':
                print(call.message.text)
                main_menu_send(chat_id,message_id)

            if call.data == 'exit_to_menu':
                main_menu_send(chat_id,message_id)
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)

            if call.data == 'admin_info':
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=func.admin_info(),
                    reply_markup=menu.back_to_admin_menu
                )

            if call.data == 'back_to_admin_menu':
                if chat_id == settings.admin_id_1 or chat_id == settings.admin_id_2:
                    bot.edit_message_text(
                        chat_id=chat_id, 
                        message_id=message_id,
                        text='Вы перешли в меню админа', 
                        reply_markup=menu.admin_menu)

            if call.data == 'send_by_bot':
                if chat_id == settings.admin_id_1 or chat_id == settings.admin_id_2:
                    msg = bot.edit_message_text(
                        chat_id=chat_id, 
                        message_id=message_id,
                        text='Отправьте id чата и через # сообщение', 
                        reply_markup=menu.back_to_admin_menu)
                    bot.register_next_step_handler(msg, chat_send_bot)

            if call.data == 'send_bd':
                if chat_id == settings.admin_id_1 or chat_id == settings.admin_id_2:
                    bot.send_document(chat_id, open(settings.sqlite_file, 'rb'))
                

            if call.data == 'add_schedule':
                shutil.copyfile(settings.sqlite_file, settings.sqlite_file_update)
                r = requests.get('https://digital.etu.ru/api/common/groups?forLastPublicatedSchedule=true&withFaculty=true&withSemesterSeasons=true&withFlows=true')

                groups_id = []
                groups = []
                if r.status_code == 200:
                    #update_mode = True
                    json = r.json()

                    count = 0

                    conn = sqlite3.connect(settings.sqlite_file_update)
                    cursor = conn.cursor()

                    exists_groups = func.get_groups_exists()

                    func.clear_groups_schedule(bot,chat_id,message_id)
                    func.clear_groups()
                    func.clear_teachers()
                    

                    for group in json:
                        if (not group['fullNumber'] in groups):
                            groups_id.append(group['id'])
                            groups.append(group['fullNumber'])

                        if count % 40 == 0:
                            bot.edit_message_text(
                                chat_id=chat_id,
                                message_id=message_id,
                                text=f"Ожидайте пока бот обновит базу групп!\n\n({count+1} из {len(json)})")
                        count+=1
                        
                        cursor.execute(f"""INSERT INTO [groups] VALUES ('{group['id']}',
                                                                        '{group['fullNumber']}',
                                                                        '{group['educationLevel']}',
                                                                        '{group['department']['faculty']['title']}',
                                                                        '{group['studyingType']}')
                                                                        """)
                                  
                    conn.commit()

                    cursor.close()
                    conn.close()
                    count = 1

                    conn = sqlite3.connect(settings.sqlite_file_update)
                    cursor = conn.cursor()

                    lessons = {}

                    for group_id in groups_id:

                        if count % 5 == 0:
                            bot.edit_message_text(
                                chat_id=chat_id,
                                message_id=message_id,
                                text=f"Ожидайте пока бот скачает базу расписания!\n\n({count+1} из {len(groups)})")
                        count+=1

                        r = requests.get(f'https://digital.etu.ru/api/schedules/publicated?groups={group_id}&withSubjectCode=true&withURL=true')

                        if r.status_code == 200:
                            text = r.text.replace("'",'')
                            json = jsonpickle.decode(text)

                            lessons[group_id] = json
                        else:
                            print("Сервак лег(")
                            bot.edit_message_text(
                                chat_id=chat_id,
                                message_id=message_id,
                                text=f"Сервак Лег(",
                                reply_markup=menu.nazad)
                            update_mode = False
                            return

                    count = 0
                    if len(lessons) > 0:
                        for group_id in groups_id:
                            if count % 20 == 0:
                                bot.edit_message_text(
                                    chat_id=chat_id,
                                    message_id=message_id,
                                    text=f"Ожидайте пока бот обновит базу расписания!\n\n({count+1} из {len(groups)})")
                            count+=1


                            json = lessons[group_id]
                            if json == [] or len(json[0]["scheduleObjects"]) == 0:
                                continue

                            if not (str(group_id) in exists_groups):
                                cursor.execute(f"""CREATE TABLE [{group_id}] (
                                                    title      TEXT,
                                                    start      TEXT,
                                                    stop       TEXT,
                                                    week_day   TEXT,
                                                    week_type  TEXT,
                                                    class      TEXT,
                                                    teacher    TEXT,
                                                    teacher_id TEXT
                                                );
                                                """)

                            teachers = []
                            for lesson in json[0]["scheduleObjects"]:
                                try:
                                    class_num = lesson['lesson']['auditoriumReservation']["auditoriumNumber"]

                                    if type(class_num) != type(None):
                                        # if type(lesson['lesson']['auditoriumReservation']["auditorium"]) == type(None):
                                        #     class_num = '3300'

                                        # if str(group_id) == "1641":
                                        #     print(lesson['lesson']['auditoriumReservation']['auditorium'])
                                        #     print(type(lesson['lesson']['auditoriumReservation']["auditorium"]) != type(None) and type(lesson['lesson']['auditoriumReservation']['auditorium']['alias']) != type(None))
                                        #     print(lesson['lesson']['auditoriumReservation']["auditoriumNumber"])

                                        if type(lesson['lesson']['auditoriumReservation']["auditorium"]) != type(None) and type(lesson['lesson']['auditoriumReservation']['auditorium']['alias']) != type(None):
                                            class_num = lesson['lesson']['auditoriumReservation']["auditoriumNumber"] + ' Название: ' +lesson['lesson']['auditoriumReservation']['auditorium']['alias']


                                    if lesson['lesson']['teacher'] == None:
                                        cursor.execute(f"""INSERT INTO [{group_id}] VALUES (
                                                                    '{lesson['lesson']['subject']['shortTitle']}  <{lesson['lesson']['subject']['subjectType']}>',
                                                                    '{lesson['lesson']['auditoriumReservation']['reservationTime']['startTime']}',
                                                                    '{lesson['lesson']['auditoriumReservation']['reservationTime']['endTime']}',
                                                                    '{lesson['lesson']['auditoriumReservation']['reservationTime']['weekDay']}',
                                                                    '{lesson['lesson']['auditoriumReservation']['reservationTime']['week']}',
                                                                    '{class_num}',
                                                                    "",
                                                                    ""
                                                                    )""")
                                    else:
                                        row = cursor.execute(f"""SELECT * FROM teachers WHERE id='{lesson['lesson']['teacher']['id']}'""").fetchall()
                                        if len(row) == 0:
                                            cursor.execute(f"""INSERT INTO teachers VALUES (
                                                                        '{lesson['lesson']['teacher']['id']}',
                                                                        '{lesson['lesson']['teacher']['initials']}',
                                                                        '{lesson['lesson']['teacher']['position']}',
                                                                        '{lesson['lesson']['teacher']['email']}',
                                                                        '{lesson['lesson']['teacher']['phone']}'
                                                                        )""")
                                            teachers.append(lesson['lesson']['teacher']['id'])

                                        # if type(lesson['lesson']['auditoriumReservation']["auditorium"]) != type(None) and type(lesson['lesson']['auditoriumReservation']['auditorium']['alias']) != type(None):
                                        #     print(lesson['lesson']['auditoriumReservation']['auditorium']['alias'],lesson['lesson']['auditoriumReservation']['auditorium']['number'],group_id)

                                        #print(lesson['lesson']['auditoriumReservation']["auditorium"])

                                        cursor.execute(f"""INSERT INTO [{group_id}] VALUES (
                                                                    '{lesson['lesson']['subject']['shortTitle']}  <{lesson['lesson']['subject']['subjectType']}>',
                                                                    '{lesson['lesson']['auditoriumReservation']['reservationTime']['startTime']}',
                                                                    '{lesson['lesson']['auditoriumReservation']['reservationTime']['endTime']}',
                                                                    '{lesson['lesson']['auditoriumReservation']['reservationTime']['weekDay']}',
                                                                    '{lesson['lesson']['auditoriumReservation']['reservationTime']['week']}',
                                                                    '{class_num}',
                                                                    '{lesson['lesson']['teacher']['initials']}',
                                                                    '{lesson['lesson']['teacher']['id']}'
                                                                    )""")
                                except Exception as e:
                                    print(str(e),group_id)
                                    #print(json)
                                    # import json
                                    # print(json.loads(r.text)[0]["scheduleObjects"]['lesson']['subject']['title'])
                                    # return



                                #     cursor.execute(f"DROP TABLE IF EXISTS [{group_id}]; ")
                                #     if (group_id == 1321):
                                #         print(jsonpickle.encode(json, make_refs=False))


                    conn.commit()

                    cursor.close()
                    conn.close()

                    shutil.copyfile(settings.sqlite_file_update, settings.sqlite_file)
                else:
                    bot.edit_message_text(
                                chat_id=chat_id,
                                message_id=message_id,
                                text=f"Сервак Лег(",
                                reply_markup=menu.nazad)
                    update_mode = False
                    return

                bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text='Вы перешли в меню админа\n\nРасписание обновлено!', 
                    reply_markup=menu.admin_menu)
                update_mode = False

    def chat_send_bot(message):
        chat_id = message.text.split('#')
        try:
            bot.send_message(chat_id[0],chat_id[1])
        except:
            print("error!")
        main_menu_send(message.chat.id)

    def request_wait(message):
        request_msg = message.text
        func.save_request(message.chat.id,request_msg,0)
        bot.send_message(message.chat.id, "Отправлено!")
        main_menu_send(message.chat.id)

    def group_number(message):
        group_num = message.text

        if not func.check_group(group_num):
            msg = bot.send_message(message.chat.id, "Такой группы не существует!\nОтправте номер своей группы")
            bot.register_next_step_handler(msg, group_number)
        else:
            #print(message.chat.id)
            func.update_user(message.chat.id,group=group_num)

            bot.send_message(message.chat.id, 
                "Выберите тип недели(<a href='https://etu.ru/ru/studentam/studencheskie-novosti/v-leti-ustanovlen-novyj-grafik-nachala-i-okonchaniya-uchebnyh-zanyatij1'>узнать</a>):", 
                reply_markup=menu.type_week,
                parse_mode='HTML')

    def send_mail(message):
        text_message = message.text
        conn = sqlite3.connect(settings.sqlite_file)
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM users')
        row = cursor.fetchall()
        cursor.close()
        conn.close()
        bot.send_message(
            chat_id=message.chat.id, 
            text='Рассылка началась!', 
            reply_markup=menu.admin_menu)

        count = 0
        for i in row:
            try:
                time.sleep(1)
                bot.send_message(row[0], text_message)
            except Exception as e:
                print("ERROW", str(e))

    bot.polling(none_stop=True,interval=0, timeout=20)
        
apihelper.SESSION_TIME_TO_LIVE = 5 * 60

start_bot()
 
