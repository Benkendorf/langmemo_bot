# LangMemo Bot (WIP)
LangMemo Bot - бот-компаньон [проекта LangMemo](https://github.com/Benkendorf/langmemo) в Telegram, с помощью которого пользователь сможет проверять информацию о своем профиле в удобном формате мессенджера.

Аккаунт в Telegram привязывается к учетной записи LangMemo при помощи токена, генерируемого на сайте.

## Стек технологий

- Python 3.9
- pyTelegramBotAPI 4.26.0


## Локальный запуск

```bash
# 1. Клонируем репозиторий
git clone git@github.com:Benkendorf/foodgram.git

# 2. Настраиваем окружение и устанавливаем зависимости
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

# 3. Запускаем проект
python langmemo_bot.py
