from unittest.mock import patch

import pytest
from envparse import env


@pytest.mark.parametrize('command, expected_text', [
    ['/start', 'Ooops I did it again'],
    ['/help', 'Ooops I did it again'],
])
@patch('telegram.Bot.send_message')
def test_reply_commands(mocked_reply_text, web_app, telegram_json_command, command, expected_text):
    telegram_json = telegram_json_command(command=command)

    web_app.simulate_post('/' + env('TELEGRAM_API_TOKEN'), body=telegram_json)

    mocked_reply_text.assert_called()
    assert expected_text in mocked_reply_text.call_args.kwargs['text']


@pytest.mark.parametrize('message_text, expected_text', [
    ['Я просто мимокрокодил', 'Непонятная команда'],
])
@patch('telegram.Bot.send_message')
def test_reply_messages(mocked_bot_send_message, web_app, telegram_json_message, message_text, expected_text):
    telegram_json = telegram_json_message(message=str(message_text))

    web_app.simulate_post('/' + env('TELEGRAM_API_TOKEN'), body=telegram_json)

    assert expected_text in mocked_bot_send_message.call_args.kwargs['text']