# Pupil's Helper Bot

Pupil's Helper Bot - это Telegram-бот, предназначенный для регистрации учеников, ввода и просмотра баллов ЕГЭ по предметам.

## Возможности

- Регистрация учеников
- Ввод баллов ЕГЭ для учеников
- Просмотр баллов ЕГЭ учеников

## Установка

1. Клонируйте репозиторий:

    ```sh
    git clone git clone https://github.com/Evkasonka/pupils_helper_bot.git
    cd Test_task_TG_bot
    ```

2. Создайте виртуальное окружение и активируйте его:

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # На Windows используйте `venv\Scripts\activate`
    ```

3. Установите необходимые зависимости:

    ```sh
    pip install -r requirements.txt
    ```

4. Создайте файл `.env` в корневом каталоге и добавьте туда ваш токен Telegram-бота:

    ```ini
    TELEGRAM_TOKEN=your_telegram_bot_token
    ```


## Использование

Запустите бота:

```sh
python main.py
