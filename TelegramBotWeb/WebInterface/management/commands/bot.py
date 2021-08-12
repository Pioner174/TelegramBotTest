from django.core.management.base import BaseCommand
from django.conf import settings
import logging
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.utils.request import Request
import telegram

from ...models import Employee, Tmessages

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)

BOT_STATUS = False

default_keyboard_buttons = [
    [telegram.KeyboardButton('/start')],
    [telegram.KeyboardButton('/delete')],
]
def_key = telegram.ReplyKeyboardMarkup(default_keyboard_buttons, resize_keyboard=True)

def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e
    return inner


def start(update: Update, context: CallbackContext) -> None:
    """Команда старт для бота, если первый раз то поподает в базу, если нет то приветствие"""
    chat_id = update.message.chat_id    
    p, created = Employee.objects.update_or_create(
        t_user_id = chat_id,
        defaults={
            'nickname': update.message.from_user.username,
            'name': update.message.from_user.first_name,
            'surname': update.message.from_user.last_name,
            'is_delete': False,
        }
    )
    if (created):
        context.bot.send_message(
        chat_id=chat_id, text="Для простой регистрации предоставьте свой номер телефона",
        reply_markup=telegram.ReplyKeyboardMarkup([
            [telegram.KeyboardButton(text="Отправить свои контакт", request_contact=True)],["Отмена"]
        ], resize_keyboard=True, one_time_keyboard =True),
    )
    else:
        p.is_delete = False
        p.save()
        user = update.effective_user
        update.message.reply_markdown_v2(
        fr'Приветствую {user.mention_markdown_v2()}\!'
        )

def get_contact(update: Update, context: CallbackContext) -> None:
    num = "+"
    num += update.message.contact.phone_number
    chat_id = update.message.chat_id
    Employee.objects.update_or_create(
        t_user_id = chat_id,
        defaults={
            'telephone_telegram': num,
        }
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ваш номер телефона добавлен!")

def delete(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    Employee.objects.filter(t_user_id = chat_id).update(is_delete=True)
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'{user.mention_markdown_v2()}\! вы отключены от бота', reply_markup=def_key
        )
    

    


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def status(update: Update, context: CallbackContext) -> None:
    text_status = str( context.bot.get_me())
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_status)


def echo(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    sender_id = Employee.objects.filter(t_user_id =update.message.chat_id).get()
    text = update.message.text
    t_id = update.message.message_id
    m = Tmessages(t_message_id = t_id, sender = sender_id, 
        recipient = Employee.objects.filter(t_user_id = 1919630151).get(), text = text   # t_user_id = 1919630151  ид бота НАДО МЕНЯТЬ!
        ).save()


   
def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def bot_status():
    return BOT_STATUS
class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **kwargs):
        # 1 -- подключение
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        request.CON_POOL_SIZE = 10
        bot = Bot(
            request=request,
            token=settings.TOKEN,
            
            
        )


        # 2 -- обработчик
        updater = Updater(
            bot=bot,
            use_context=True, 
        )
        dispatcher = updater.dispatcher

        # on different commands - answer in Telegram
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))
        dispatcher.add_handler(CommandHandler("caps", caps))
        dispatcher.add_handler(CommandHandler("status", status))
        dispatcher.add_handler(CommandHandler("delete", delete))
        # on non command i.e message - echo the message on Telegram
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
        dispatcher.add_handler(MessageHandler(Filters.command, unknown))
        dispatcher.add_handler(MessageHandler(Filters.contact, get_contact))

        updater.start_polling()
        BOT_STATUS = True
        updater.idle()
        BOT_STATUS = False
        