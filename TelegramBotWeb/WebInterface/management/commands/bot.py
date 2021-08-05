from django.core.management.base import BaseCommand
from django.conf import settings
import logging
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.utils.request import Request


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e
    return inner

@log_errors
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!'
    )

@log_errors
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

@log_errors
def status(update: Update, context: CallbackContext) -> None:
    text_status = str( context.bot.get_me())
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_status)

@log_errors
def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

@log_errors   
def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

@log_errors
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

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
        print(bot.get_me())


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
        # on non command i.e message - echo the message on Telegram
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
        dispatcher.add_handler(MessageHandler(Filters.command, unknown))

        updater.start_polling()
        updater.idle()