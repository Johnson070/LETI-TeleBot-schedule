from telebot import types
import sqlite3
import telebot
import os
import requests
import settings
import random
import json
import datetime


class user_data:
    def __init__(self,id_sys,group_id,level,facultu,EDType):
        self.id_sys = id_sys
        self.group_id = group_id
        self.level = level
        self.facultu = facultu
        self.EDType = EDType

class user:
    def __init__(self, user_id,name,date_connect,week=None,group=None,lang = 'RU'):
        self.user_id = user_id
        self.week = week
        self.group = group
        self.date_connect = date_connect
        self.lang = lang
        self.name = name

class facultie:
    def __init__(self, name, id_facu,link = ""):
        self.name = name
        self.id_facu = id_facu
        self.link = link

class requests:
    def __init__(self, user_id,request, done = False):
        self.user_id = user_id
        self.request = request
        self.done = done

class schedule:
    def __init__(self, course, group, name, n_class, time_start, teacher, distance = False):
        self.course = course
        self.group = group
        self.name = name
        self.n_class = n_class
        self.time_start = time_start
        self.distance = distance
        self.teacher = teacher


class Admin_sending_messages:
    def __init__(self, user_id):
        self.user_id = user_id
        self.text = None

time_schedule = {
    100: '8:00',
    1100: '9:30',
    101: '9:50',
    1101: '11:20',
    102: '11:40',
    1102: '13:10',
    103: '13:40',
    1103: '15:10',
    104: '15:30',
    1104: '17:00',
    105: '17:20',
    1105: '18:50',
    106: '19:05',
    1106: '20:35',
    107: '20:50',
    1107: '22:20'
}


###########################################################################################

def get_requests():
    text = ''
    conn = sqlite3.connect(settings.sqlite_file)
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM [requests]').fetchall()
    cursor.close()
    conn.close()

    if row == []:
        return 'Заявок нету!'

    for i in row:
        #print(i)
        if i[2] == 0:
            text += f'➖ {i[1]}\n'

    if text == '':
        return 'Заявок нету!'
    #print(text)
    return text

def get_links():
    text = ''
    conn = sqlite3.connect(settings.sqlite_file)
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM [links]').fetchall()
    cursor.close()
    conn.close()

    for i in row:
        text += f'➖ <a href="{i[1]}">{i[0]}</a>\n'

    #text += '<a href="https://etu.ru/assets/images/university/campus/leti_map.jpg">Карта</a>'
    return text

def check_group(group):
    conn = sqlite3.connect(settings.sqlite_file)
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM [groups] WHERE group_id = "{group}"').fetchall()
    cursor.close()
    conn.close()
    if row == []:
        return False
    else:
        return True

def get_week_type(week_user,date):
    week_user = int(week_user)
    week_count = date.isocalendar()[1]
    out_week = 0
    if week_user == 1:
         out_week = 1 if week_count % 2 != 0 else 2
    else:
         out_week = 1 if week_count % 2 == 0 else 2
    return out_week

def get_schedule(group_id,weekday,week_type):
    conn = sqlite3.connect(settings.sqlite_file)
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM [{group_id}] WHERE week_day = "{weekday}" and week_type = "{week_type}"').fetchall()
    cursor.close()
    conn.close()
    return row

def get_group_data(group_id):
    conn = sqlite3.connect(settings.sqlite_file)
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM [groups] WHERE group_id = "{group_id}"').fetchall()
    cursor.close()
    conn.close()

    if row == []:
        return False
    else:
        return user_data(row[0][0],row[0][1],row[0][2],row[0][3],row[0][4])


def get_user(user_id):
    conn = sqlite3.connect(settings.sqlite_file)
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchall()

    cursor.close()
    conn.close()

    #print(row)

    if row == []:
        return False
    else:
        #print(row[0][0])
        return user(row[0][0],row[0][5],row[0][3],row[0][1],row[0][2],row[0][4])

def update_user(user_id,group=None,week=None):
    conn = sqlite3.connect(settings.sqlite_file)
    cursor = conn.cursor()

    row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchone()

    if row != None:
        if group != None:
            cursor.execute(f'UPDATE users SET [group] = {group} WHERE user_id = "{user_id}"')
            conn.commit()
        if week != None:
            cursor.execute(f'UPDATE users SET week = {week} WHERE user_id = "{user_id}"')
            conn.commit()

    cursor.close()
    conn.close()


