import logging

from celery import Celery
from envparse import env
from telegram import Bot

from .amplitude_helper import AmplitudeLogger
from .models import user_get_by

env.read_envfile()

celery = Celery('tasks')
celery.conf.update(
    broker_url=env('REDIS_URL'),
    task_always_eager=env('CELERY_ALWAYS_EAGER', cast=bool, default=False),
    task_serializer='pickle',  # we transfer binary data like photos or voice messages,
    accept_content=['pickle'],
)

# включаем Amplitude
if env('AMPLITUDE_API_KEY', default=None) is not None:
    amplitude = AmplitudeLogger(env('AMPLITUDE_API_KEY'))

# включаем логи
logger = logging.getLogger(__name__)

bot = Bot(env('TELEGRAM_API_TOKEN'))


@celery.task()
def track_amplitude(chat_id: int, event: str, event_properties=None, timestamp=None):
    if amplitude:
        user = user_get_by(chat_id=chat_id)
        amplitude.log(
            user_id=chat_id,
            event=event,
            user_properties={
                'Telegram chat ID': user.chat_id,
                'Name': user.full_name,
                'Telegram user name': user.user_name,
                'Daily catalog request limit': user.daily_catalog_requests_limit,
                'Subscribed to WB categories updates': user.subscribe_to_wb_categories_updates,
            },
            event_properties=event_properties,
            timestamp=timestamp,
        )
