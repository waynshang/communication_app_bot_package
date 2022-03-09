
import requests
import datetime
import logging

TELEGRAM_API = "https://api.telegram.org/bot"
GET_UPDATE = 'getUpdates'
SEND_MESSAGE = 'sendMessage'
class Telegram:
    def __init__(self, session_filename, id, hash, bot_token = None):
      # token = '1632387033:AAEgUxJiAwZBRVXwVpocXohQOxZYFhkkR6g'
      super(type(self).__name__)
      self.bot_url = f"{TELEGRAM_API}{bot_token}/"

    async def send_message(self, text):
      try:
        if type(text) == list:
          for t in text:
              self.send_message(self.chat_id, t)
        else:
          params = {'chat_id': self.chat_id or 1230975396, 'text': text, 'parse_mode': 'HTML'}
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
    


