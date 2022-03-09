
import requests
import datetime
import logging
import sqlite3
import asyncio
from utils import get_object_by_keys 

TELEGRAM_API = "https://api.telegram.org/bot"
GET_UPDATE = 'getUpdates'
SEND_MESSAGE = 'sendMessage'
class Telegram:
    def __init__(self, session_filename, id, hash, bot_token = None):
      super(type(self).__name__)
      self.bot_url = f"{TELEGRAM_API}{bot_token}/"
      self.connection = self.init_db
      self.cursor = self.connection.cursor()
      self._create_table

    def init_db(self):
      connection = sqlite3.connect("telegram.db")
      return connection

    async def send_message(self, text):
      try:
        self._get_chat_id()
        if type(text) == list:
          for t in text:
              self.send_message(self.chat_id, t)
        else:
          params = {'chat_id': self.chat_id, 'text': text, 'parse_mode': 'HTML'}
          method = SEND_MESSAGE
          resp = await requests.post(self.api_url + method, params)
      except Exception as Argument:
        filename = datetime.date.today().strftime("%Y-%m-%d")
        logging.basicConfig(filename=f'{filename}.log', encoding='utf-8', level=logging.DEBUG)
        logging.error("send_message exception", exc_info=True)
      return resp

    def get_response(self):
      get_result = self._get_all_responses()

      if len(get_result) > 0:
          last_update = get_result[0]
      else:
          last_update = None

      return last_update

    async def _get_all_responses(self, offset=0, timeout=30):
      result_json = []
      try:
        method = GET_UPDATE
        params = {'timeout': timeout, 'offset': offset}
        resp = await requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
      except Exception as Argument:
        filename = datetime.date.today().strftime("%Y-%m-%d")
        logging.basicConfig(filename=f'{filename}.log', encoding='utf-8', level=logging.DEBUG)
        logging.error("get_all_responses exception", exc_info=True)

      return result_json

    def _get_chat_id(self):
      if self.chat_id: return self.chat_id
      if self._select_chat_id: 
        self.chat_id =self._select_chat_id
        return self.chat_id
      else: 
        loop = asyncio.get_event_loop() #建立一個Event Loop
        results = loop.run_until_complete(self._get_all_responses)
        if results: 
          chat_id= get_object_by_keys(results[0], ["message", "chat", "id"])
          if chat_id: self.chat_id = chat_id
        return self.chat_id

    def _create_table(self):
      self.cursor.execute("CREATE TABLE IF NOT EXISTS telegram_chat_infos (chat_id INTEGER NOT NULL PRIMARY KEY, bot_token TEXT NOT NULL, first_name VARCHAR, last_name VARCHAR)")

    def _insert_chat_id(self, chat_id):
      self.cursor.execute(f"INSERT OR IGNORE INTO telegram_chat_infos (chat_id, bot_token) VALUES ({chat_id}, {self.bot_token})")

    def _update_chat_user_info(self, first_name, last_name, chat_id):
      self.cursor.execute(f"UPDATE telegram_chat_infos SET first_name = {first_name}, last_name= {last_name} WHERE chat_id = {chat_id}")

    def _select_chat_id(self):
      rows = self.cursor.execute(f"SELECT chat_id from telegram_chat_infos where bot_token = {self.bot_token}").fetchall()
      row = rows[0]
      if row: return list(row)[0]
      return None





    


