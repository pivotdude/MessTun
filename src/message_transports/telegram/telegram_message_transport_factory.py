from typing import Any
from src.config.base_config import BaseConfig
from .telegram_message_transport import TelegramMessageTransport

class TelegramMessageTransportFactory():
  """Factory for creating Telegram transport"""

  def __init__(self, base_config: BaseConfig):
    self.base_config = base_config



  def get_config_value(self, key: str) -> Any:
    """Getting configuration value by key with validation"""
    return self.base_config.get_config_value('message_transport.telegram.' + key)
  


  def get_config_value_safe(self, key: str, default_value: Any = None) -> Any:
    """Safe getting of configuration value by key"""
    return self.base_config.get_config_value_safe('message_transport.telegram.' + key, default_value)



  def create_transport(self) -> TelegramMessageTransport:
    """Creates and returns TelegramMessageTransport instance"""
    config = {
      'api_id': self.get_config_value("api_id"),
      'api_hash': self.get_config_value("api_hash"),
      'session_string': self.get_config_value("session_string"),
      'session_name': self.get_config_value_safe("session_name", "telegram_transport"),
      'peer_username': self.get_config_value("peer_username") 
    }
      
    return TelegramMessageTransport(config)
