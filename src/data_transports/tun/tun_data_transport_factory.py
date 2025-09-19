from typing import Any
from .tun_data_transport import TunDataTransport
from src.config.base_config import BaseConfig


class TunDataTransportFactory():
    """Factory for creating TUN transport"""

    def __init__(self, base_config: BaseConfig):
        self.base_config = base_config

    def get_config_value(self, key: str) -> Any:
        """Getting configuration value by key with validation"""
        return self.base_config.get_config_value('data_transport.tun.' + key)
    
    def get_config_value_safe(self, key: str, default_value: Any = None) -> Any:
        """Safe getting of configuration value by key"""
        return self.base_config.get_config_value_safe('data_transport.tun.' + key, default_value)

    def create_transport(self) -> TunDataTransport:
        """Creates and returns TunDataTransport instance"""
        config = {
            'src_ip': self.get_config_value("src_ip"),
            'dst_ip': self.get_config_value("dst_ip"),
            'mask': self.get_config_value("mask"),
            'mtu': self.get_config_value("mtu"),
            'interface_name': self.get_config_value("interface_name")
        }
        
        return TunDataTransport(config)