def first_join(user_id,date_connect,name):
    conn = sqlite3.connect(settings.sqlite_file)
    cursor = conn.cursor()

    row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchone()

    if row == None:
        cursor.execute(f"INSERT INTO users VALUES ('{user_id }','','','{date_connect }','RU','{name}')")
        conn.commit()
    
    cursor.close()
    conn.close()

def first_join_channel(channel_id,type_week=None,group_id = None, enabled = None):
    conn = sqlite3.connect(settings.sqlite_file)
    cursor = conn.cursor()

    row = cursor.execute(f'SELECT * FROM channels WHERE channel_id = "{channel_id}"').fetchone()

    if row == None:
        cursor.execute(f"INSERT INTO channels VALUES ('{channel_id}','{0}','{0}','{1}')")
        conn.commit()
    else:
        if type_week != None:
            cursor.execute(f'UPDATE channels SET [type_week] = {type_week} WHERE channel_id = "{row[0]}"')
            conn.commit()
        if group_id != None:
            cursor.execute(f'UPDATE channels SET [group_id] = {group_id} WHERE channel_id = "{row[0]}"')
            conn.commit()
        if enabled != None:
            cursor.execute(f'UPDATE channels SET [enabled] = {enabled} WHERE channel_id = "{row[0]}"')
            conn.commit()
    
    cursor.close()
    conn.close()

def check_channel(channel_id):
    conn = sqlite3.connect(settings.sqlite_file)
    cursor = conn.cursor()

    row = cursor.execute(f'SELECT * FROM channels WHERE channel_id = "{channel_id}"').fetchone()
    cursor.close()
    conn.close()

    if row == None:
        return False
    else:
        if row[1] == '0' or row[2] == '0':
            return False
        else:
            return True

def get_channel(channel_id):
    conn = sqlite3.connect(settings.sqlite_file)
    cursor = conn.cursor()

    row = cursor.execute(f'SELECT * FROM channels WHERE channel_id = "{channel_id}"').fetchone()
    cursor.close()
    conn.close()

    return [row[1],row[2],row[3]]

def save_request(user_id,request,done):
    conn = sqlite3.connect(settings.sqlite_file)
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO requests VALUES ('{user_id }','{request}','{done}')")
    conn.commit()
    
    cursor.close()
    conn.close()

def clear_groups():
    conn = sqlite3.connect(settings.sqlite_file_update)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM [groups]")
    conn.colmmit()
    cursor.close()
    conn.close()

def clear_teachers():
    conn = sqlite3.connect(settings.sqlite_file_update)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM teachers")
    conn.commit()
    cursor.close()
    conn.close()

def get_groups_exists():
    groups = []
    conn = sqlite3.connect(settings.sqlite_file_update)
    cursor = conn.cursor()


    row = cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    conn.commit()    
    cursor.close()
    conn.close()

    for i in row:
        if i[0].isdigit() and i[0] != '0000':
            groups.append(i[0])

    return groups



def clear_groups_schedule(bot,chat_id,message_id):
    conn = sqlite3.connect(settings.sqlite_file_update)
    cursor = conn.cursor()


    row = cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    count = 0
    for i in row:
        if count % 40 == 0:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"Ожидайте пока бот удалит старую базу!\n\n({count+1} из {len(row)})")
        count += 1
        if i[0].isdigit() and i[0] != '0000':
            cursor.execute(f"DELETE FROM [{i[0]}]; ")

    conn.commit()    
    cursor.close()
    conn.close()


def admin_info():
    conn = sqlite3.connect(settings.sqlite_file)
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM users').fetchone()

    current_time = str(datetime.datetime.now())

    amount_user_all = 0
    amount_user_day = 0
    amount_user_hour = 0

    while row is not None:
        amount_user_all += 1
        if row[3][:-15:] == current_time[:-15:]:
            amount_user_day += 1
        if row[3][:-13:] == current_time[:-13:]:
            amount_user_hour += 1

        row = cursor.fetchone()

    msg = '❕ Информация:\n\n' \
          f'❕ Пользователей за все время: - {amount_user_all}\n' \
          f'❕ За день - {amount_user_day}\n' \
          f'❕ За час - {amount_user_hour}'

    return msg


