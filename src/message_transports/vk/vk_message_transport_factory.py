from typing import Any
from .vk_message_transport import VKMessageTransport
from src.config.base_config import BaseConfig


class VKMessageTransportFactory():
    """Factory for creating VK message transport"""

    def __init__(self, base_config: BaseConfig):
        self.base_config = base_config

    def get_config_value(self, key: str) -> Any:
        """Getting configuration value by key with validation"""
        return self.base_config.get_config_value('message_transport.vk.' + key)
    
    def get_config_value_safe(self, key: str, default_value: Any = None) -> Any:
        """Safe getting of configuration value by key"""
        return self.base_config.get_config_value_safe('message_transport.vk.' + key, default_value)

    def create_transport(self) -> VKMessageTransport:
        """Creates and returns VKMessageTransport instance"""
        config = {
            'access_token': self.get_config_value("access_token"),
            'peer_id': self.get_config_value("peer_id"),
            'api_version': self.get_config_value_safe("api_version", "5.131")
        }
        
        return VKMessageTransport(config)