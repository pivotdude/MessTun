from src.config.base_config import BaseConfig
from src.data_transports.base_data_transport import BaseDataTransport


class DataTransportFactory:
    """Factory for creating data transport"""
    
    def __init__(self, base_config: BaseConfig):
        self.base_config = base_config

    def get_data_transport(self) -> BaseDataTransport:
        """Get data transport"""
        transport_type = self.base_config.get_config_value('data_transport.type')
        
        if transport_type == 'tun':
            from src.data_transports.tun.tun_data_transport_factory import TunDataTransportFactory
            return TunDataTransportFactory(self.base_config).create_transport()
        elif transport_type == 'socks':
            from src.data_transports.socks.socks_data_transport_factory import SocksDataTransportFactory
            return SocksDataTransportFactory(self.base_config).create_transport()
        
        raise ValueError(f"Unsupported data transport type: {transport_type}")