from datetime import datetime

from envparse import env
from mongoengine import DateTimeField, Document, IntField, ReferenceField, StringField, connect
from telegram import Update

env.read_envfile()

connect(host=env('MONGODB_URI'))


def user_get_by(*args, **kwargs):
    return User.objects(*args, **kwargs).first()


def user_get_by_update(update: Update):
    if update.message:
        message = update.message
    else:
        message = update.callback_query.message

    matched = User.objects(chat_id=message.chat.id)

    if matched.count():
        return matched.first()

    full_name = ''
    if message.from_user.first_name:
        full_name += message.from_user.first_name
    if message.from_user.last_name:
        full_name += ' ' + message.from_user.last_name

    return User(
        chat_id=message.chat_id,
        user_name=message.from_user.username,
        full_name=full_name,
    ).save()


def log_command(user, command: str, message: str = ''):
    return LogCommandItem(
        user=user,
        command=command,
        message=message,
    ).save()


class User(Document):
    chat_id = IntField(required=True, primary_key=True)
    user_name = StringField()
    full_name = StringField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        """Add timestamps for creating and updating items."""
        if not self.created_at:
            self.created_at = datetime.now()

        self.updated_at = datetime.now()

        return super(User, self).save(*args, **kwargs)


class LogCommandItem(Document):
    user = ReferenceField(User)
    command = StringField()
    message = StringField()
    status = StringField()
    created_at = DateTimeField()

    def set_status(self, status):
        self.status = status
        self.save()
        return self

    def save(self, *args, **kwargs):
        """Add timestamps for creating and updating items."""
        if not self.created_at:
            self.created_at = datetime.now()

        return super(LogCommandItem, self).save(*args, **kwargs)