def get_teachers_group(group_id):
    conn = sqlite3.connect(settings.sqlite_file)
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM [{group_id}]').fetchall()
    

    if row == []:
        return "Учителей нету!"

    teachers_ids = []
    for i in row:
        if i[7] != '' and not (i[7] in teachers_ids):
            teachers_ids.append(i[7])

    text = ''
    for i in teachers_ids:
        row = cursor.execute(f'SELECT * FROM teachers WHERE id="{i}"').fetchall()
        #print(row)
        if row != []:
            row = row[0]
            text += f'➖ {row[1]} <a href="{row[3]}">{row[3]}</a>' + (f'<a href="tel:{row[4]}">{row[4]}</a>' if row[4] != 'None' else "") + "\n"

    cursor.close()
    conn.close()

    return text





###########################################################################################
# Menu catalog
# def menu_catalog():
#     conn = sqlite3.connect("base_ts.sqlite")
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM catalog')
#     row = cursor.fetchall()

#     menu = types.InlineKeyboardMarkup(row_width=1)

#     for i in row:
#         menu.add(types.InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[1]}'))

#     menu.add(types.InlineKeyboardButton(text='Назад', callback_data='exit_to_menu'))

#     cursor.close()
#     conn.close()

#     return menu


# # Menu section
# def menu_section(name_section):
#     conn = sqlite3.connect("base_ts.sqlite")
#     cursor = conn.cursor()
#     cursor.execute(f"SELECT * FROM '{name_section}' ")
#     row = cursor.fetchall()

#     menu = types.InlineKeyboardMarkup(row_width=1)

#     for i in row:
#         menu.add(types.InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[2]}'))

#     menu.add(types.InlineKeyboardButton(text='Назад', callback_data='exit_to_menu'))

#     cursor.close()
#     conn.close()

#     return menu


# # Menu product
# def menu_product(product, dict):
#     conn = sqlite3.connect("base_ts.sqlite")
#     cursor = conn.cursor()

#     row = cursor.execute(f'SELECT * FROM section WHERE code = "{product}"').fetchone()
#     section = row[1]
#     info = row[3]

#     amount = len(cursor.execute(f'SELECT * FROM "{product}"').fetchall())

#     cursor.execute(f'SELECT * FROM "{section}" WHERE code = "{product}"')
#     row = cursor.fetchone()

#     dict.section = section
#     dict.product = product
#     dict.amount_MAX = amount
#     dict.price = row[1]

#     text = settings.text_purchase.format(
#         name=row[0],
#         info=info,
#         price=row[1],
#         amount=amount
#     )

#     return text, dict

# #   Admin menu - add_to_section_to_catalog
# def add_section_to_catalog(name_section):
#     # Connection
#     conn = sqlite3.connect("base_ts.sqlite")
#     cursor = conn.cursor()
#     code = random.randint(11111, 99999)
#     # Add
#     cursor.execute(f"INSERT INTO catalog VALUES ('{name_section}', '{code}')")
#     conn.commit()

#     # Create table section
#     conn.execute(f"CREATE TABLE '{code}' (list text, price text, code text)")

#     # Close connection
#     cursor.close()
#     conn.close()


# # Admin menu - del_section_to_catalog
# def del_section_to_catalog(name_section):
#     # Connection
#     conn = sqlite3.connect("base_ts.sqlite")
#     cursor = conn.cursor()

#     # Del
#     cursor.execute(f"DELETE FROM catalog WHERE code = '{name_section}'")
#     conn.commit()

#     cursor.execute(f"DROP TABLE '{name_section}'")

#     row = cursor.execute(f'SELECT * FROM section WHERE section = "{name_section}"').fetchall()

#     for i in range(len(row)):
#         cursor.execute(f'DROP TABLE "{row[i][2]}"')

#         cursor.execute(f'DELETE FROM section WHERE code = "{row[i][2]}"')
#         conn.commit()

#     # Close connection
#     cursor.close()
#     conn.close()


# # Admin menu - add_product_to_section
# def add_product_to_section(name_product, price, name_section, info):
#     # Connection
#     conn = sqlite3.connect("base_ts.sqlite")
#     cursor = conn.cursor()

#     code = random.randint(11111, 99999)

#     cursor.execute(f"INSERT INTO '{name_section}' VALUES ('{name_product}', '{price}', '{code}')")
#     conn.commit()

#     cursor.execute(f"INSERT INTO 'section' VALUES ('{name_product}', '{name_section}', '{code}', '{info}')")
#     conn.commit()

#     # Create table product
#     cursor.execute(f"CREATE TABLE '{code}' (list text, code text)")

#     # Close connection
#     cursor.close()
#     conn.close()


# # Admin menu - del_product_to_section
# def del_product_to_section(name_product, section):
#     # Connection
#     conn = sqlite3.connect("base_ts.sqlite")
#     cursor = conn.cursor()

