from abc import ABC, abstractmethod

class CommunicationApp(ABC):

  def __init__(self, app):
    self.app = app

  @abstractmethod
  def send_message(self, text):
    pass
  @abstractmethod
  def get_response(self):
    pass
