from typing import Any
from .socks_data_transport import SocksTransport
from src.config.base_config import BaseConfig


class SocksDataTransportFactory():
    """Factory for creating SOCKS transport"""

    def __init__(self, base_config: BaseConfig):
        self.base_config = base_config

    def get_config_value(self, key: str) -> Any:
        """Getting configuration value by key with validation"""
        return self.base_config.get_config_value('data_transport.socks.' + key)
    
    def get_config_value_safe(self, key: str, default_value: Any = None) -> Any:
        """Safe getting of configuration value by key"""
        return self.base_config.get_config_value_safe('data_transport.socks.' + key, default_value)

    def create_transport(self) -> SocksTransport:
        """Creates and returns SocksTransport instance"""
        config = {
            'proxy_host': self.get_config_value_safe("proxy_host", "127.0.0.1"),
            'proxy_port': self.get_config_value_safe("proxy_port", 9050),
            'target_host': self.get_config_value("target_host"),
            'target_port': self.get_config_value("target_port")
        }
        
        return SocksTransport(config)