#     # del
#     product = cursor.execute(f'SELECT * FROM "{section}" WHERE list = "{name_product}"').fetchone()

#     cursor.execute(f"DELETE FROM '{section}' WHERE list = '{name_product}'")
#     conn.commit()

#     cursor.execute(f"DROP TABLE '{product[2]}'")

#     # Close connection
#     cursor.close()
#     conn.close()


# def download_product(name_file, product):
#     conn = sqlite3.connect("base_ts.sqlite")
#     cursor = conn.cursor()

#     file = open(name_file, 'r')

#     for i in file:
#         cursor.execute(f"INSERT INTO '{product}' VALUES ('{i}', '{random.randint(111111, 999999)}')")

#     conn.commit()

#     file.close()
#     os.remove(name_file)

#     cursor.close()
#     conn.close()


# def basket(user_id):
#     conn = sqlite3.connect(settings.sqlite_file)
#     cursor = conn.cursor()
#     row = cursor.execute(f'SELECT * FROM purchase_information WHERE user_id = "{user_id}"').fetchall()

#     text = ''

#     for i in row:
#         text = text + '💠 ' + i[2][:10:] + ' | ' + i[1] + '\n\n'

#     return text



# def admin_info():
#     conn = sqlite3.connect(settings.sqlite_file)
#     cursor = conn.cursor()
#     row = cursor.execute(f'SELECT * FROM users').fetchone()

#     current_time = str(datetime.datetime.now())

#     amount_user_all = 0
#     amount_user_day = 0
#     amount_user_hour = 0

#     while row is not None:
#         amount_user_all += 1
#         if row[2][:-15:] == current_time[:-15:]:
#             amount_user_day += 1
#         if row[2][:-13:] == current_time[:-13:]:
#             amount_user_hour += 1

#         row = cursor.fetchone()

#     msg = '❕ Информация:\n\n' \
#           f'❕ Пользователей за все время: - {amount_user_all}\n' \
#           f'❕ За день - {amount_user_day}\n' \
#           f'❕ За час - {amount_user_hour}'

#     return msg

# def check_payment(user_id):
#     conn = sqlite3.connect(settings.sqlite_file)
#     cursor = conn.cursor()
#     try:
#         session = requests.Session()
#         session.headers['authorization'] = 'Bearer ' + settings.QIWI_TOKEN
#         parameters = {'rows': '5'}
#         h = session.get(
#             'https://edge.qiwi.com/payment-history/v1/persons/{}/payments'.format(settings.QIWI_NUMBER),
#             params=parameters)
#         req = json.loads(h.text)
#         result = cursor.execute(f'SELECT * FROM check_payment WHERE user_id = {user_id}').fetchone()
#         comment = result[1]

#         for i in range(len(req['data'])):
#             if comment in str(req['data'][i]['comment']):
#                 balance = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchone()

#                 balance = float(balance[5]) + float(req["data"][i]["sum"]["amount"])

#                 cursor.execute(f'UPDATE users SET balance = {balance} WHERE user_id = "{user_id}"')
#                 conn.commit()

#                 cursor.execute(f'DELETE FROM check_payment WHERE user_id = "{user_id}"')
#                 conn.commit()

#                 referral_web(user_id, float(req["data"][i]["sum"]["amount"]))

#                 return 1, req["data"][i]["sum"]["amount"]
#     except Exception as e:
#         print(e)

#     return 0, 0


# def replenish_balance(user_id):
#     conn = sqlite3.connect(settings.sqlite_file)
#     cursor = conn.cursor()

#     code = random.randint(1111111111, 9999999999)

#     cursor.execute(f'SELECT * FROM check_payment WHERE user_id = "{user_id}"')
#     row = cursor.fetchall()

#     if len(row) > 0:
#         cursor.execute(f'DELETE FROM check_payment WHERE user_id = "{user_id}"')
#         conn.commit()

#     cursor.execute(f'INSERT INTO check_payment VALUES ("{user_id}", "{code}", "0")')
#     conn.commit()

#     msg = settings.replenish_balance.format(
#         number=settings.QIWI_NUMBER,
#         code=code
#     )

#     return msg, code


# def cancel_payment(user_id):
#     conn = sqlite3.connect(settings.sqlite_file)
#     cursor = conn.cursor()

#     cursor.execute(f'DELETE FROM check_payment WHERE user_id = "{user_id}"')
#     conn.commit()


# def profile(user_id):
#     conn = sqlite3.connect(settings.sqlite_file)
#     cursor = conn.cursor()

