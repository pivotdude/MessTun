import asyncio
import sys
from src.config.base_config import BaseConfig
from src.message_transports.message_transport_factory import MessageTransportFactory
from src.data_transports.data_transport_factory import DataTransportFactory
from src.core.tunnel_manager import TunnelManager


async def main():
    """Main function with Dependency Injection"""
    try:
        config = BaseConfig()

        data_transport_factory = DataTransportFactory(config)
        data_transport = data_transport_factory.get_data_transport()

        message_transport_factory = MessageTransportFactory(config)
        message_transport = message_transport_factory.get_message_transport()

        # Dependency Injection in TunnelManager
        tunnel = TunnelManager(
            message_transport=message_transport,
            data_transport=data_transport
        )
        
        # Start tunnel
        await tunnel.start_tunnel()
        
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())