import json
import falcon
import logging
from telegram import Bot, Update
from envparse import env

from .bot import reset_webhook, start_bot


logger = logging.getLogger(__name__)


class CallbackTelegramWebhook(object):
    def on_post(self, req, resp):
        bot_dispatcher.process_update(Update.de_json(json.load(req.bounded_stream), bot))

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'status': 'ok'})


class CallbackIndex(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'status': 'lucky_you'})


bot = Bot(env('TELEGRAM_API_TOKEN'))
reset_webhook(bot, env('TELEGRAM_WEBHOOKS_DOMAIN'), env('TELEGRAM_API_TOKEN'))
bot_dispatcher = start_bot(bot)

app = falcon.API()
app.req_options.auto_parse_form_urlencoded = True

app.add_route('/' + env('TELEGRAM_API_TOKEN'), CallbackTelegramWebhook())
app.add_route('/', CallbackIndex())