#     row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchone()

#     return row


# def buy(dict):
#     conn = sqlite3.connect(settings.sqlite_file)
#     cursor = conn.cursor()

#     data = str(datetime.datetime.now())
#     list = ''
#     cursor.execute(f'SELECT * FROM "{dict.product}"')
#     row = cursor.fetchmany(int(dict.amount))

#     for i in range(int(dict.amount)):
#         list = list + f'💠 {data[:19]} | {row[i][0]}\n'


#         cursor.execute(f'INSERT INTO purchase_information VALUES ("{dict.user_id}", "{row[i][0]}", "{data}")')
#         conn.commit()

#         cursor.execute(f'DELETE FROM "{dict.product}" WHERE code = "{row[i][1]}"')
#         conn.commit()


#     balance = cursor.execute(f'SELECT * FROM users WHERE user_id = "{dict.user_id}"').fetchone()
#     balance = float(balance[5]) - (float(dict.price) * float(dict.amount))
#     cursor.execute(f'UPDATE users SET balance = "{balance}" WHERE user_id = "{dict.user_id}"')
#     conn.commit()

#     return list

# def give_balance(dict):
#     conn = sqlite3.connect(settings.sqlite_file)
#     cursor = conn.cursor()

#     cursor.execute(f'UPDATE users SET balance = "{dict.balance}" WHERE user_id = "{dict.login}"')
#     conn.commit()

# def check_balance(user_id, price):
#     conn = sqlite3.connect(settings.sqlite_file)
#     cursor = conn.cursor()

#     cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"')
#     row = cursor.fetchone()

#     if float(row[5]) >= float(price):
#         return 1
#     else:
#         return 0


# def list_sections():
#     conn = sqlite3.connect("base_ts.sqlite")
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM catalog')
#     row = cursor.fetchall()

#     sections = []

#     for i in row:
#         sections.append(i[1])

#     return sections


# def list_product():
#     conn = sqlite3.connect("base_ts.sqlite")
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM section')
#     row = cursor.fetchall()

#     list_product = []

#     for i in row:
#         list_product.append(i[2])

#     return list_product


# def check_ref_code(user_id):
#     conn = sqlite3.connect("base_ts.sqlite")
#     cursor = conn.cursor()

#     cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"')
#     user = cursor.fetchone()

#     if int(user[3]) == 0:
#         cursor.execute(f'UPDATE users SET ref_code = {user_id} WHERE user_id = "{user_id}"')
#         conn.commit()

#     return user_id
        

# def referral_web(user_id, deposit_sum):
#     conn = sqlite3.connect("base_ts.sqlite")
#     cursor = conn.cursor()

#     cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"')
#     user = cursor.fetchone()

#     if user[4] == '0':
#         return
#     else:
#         user2 = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user[4]}"').fetchone()

#         profit = (deposit_sum / 100) * float(settings.ref_percent)

#         balance = float(user[5]) + profit

#         cursor.execute(f'UPDATE users SET balance = {balance} WHERE user_id = "{user[4]}"')
#         conn.commit()

#         ref_log(user2[0], profit, user2[1])


# def ref_log(user_id, profit, name):
#     conn = sqlite3.connect("base_ts.sqlite")
#     cursor = conn.cursor()

#     cursor.execute(f'SELECT * FROM ref_log WHERE user_id = "{user_id}"')
#     user = cursor.fetchall()

#     if len(user) == 0:
#         cursor.execute(f'INSERT INTO ref_log VALUES ("{user_id}", "{profit}", "{name}")')
#         conn.commit()
#     else:
#         all_profit = user[0][1]

#         all_profit = float(all_profit) + float(profit)

#         cursor.execute(f'UPDATE ref_log SET all_profit = {all_profit} WHERE user_id = "{user_id}"')
#         conn.commit()


# def check_all_profit_user(user_id):
#     conn = sqlite3.connect("base_ts.sqlite")
#     cursor = conn.cursor()

#     cursor.execute(f'SELECT * FROM ref_log WHERE user_id = "{user_id}"')
#     user = cursor.fetchall()

#     if len(user) == 0:
#         return 0
#     else:
#         return user[0][1]


def admin_top_ref():
    conn = sqlite3.connect("base_ts.sqlite")
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM ref_log')
    users = cursor.fetchall()

    msg = '<b>Топ рефералов за все время:</b>\n' \

    for i in users:
        msg = msg + f'{i[0]}/{i[2]} - {i[1]} ₽\n'
    return msg