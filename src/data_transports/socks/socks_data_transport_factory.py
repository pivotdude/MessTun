from typing import Any, Callable, Optional
from .socks_data_transport import SocksTransport
from src.config.base_config import BaseConfig


class SocksDataTransportFactory():
    """Factory for creating SOCKS transport for incoming request processing"""

    def __init__(self, base_config: BaseConfig):
        self.base_config = base_config

    def get_config_value(self, key: str) -> Any:
        """Getting configuration value by key with validation"""
        return self.base_config.get_config_value('data_transport.socks.' + key)
    
    def get_config_value_safe(self, key: str, default_value: Any = None) -> Any:
        """Safe getting of configuration value by key"""
        return self.base_config.get_config_value_safe('data_transport.socks.' + key, default_value)

    def create_transport(self, request_handler: Optional[Callable] = None) -> SocksTransport:
        """Creates SocksTransport for processing incoming requests"""
        config = {
            'proxy_host': self.get_config_value_safe("proxy_host", "127.0.0.1"),
            'proxy_port': self.get_config_value_safe("proxy_port", 9050),
            'request_handler': request_handler  # Пользовательский обработчик запросов
        }
        
        return SocksTransport(config)

    def create_test_transport(self) -> SocksTransport:
        """Creates SocksTransport with built-in test request handler"""
        return self.create_transport(request_handler=SocksTransport.test_request_handler)