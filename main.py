from telegram import Update
from telegram.ext import Updater, CommandHandler, Filters, CallbackContext, MessageHandler
import bottoken as token
import json


def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(f'Введите имя, чтобы найти телефон, либо используйте команды: \
\n/start - проверка работоспособности бота\n/help - помощь\n/all - вывести всю записную книжку \
\n/sort - вывести всю записную книжку, отсортированную по алфавиту\n/add [имя] [номер телефона]\
 - добавить новую запись\n/del [имя] - удалить запись\n/format - стереть всю записную книжку\
 (Осторожно! Данные будет не восстановить)')


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello, {update.effective_user.first_name}')


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'К работе готов')


def dict2(update: Update, context: CallbackContext):
    if(update.message.text in dict1):
        update.message.reply_text(dict1[update.message.text])
    else:
        try:
            update.message.reply_text(eval(update.message.text))
        except:
            update.message.reply_text("Не понятно")


def add_new(update: Update, context: CallbackContext):
    global dict1
    msg = update.message.text
    print(msg)
    items = msg.split()  # /add_new 123 534543
    if len(items) == 2:
        update.message.reply_text("Неправильный формат ввода")
        return
    if len(items) == 3:
        new_name = items[1]
        new_tel = items[2]
    elif len(items) == 4:
        new_name = items[1] + ' ' + items[2]
        new_tel = items[3]
    elif len(items) == 5:
        new_name = items[1] + ' ' + items[2] + ' ' + items[3]
        new_tel = items[4]
    dict1[new_name] = new_tel
    with open('phone_number.json', 'w', encoding='utf-8') as fp:
        dict = json.dump(dict1, fp, indent=2, ensure_ascii=False)
    print('--- В записную книжку добавлена новая запись ---')
    update.message.reply_text("Новая запись добавлена успешно")


def show_all(update: Update, context: CallbackContext):
    global dict1
    print('------- Вывод всей записной книжки ------')
    if len(dict1) == 0:
        update.message.reply_text("Записная книжка пустая")
    else:
        for key, value in dict1.items():
            update.message.reply_text(key + ': ' + value)


def show_all_sorted(update: Update, context: CallbackContext):
    global dict1
    print('--- Вывод отсортированной записной книжки ---')
    if len(dict1) == 0:
        update.message.reply_text("Записная книжка пустая")
    else:
        sorted_dict = dict(sorted(dict1.items()))
        for key, value in sorted_dict.items():
            update.message.reply_text(key + ': ' + value)


def del_name(update: Update, context: CallbackContext):
    global dict1
    msg = update.message.text
    print(msg)
    items = msg.split()  # /add_new 123
    del_name = items[1]
    if del_name in dict1:
        dict1.pop(del_name)
        update.message.reply_text("Запись успешно удалена")
        with open('phone_number.json', 'w', encoding='utf-8') as fp:
            dict = json.dump(dict1, fp, indent=2, ensure_ascii=False)
        print('------- Запись успешно удалена ------')
    else:
        update.message.reply_text("Такого имени не нашлось")


def format_all(update: Update, context: CallbackContext):
    global dict1
    msg = update.message.text
    print(msg)
    answer = msg.split()  # /del 123
    if len(answer) > 1:
        if answer[1] == "да":
            with open('phone_number.json', 'w') as fp:
                data_to_json = '''{}'''
                dict1 = json.loads(data_to_json)
                data = json.dump(dict1, fp)
            print('---- Записная книжка успешно удалена ----')
            update.message.reply_text("Записная книжка успешно удалена")
        else:
            update.message.reply_text("Отмена стирания записной книжки")
    else:
        update.message.reply_text("ВНИМАНИЕ! Вы действительно хотите стереть всю записную книжку?\
 Если да, то введите /format да")
        print('---- Попытка удаления записной книжки ----')


print('---------------- Старт -----------------')
with open('phone_number.json', 'r') as f:
    dict1 = json.load(f)
    print('--- Записная книжка подгружена успешно ---')
updater = Updater(token.token)
updater.dispatcher.add_handler(CommandHandler('help', help_command))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('all', show_all))
updater.dispatcher.add_handler(CommandHandler('sort', show_all_sorted))
updater.dispatcher.add_handler(CommandHandler('add', add_new))
updater.dispatcher.add_handler(CommandHandler('del', del_name))
updater.dispatcher.add_handler(CommandHandler('format', format_all))
updater.dispatcher.add_handler(MessageHandler(Filters.text, dict2))
updater.start_polling()
updater.idle()