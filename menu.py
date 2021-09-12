import settings
import telebot
import random
#import functions as func
from telebot import types


# Main menu
main_menu = types.InlineKeyboardMarkup()
#main_menu.row(types.InlineKeyboardButton(text='Расписание на сегодня', callback_data='schedule_now'))
main_menu.row(
    types.InlineKeyboardButton(text='Расписание на завтра', callback_data='schedule_next'),
    types.InlineKeyboardButton(text='Расписание на неделю', callback_data='schedule_full'))
main_menu.row(
    types.InlineKeyboardButton(text='Профиль', callback_data='profile'),
    types.InlineKeyboardButton(text='Полезные ссылки', callback_data='links'))
main_menu.row(types.InlineKeyboardButton(text='Учителя группы', callback_data='teachers_group'))
main_menu.row(types.InlineKeyboardButton(text='Пожелания', callback_data='requests'))

main_menu_1 = types.InlineKeyboardMarkup()
#main_menu.row(types.InlineKeyboardButton(text='Расписание на сегодня', callback_data='schedule_now'))
main_menu_1.row(
    types.InlineKeyboardButton(text='Расписание на сегодня', callback_data='schedule_now'),
    types.InlineKeyboardButton(text='Расписание на неделю', callback_data='schedule_full'))
main_menu_1.row(
    types.InlineKeyboardButton(text='Профиль', callback_data='profile'),
    types.InlineKeyboardButton(text='Полезные ссылки', callback_data='links'))
main_menu_1.row(types.InlineKeyboardButton(text='Учителя группы', callback_data='teachers_group'))
main_menu_1.row(types.InlineKeyboardButton(text='Пожелания', callback_data='requests'))

main_menu_2 = types.InlineKeyboardMarkup()
#main_menu.row(types.InlineKeyboardButton(text='Расписание на сегодня', callback_data='schedule_now'))
main_menu_2.row(
    types.InlineKeyboardButton(text='Расписание на сегодня', callback_data='schedule_now'),
    types.InlineKeyboardButton(text='Расписание на завтра', callback_data='schedule_next'))
main_menu_2.row(
    types.InlineKeyboardButton(text='Профиль', callback_data='profile'),
    types.InlineKeyboardButton(text='Полезные ссылки', callback_data='links'))
main_menu_2.row(types.InlineKeyboardButton(text='Учителя группы', callback_data='teachers_group'))
main_menu_2.row(types.InlineKeyboardButton(text='Пожелания', callback_data='requests'))

main_menu_3 = types.InlineKeyboardMarkup()
main_menu_3.row(
    types.InlineKeyboardButton(text='Расписание на сегодня', callback_data='schedule_now'),
    types.InlineKeyboardButton(text='Расписание на завтра', callback_data='schedule_next'))
main_menu_3.row(
    types.InlineKeyboardButton(text='Расписание на неделю', callback_data='schedule_full'))
main_menu_3.row(
    types.InlineKeyboardButton(text='Профиль', callback_data='profile'))
main_menu_3.row(types.InlineKeyboardButton(text='Учителя группы', callback_data='teachers_group'))
main_menu_3.row(types.InlineKeyboardButton(text='Пожелания', callback_data='requests'))

main_menu_4 = types.InlineKeyboardMarkup()
main_menu_4.row(
    types.InlineKeyboardButton(text='Расписание на сегодня', callback_data='schedule_now'),
    types.InlineKeyboardButton(text='Расписание на завтра', callback_data='schedule_next'))
main_menu_4.row(
    types.InlineKeyboardButton(text='Расписание на неделю', callback_data='schedule_full'))
main_menu_4.row(
    types.InlineKeyboardButton(text='Профиль', callback_data='profile'))
main_menu_4.row(types.InlineKeyboardButton(text='Пожелания', callback_data='requests'))

profile = types.InlineKeyboardMarkup(row_width=2)
profile.add(
    types.InlineKeyboardButton(text='Настроить заново', callback_data='reset'),
    types.InlineKeyboardButton(text='Назад', callback_data='exit_to_menu')
)


# Admin menu
admin_menu = types.InlineKeyboardMarkup(row_width=2)
admin_menu.add(types.InlineKeyboardButton(text='Обновить расписание', callback_data='add_schedule'))
admin_menu.add(types.InlineKeyboardButton(text='Рассылка', callback_data='mail_to'))
admin_menu.add(types.InlineKeyboardButton(text='Заявки', callback_data='requests_view'))
admin_menu.add(types.InlineKeyboardButton(text='Скачать BD', callback_data='send_bd'))
admin_menu.add(
    types.InlineKeyboardButton(text='Информация', callback_data='admin_info'),
    types.InlineKeyboardButton(text='Выйти', callback_data='exit_to_menu')
)

type_week = types.InlineKeyboardMarkup(row_width=2)
type_week.add(
    types.InlineKeyboardButton(text='Верхняя(нечётная)', callback_data='week_1'),
    types.InlineKeyboardButton(text='Нижняя(четная)', callback_data='week_2')
)

requestBtn = types.InlineKeyboardMarkup(row_width=2)
requestBtn.add(
    types.InlineKeyboardButton(text='Назад', callback_data='exit_to_menu'),
    types.InlineKeyboardButton(text='Отправить', callback_data='send_request')
)

# Admin control
nazad = types.InlineKeyboardMarkup(row_width=1)
nazad.add(
    types.InlineKeyboardButton(text='Назад', callback_data='exit_to_menu')
)

# Back to admin menu
back_to_admin_menu = types.InlineKeyboardMarkup(row_width=1)
back_to_admin_menu.add(
    types.InlineKeyboardButton(text='Вернуться в админ меню', callback_data='back_to_admin_menu')
)

