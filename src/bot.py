import logging
from telegram.ext import MessageHandler, Filters, Dispatcher, CallbackContext, CommandHandler
from telegram import Update
from .helpers import get_file


# включаем логи
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    logger.info('Start command received')

    update.message.reply_text(f'Ooops I did it again. Чтобы бот начал что-то делать, нужно что-нибудь напрограммировать.')


def sample_command(update: Update, context: CallbackContext):
    logger.info('Sample command received')

    update.message.reply_text(f'Получена тестовая команда')


def reset_webhook(bot, url, token):
    bot.delete_webhook()
    bot.set_webhook(url=url+token)


def start_bot(bot):
    dp = Dispatcher(bot, None, workers=0, use_context=True)

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.photo, sample_command))

    return dp
