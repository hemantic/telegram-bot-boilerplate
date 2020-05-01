[![CircleCI](https://circleci.com/gh/wondersell/telegram-bot-boilerplate.svg?style=svg)](https://circleci.com/gh/wondersell/telegram-bot-boilerplate)

[![codecov](https://codecov.io/gh/wondersell/telegram-bot-boilerplate/branch/master/graph/badge.svg)](https://codecov.io/gh/wondersell/telegram-bot-boilerplate)


## Шаблон для Телеграм ботов

Шаблон построен на базе библиотеки [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) и  фреймворка [falcon](https://falconframework.org) для приема вебхуков. Схема работы по-умолчанию – установка нового вебхука через API телеграм и прием данных через хуки. Не лонг-поллинг!

Шаблон включает в себя:

1. Примеры базовых команд для бота
2. Сохранение пользователей и их команд в MongoDB, а так же базовые классы моделей [MongoEngine ORM](https://mongoengine-odm.readthedocs.io)
3. Очереди в [Celery](http://www.celeryproject.org) с базовыми классами для быстрой разработки воркеров
4. Поддержку локального запуска в виде [Docker](https://www.docker.com) контейнеров через docker-compose
5. Возможность разворачивания в [Heroku](https://www.heroku.com) в виде Docker образов через heroku.yml
6. Отправку статистики в [Sentry](https://sentry.io/) из коробки
7. Отправку продуктовых метрик в [Amplitude](https://amplitude.com)
7. Преднастроенный набор линтеров [flake-8](https://pypi.org/project/flake8/)
8. Базовые автотесты через [pytest](https://docs.pytest.org/)

## Подготовка к использованию

1. Исправить в файлах `docker-compose.yaml` и `infra/mongodb/mongo-init.js` тестовые логины и пароли для доступа к Mongodb
2. Скопировать файл с переменными окружения `.env.default` в `.env` и указать в нем актуальные значения для необходимых сервисов
3. Для включения деплоя на Heroku в файле `.circleci/config.yml` раскомментировать соответствующий блок в разделе `workflows`

## Развертывание через CircleCI

Бойлерплейт идет вместе с шаблоном для непрерывной интеграции через [CircleCI](https://circleci.com). Она включает в себя сборку приложения при любом обновлении любой ветки в следующем формате:

1. Сборку Docker контейнеров
2. Запуск автотестов
3. Запуск линтеров
4. Отправку результатов автотестов в [Codecov](https://codecov.io)
5. Публикацию приложения в Heroku, если обновилась ветка `master`

## Шпаргалка по командам

1. Запуск автотестов локально – `pytest`
2. Запуск линтеров – `flake8`
3. Запуск автоформатирования кода – `isort -rc .`
