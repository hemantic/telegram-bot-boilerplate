from datetime import datetime

from freezegun import freeze_time

from src.models import LogCommandItem, User, log_command, user_get_by, user_get_by_update


def test_user_get_by_chat_id():
    u_created = User(chat_id='1234').save()

    u_fetched = user_get_by(chat_id='1234')

    assert u_created == u_fetched


@freeze_time('2030-01-15')
def test_user_created_updated_at():
    user = User(chat_id='12345').save()

    assert user.created_at == datetime(2030, 1, 15)
    assert user.updated_at == datetime(2030, 1, 15)


@freeze_time('2030-01-15')
def test_user_updated_at_changing():
    user = User(chat_id='123456').save()

    assert user.updated_at == datetime(2030, 1, 15)

    with freeze_time('2030-06-15'):
        user.full_name = 'Oh my dummy'
        user.save()
        assert user.updated_at == datetime(2030, 6, 15)
        assert user.created_at == datetime(2030, 1, 15)


@freeze_time('2030-01-15')
def test_log_command_item_created_at():
    lci = LogCommandItem(command='/start').save()

    assert lci.created_at == datetime(2030, 1, 15)


@freeze_time('2030-01-15')
def test_log_command_item_created_at_existing():
    lci = LogCommandItem(command='/start').save()

    with freeze_time('2030-06-15'):
        lci.message = 'Oh my dummy'
        lci.save()
        assert lci.created_at == datetime(2030, 1, 15)


def test_telegram_update_fixture_message(telegram_update):
    update = telegram_update(message='Um, hi!')

    assert update.message.text == 'Um, hi!'


def test_telegram_update_fixture_command(telegram_update):
    update = telegram_update(command='/start')

    assert update.message.text == '/start'


def test_user_get_by_update_empty(telegram_update):
    update = telegram_update(message='Um, hi!')

    user = user_get_by_update(update)

    assert isinstance(user, User)
    assert user.chat_id == 987654321
    assert user.user_name == 'vasisualiy_is_my_name'
    assert user.full_name == 'Акакий Акакиевич'


def test_user_get_by_update_without_surname(telegram_update_without_surname):
    update = telegram_update_without_surname()

    user = user_get_by_update(update)

    assert isinstance(user, User)
    assert user.chat_id == 98765432
    assert user.user_name == 'username'
    assert user.full_name == 'GlobBlob'


def test_user_log_command(bot_user):
    log_command(bot_user, '/start', 'Hi')
    log_command(bot_user, '/stop', 'Bye')

    all_commands = LogCommandItem.objects(user=bot_user.id)

    assert all_commands.count() == 2
    assert all_commands.first()['message'] == 'Hi'
