import io
import logging
import tempfile
import numpy as np

from PIL import Image
from celery import Celery
from envparse import env
from moviepy.editor import *
from sentry_sdk.integrations.celery import CeleryIntegration
from telegram import Bot


env.read_envfile()

celery = Celery('tasks')
celery.conf.update(
    broker_url=env('REDIS_URL'),
    task_always_eager=env('CELERY_ALWAYS_EAGER', cast=bool, default=False),
    task_serializer='pickle',  # we transfer binary data like photos or voice messages,
    accept_content=['pickle'],
)

# включаем логи
logger = logging.getLogger(__name__)

bot = Bot(env('TELEGRAM_API_TOKEN'))
