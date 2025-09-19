import asyncio
from src.message_transports.base_message_transport import MessageTransport
from src.data_transports.base_data_transport import BaseDataTransport
from src.utils.statistics import TunnelStatistics

class TunnelManager:
    """Universal tunnel manager - works with ANY MessageTransport"""
    
    def __init__(self, message_transport: MessageTransport, 
                 data_transport: BaseDataTransport):
        # Dependency Injection - we get ready objects
        self.message_transport = message_transport
        self.data_transport = data_transport
        self.stats = TunnelStatistics()
        self.running = False
    
    async def start_tunnel(self) -> None:
        """Start tunnel - universal logic"""
        self.running = True
        
        # Setup handlers
        self.message_transport.set_data_handler(self._handle_message_data)
        self.message_transport.set_control_handler(self._handle_control_message)
        
        # Connect transports
        await self.data_transport.setup()
        await self.message_transport.connect()
        
        # Send ready signal
        await self.message_transport.send_control("ready")
        
        # Start main loop
        tasks = [
            asyncio.create_task(self._data_to_message_loop()),
            asyncio.create_task(self._heartbeat_loop())
        ]
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            await self.stop_tunnel()
    
    def _handle_message_data(self, data: bytes) -> None:
        """Processing data from MessageTransport - PURE LOGIC"""
        if not self.running:
            return
        
        try:
            # Write to data transport (TUN, SOCKS, etc.)
            asyncio.create_task(self.data_transport.write_data(data))
            self.stats.add_received(len(data))
        except Exception as e:
            print(f"Error writing to data transport: {e}")
    
    def _handle_control_message(self, message: str) -> None:
        """Processing control messages - PURE LOGIC"""
        if message == "ready":
            print("Peer is ready")
        elif message == "ping":
            asyncio.create_task(self.message_transport.send_control("pong"))
        elif message == "disconnect":
            asyncio.create_task(self.stop_tunnel())
    
    async def _data_to_message_loop(self) -> None:
        """Data transfer loop from DataTransport to MessageTransport"""
        while self.running:
            try:
                data = await self.data_transport.read_data()
                if data:
                    await self.message_transport.send_data(data)
                    self.stats.add_sent(len(data))
            except Exception as e:
                print(f"Data transport read error: {e}")
                await asyncio.sleep(0.1)
    
    async def _heartbeat_loop(self) -> None:
        """Connection maintenance"""
        while self.running:
            await asyncio.sleep(30)
            if self.running:  # Проверяем еще раз
                await self.message_transport.send_control("ping")
    
    async def stop_tunnel(self) -> None:
        """Stop tunnel"""
        self.running = False
        await self.data_transport.cleanup()
        await self.message_transport.disconnect()
        print(f"Tunnel stopped. {self.stats.get_summary()}")