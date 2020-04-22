## Шаблон для Телеграм ботов

Шаблон построен на базе библиотеки [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) и  фреймворка [falcon](https://falconframework.org) для приема вебхуков. Схема работы по-умолчанию – установка нового вебхука через API телеграм и прием данных через хуки. Не лонг-поллинг!

Шаблон включает в себя:

1. Поддержку локального запуска в виде [Docker](https://www.docker.com) контейнеров через docker-compose
2. Возможность разворачивания в [Heroku](https://www.heroku.com) в виде Docker образов через heroku.yml
3. Очереди в [Celery](http://www.celeryproject.org) с базовыми классами для быстрой разработки воркеров
4. Отправку статистики в [Sentry](https://sentry.io/) из коробки
5. Преднастроенный набор линтеров [flake-8](https://pypi.org/project/flake8/)
6. Базовые автотесты через [pytest](https://docs.pytest.org/)

## Подготовка к использованию

1. Исправить в файлах `docker-compose.yaml` и `infra/mongodb/mongo-init.js` тестовые логины и пароли для доступа к Mongodb
2. Скопировать файл с переменными окружения `.env.default` в `.env` и указать в нем актуальные значения для необходимых сервисов