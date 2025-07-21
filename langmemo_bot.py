import os
import requests

from requests.exceptions import HTTPError
from dotenv import load_dotenv, set_key
from telebot import types, TeleBot

load_dotenv()

API_URL = os.getenv('API_URL')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = TeleBot(token=TELEGRAM_TOKEN)


class TokenAuthClient:
    def __init__(self, api_base=API_URL, env_path='.env'):
        self.api_base = api_base
        self.refresh_url = f'{self.api_base}/auth/jwt/refresh/'
        self.env_path = env_path

        self.access_token = os.getenv('ACCESS_TOKEN')
        self.refresh_token = os.getenv('REFRESH_TOKEN')

    def _get_headers(self):
        return {'Authorization': f'Bearer {self.access_token}'}

    def _save_tokens(self):
        set_key(self.env_path, 'ACCESS_TOKEN', self.access_token)
        set_key(self.env_path, 'REFRESH_TOKEN', self.refresh_token)

    def _refresh_tokens(self):
        resp = requests.post(self.refresh_url, json={'refresh': self.refresh_token})
        resp.raise_for_status()
        data = resp.json()
        self.access_token = data['access']
        self._save_tokens()

    def _request_with_refresh(self, method, path, **kwargs):
        url = f'{self.api_base}{path}'
        headers = kwargs.pop('headers', {})
        print('--------------------')
        print(headers)
        print('--------------------')
        headers.update(self._get_headers())
        print('--------------------')
        print(headers)
        print('--------------------')

        resp = requests.request(method, url, headers=headers, **kwargs)
        if resp.status_code == 401:
            self._refresh_tokens()
            headers = self._get_headers()
            resp = requests.request(method, url, headers=headers, **kwargs)

        resp.raise_for_status()
        return resp

    def get(self, path, **kwargs):
        return self._request_with_refresh('GET', path, **kwargs)

    def post(self, path, **kwargs):
        return self._request_with_refresh('POST', path, **kwargs)
    
client = TokenAuthClient(api_base=API_URL)

@bot.message_handler(commands=['start'])
def wake_up(message):
    chat_id = message.chat.id
    name = message.chat.first_name

    #keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #button_add_token = types.KeyboardButton('/add_token')
    #keyboard.add(button_add_token)

    bot.send_message(
        chat_id=chat_id,
        text=(f'Привет, {name}. Чтобы добавить токен LangMemo'
               ' пришли его.'),
        #reply_markup=keyboard,
    )

@bot.message_handler(regexp=r'^[A-Za-z0-9]{30}$')
def add_token(message):
    chat_id = message.chat.id
    name = message.chat.first_name

    payload = {'api_token': message.text, 'telegram_chat_id': str(chat_id)}
    try:
        resp = client.post(path='users/tg_token/', json=payload)
    except HTTPError as e:
        resp = f'Что-то пошло не так! {e}'
    print(resp)

    bot.send_message(
        chat_id=chat_id,
        text=(f'Привет, {name}. {resp}\n ')
        #reply_markup=keyboard,
    )


@bot.message_handler(regexp=r'^(?![A-Za-z0-9]{30}$).+')
def non_token_text(message):
    chat_id = message.chat.id
    name = message.chat.first_name

    #keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #button_add_token = types.KeyboardButton('/add_token')
    #keyboard.add(button_add_token)

    bot.send_message(
        chat_id=chat_id,
        text=(f'Привет, {name}. Токен не валиден!')
        #reply_markup=keyboard,
    )

def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()