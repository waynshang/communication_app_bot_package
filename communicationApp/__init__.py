from communicationApp.telegram import Telegram
from typing import  Any


def createClient(app_name: str, **kwargs: Any):
  try:
    app_name = app_name.capitalize()
    klass = globals()[app_name]
    print(klass)
    return klass(**kwargs)
  except KeyError:
    return {"status_code": 404, "error": f"{app_name} is not support"}

