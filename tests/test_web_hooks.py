from unittest.mock import MagicMock, patch

import pytest
from envparse import env


@pytest.fixture()
def bot_app(bot):
    """Our bot app, adds the magic curring `call` method to call it with fake bot"""
    from src import bot as bot_methods
    setattr(bot_methods, 'call', lambda method, *args, **kwargs: getattr(bot_methods, method)(bot, *args, **kwargs))  # noqa
    return bot_methods


@pytest.fixture
def bot():
    """Mocked instance of the bot."""

    class Bot:
        send_message = MagicMock()
        delete_webhook = MagicMock()
        set_webhook = MagicMock()

    return Bot()


@patch('telegram.ext.Dispatcher.process_update')
@patch('telegram.Update.de_json')
def test_telegram_webhook(mocked_de_json, mocked_process_update, web_app):
    with open('tests/mocks/tg_request_text.json') as f:
        json_body = f.read()
        got = web_app.simulate_post('/' + env('TELEGRAM_API_TOKEN'), body=json_body)

        mocked_de_json.assert_called()
        mocked_process_update.assert_called()
        assert got.status_code == 200


def test_index_page(web_app):
    got = web_app.simulate_get('/')

    assert got.status_code == 200
    assert 'lucky_you' in got.text


@patch('telegram.Bot.delete_webhook')
@patch('telegram.Bot.set_webhook')
def test_setting_webhooks(mocked_set_webhook, mocked_delete_webhook):
    from src.bot import reset_webhook
    from telegram import Bot

    bot = Bot(env('TELEGRAM_API_TOKEN'))
    reset_webhook(bot, 'https://wondersell.ru/', 'SUPERSECRETTOCKEN')

    mocked_delete_webhook.assert_called()
    mocked_set_webhook.assert_called()
