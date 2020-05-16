import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Dispatcher, Filters, MessageHandler

from . import tasks
from .models import log_command, user_get_by_update


def process_event(event, user):
    logger.info(event)
    tasks.track_amplitude.delay(chat_id=user.chat_id, event=event)


def process_command(name, user, text=''):
    # Здесь нужно перечислить все команды, которые понимает бот и перевести их в человекочитаемый вид
    # Это нужно для записи в логи и Amplitude
    slug_list = {
        'Started bot': 'help_start',
        'Sent unknown command': 'help_command_not_found',
    }

    log_item = log_command(user, slug_list[name], text)
    process_event(name, user)

    return log_item


# включаем логи
logger = logging.getLogger(__name__)


def help_start(update: Update, context: CallbackContext):
    user = user_get_by_update(update)
    process_command(name='Started bot', user=user)

    context.bot.send_message(
        chat_id=user.chat_id,
        text='Ooops I did it again. Чтобы бот начал что-то делать, нужно что-нибудь напрограммировать.',
    )


def help_command_not_found(update: Update, context: CallbackContext):
    user = user_get_by_update(update)
    process_command(name='Sent unknown command', user=user, text=update.message.text)

    context.bot.send_message(
        chat_id=user.chat_id,
        text='⚠️🤷 Непонятная команда.',
    )


def reset_webhook(bot, url, token):
    bot.delete_webhook()
    bot.set_webhook(url=url + token)


def start_bot(bot):
    dp = Dispatcher(bot, None, workers=0, use_context=True)

    dp.add_handler(CommandHandler('start', help_start))

    dp.add_handler(MessageHandler(Filters.all, help_command_not_found))

    return dp
