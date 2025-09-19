from src.config.base_config import BaseConfig
from .base_message_transport import MessageTransport


class MessageTransportFactory():
    """Factory for creating message transport"""
    
    def __init__(self, base_config: BaseConfig):
        self.base_config = base_config

    def get_message_transport(self) -> MessageTransport:
        """Get message transport"""
        transport_type = self.base_config.get_config_value('message_transport.type')
        
        if transport_type == 'telegram':
            from .telegram.telegram_message_transport_factory import TelegramMessageTransportFactory
            return TelegramMessageTransportFactory(self.base_config).create_transport()
        elif transport_type == 'vk':
            from .vk.vk_message_transport_factory import VKMessageTransportFactory
            return VKMessageTransportFactory(self.base_config).create_transport()
        

        raise ValueError(f"Unsupported message transport type: {transport_type}")