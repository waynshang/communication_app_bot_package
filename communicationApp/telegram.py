
import requests
import datetime
import logging
import sqlite3
import asyncio
from communicationApp.utils import get_object_by_keys 
from communicationApp.communicationApp import CommunicationApp
import os

TELEGRAM_API = "https://api.telegram.org/bot"
GET_UPDATE = 'getUpdates'
SEND_MESSAGE = 'sendMessage'
SEND_PHOTO= 'sendPhoto'
DEFAULT_DB = 'db/telegram.db'
DEFAULT_LOG_FILE = f"log/{datetime.date.today().strftime('%Y-%m-%d')}.log"
# 400 user error
# 404 exception
class Telegram(CommunicationApp):
  def __init__(self, **kwargs):
    bot_token = get_object_by_keys(kwargs, 'bot_token')
    db_name = get_object_by_keys(kwargs, 'db_name') or DEFAULT_DB
    log_file_name = get_object_by_keys(kwargs, 'log_file_name') or DEFAULT_LOG_FILE

    super().__init__(type(self).__name__)
    self.bot_token = bot_token
    self.bot_url = f"{TELEGRAM_API}{bot_token}/"
    self.db_name = db_name
    self.log_file_name = log_file_name
    self._create_folder(os.path.dirname(log_file_name))
    # db
    self._create_folder(os.path.dirname(db_name))
    self.connection = self.init_db()
    self.cursor = self.connection.cursor()
    self._create_table()
    self.chat_id = self._get_chat_id()
    

  def _create_folder(self, directory_name):
    try:
      os.stat(directory_name)
    except:
      os.mkdir(directory_name)

  def init_db(self):
    connection = sqlite3.connect(self.db_name)
    return connection
  
  def send_message(self, text):
    try:
      # print("chat_id----------", self.chat_id)
      result = {}
      if self.chat_id is None: return {"status_code": 400, "error": "Please send a message to bot"}
      if type(text) == list:
        result["status_code"] = 200
        result["data"] = []
        for t in text:
          message_result = self.send_message(t)
          if message_result["status_code"] == 200: 
            result["data"] = result["data"] + message_result["data"]
          else:
            return {**result, **message_result}
      else:
        
        params = {'chat_id': self.chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = SEND_MESSAGE
        response = requests.post(self.bot_url + method, params)
        result = self._handle_request(response)
    except Exception as Argument:

      logging.basicConfig(filename=self.log_file_name, level=logging.DEBUG)
      logging.error("send_message exception", exc_info=True)
      result= {"status_code": 404, "error": Argument}
    return result

  def send_photo(self, image_url: None, file_id: None, file: None):
    try:
      # print("chat_id----------", self.chat_id)
      result = {}
      if self.chat_id is None: return {"status_code": 400, "error": "Please send a message to bot"}
      if image_url is None and file_id is None and file is None: return {"status_code": 400, "error": "Please pass at least one file osurce"}

      photo = image_url
      if not photo: photo = file_id
      if not photo: photo = file 

      params = {'chat_id': self.chat_id, 'photo': photo, 'parse_mode': 'HTML'}
      method = SEND_PHOTO
      response = requests.post(self.bot_url + method, params)
      result = self._handle_request(response)
    except Exception as Argument:

      logging.basicConfig(filename=self.log_file_name, level=logging.DEBUG)
      logging.error("send_message exception", exc_info=True)
      result= {"status_code": 404, "error": Argument}
    return result

  def get_response(self, limit: int = 1):
    try:
      get_result =  self._get_all_responses()
      result = self._handle_request(get_result)
      if result.get("status_code") is not 200: return result
      if len(get_result) > 0:
        data = []
        if limit < 1: raise ValueError
        limit = min(len(get_result), limit)
        # start_index = -1 * limit
        # for i in range(limit):
        #   index  = start_index + i
        #   last_update = get_result[index]
        #   response_text = get_object_by_keys(last_update, ["message", "text"])
        #   response_user_info = get_object_by_keys(last_update, ["message", "from"])
        #   data.append({'response':{
        #     'text': response_text,
        #     'user_info': response_user_info
        #   }})
        start_index = len(get_result) - limit
        result['data'] = (result.get('data') or [])[start_index:]
      else:
        result = {"status_code": 400, "error": "Not found response"}
    except ValueError:
      result= {"status_code": 404, "error": "Please enter number over 0"}
    except Exception as Argument:
      logging.basicConfig(filename=self.log_file_name, level=logging.DEBUG)
      logging.error("send_message exception", exc_info=True)
      result= {"status_code": 404, "error": Argument}
    return result

  def _get_all_responses(self, offset=0, timeout=10):
    result_json = []
    try:
      method = GET_UPDATE
      params = {'timeout': timeout, 'offset': offset}
      resp = requests.get(self.bot_url + method, params)
      result_json = get_object_by_keys(resp.json(),'result')
    except Exception as Argument:
      logging.basicConfig(filename=self.log_file_name, encoding='utf-8', level=logging.DEBUG)
      logging.error("get_all_responses exception", exc_info=True)

    return result_json

  def _get_chat_id(self):
    # if self.chat_id: return self.chat_id
    select_result = self._select_chat_id()
    chat_id = None
    if select_result: 
      return select_result
    else: 
      results = self._get_all_responses()
      if results: 
        chat_id = get_object_by_keys(results[0], ["message", "chat", "id"])
        if chat_id: 
          first_name = get_object_by_keys(results[0], ["message", "chat", "id"])
          last_name = get_object_by_keys(results[0], ["message", "chat", "id"])
          self._insert_chat_id(chat_id)
          self._update_chat_user_info(first_name, last_name, chat_id)

      return chat_id

  def _create_table(self):
    self.cursor.execute("CREATE TABLE IF NOT EXISTS telegram_chat_infos (chat_id INTEGER NOT NULL PRIMARY KEY, bot_token TEXT NOT NULL, first_name VARCHAR, last_name VARCHAR)")
    self.connection.commit()

  def _insert_chat_id(self, chat_id):
    self.cursor.execute(f"INSERT OR IGNORE INTO telegram_chat_infos (chat_id, bot_token) VALUES ({chat_id}, '{self.bot_token}')")
    self.connection.commit()

  def _update_chat_user_info(self, first_name, last_name, chat_id):
    self.cursor.execute(f"UPDATE telegram_chat_infos SET first_name = '{first_name}', last_name= '{last_name}' WHERE chat_id = {chat_id}")
    self.connection.commit()  

  def _select_chat_id(self):
    rows = self.cursor.execute(f"SELECT chat_id from telegram_chat_infos where bot_token = '{self.bot_token}'").fetchall()
    if not rows: return None
    row = rows[0]
    if row: return list(row)[0]
    return None

  def _handle_request(self, response):
    if not response: return {"status_code": 404, "error": "missing response"}
    response = response.json()
    if not get_object_by_keys(response,'ok'): return {"status_code": response["error_code"], "error": response["description"]}
    result = get_object_by_keys(response,'result')
    user_info = get_object_by_keys(result,['message', 'from'])
    date = user_info = result.get('date')
    text = user_info = result.get('text')

    return {
      "status_code": 200,
      "data": [{
          user_info: user_info,
          date: date,
          text: text,
        }]
    }






    


