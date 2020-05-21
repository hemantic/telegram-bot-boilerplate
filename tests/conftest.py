import json
from os import environ
from unittest.mock import patch

import mongoengine as me
import pytest
import requests_mock
from envparse import env
from falcon import testing
from telegram import Bot, Update

from src.models import User, log_command


@pytest.fixture
def telegram_json_message():
    def _telegram_json_message(message=None):
        with open('tests/mocks/tg_request_text.json') as f:
            json_body = f.read()
            json_data = json.loads(json_body)

            if message is not None:
                json_data['message']['text'] = message

            return json.dumps(json_data)
    return _telegram_json_message


@pytest.fixture
def telegram_json_message_without_surname():
    def _telegram_json_message(message=None):
        with open('tests/mocks/tg_request_text_without_surname.json') as f:
            json_body = f.read()
            json_data = json.loads(json_body)

            if message is not None:
                json_data['message']['text'] = message

            return json.dumps(json_data)
    return _telegram_json_message


@pytest.fixture
def telegram_json_command():
    def _telegram_json_command(command=None):
        with open('tests/mocks/tg_request_command.json') as f:
            json_body = f.read()
            json_data = json.loads(json_body)

            if command is not None:
                json_data['message']['text'] = command
                json_data['message']['entities'][0]['length'] = len(command)

            return json.dumps(json_data)

    return _telegram_json_command


@pytest.fixture
def telegram_json_callback():
    def _telegram_json_command(callback=None):
        with open('tests/mocks/tg_request_callback.json') as f:
            json_body = f.read()
            json_data = json.loads(json_body)

            if callback is not None:
                json_data['callback_query']['data'] = callback

            return json.dumps(json_data)

    return _telegram_json_command


@pytest.fixture
def telegram_update(telegram_json_message, telegram_json_command, telegram_json_callback):
    def _telegram_update(command=None, message=None, callback=None):
        telegram_json = telegram_json_message()

        if command is not None:
            telegram_json = telegram_json_command(command)

        if message is not None:
            telegram_json = telegram_json_message(message)

        if callback is not None:
            telegram_json = telegram_json_callback(callback)

        bot = Bot(env('TELEGRAM_API_TOKEN'))
        update = Update.de_json(json.loads(telegram_json), bot)

        return update

    return _telegram_update


@pytest.fixture
def telegram_update_without_surname(telegram_json_message_without_surname):
    def _telegram_update():
        telegram_json = telegram_json_message_without_surname()

        bot = Bot(env('TELEGRAM_API_TOKEN'))
        update = Update.de_json(json.loads(telegram_json), bot)

        return update

    return _telegram_update


@pytest.fixture
def create_telegram_command_logs(bot_user):
    def _create_telegram_catalog_logs(logs_count=1, command='/start', message='message'):
        for _ in range(logs_count):
            cmd = log_command(bot_user, command, message)
            cmd.set_status('success')

    return _create_telegram_catalog_logs


@pytest.fixture
def web_app():
    with patch('src.bot.reset_webhook'):
        from src import web
        return testing.TestClient(web.app)


@pytest.fixture(autouse=True)
def mongo(request):
    me.connection.disconnect()
    me.connect('mongotest', host='mongomock://localhost')


@pytest.fixture(autouse=True)
def requests_mocker():
    """Mock all requests.
    This is an autouse fixture so that tests can't accidentally
    perform real requests without being noticed.
    """
    with requests_mock.Mocker() as m:
        m.post('https://api.amplitude.com/2/httpapi', json={'code': 200})
        yield m


@pytest.fixture()
def bot_user():
    return User(
        chat_id=56473829,
        user_name='boilerplate_test_user',
        full_name='I am Dummy',
    ).save()


@pytest.fixture()
def set_amplitude():
    environ['AMPLITUDE_API_KEY'] = 'dummy_amplitude_key'
