import aiohttp
import base64
from typing import Dict, Any
from ..base_message_transport import MessageTransport

class VKMessageTransport(MessageTransport):
    """VK implementation of MessageTransport"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.access_token = config['access_token']
        self.peer_id = config['peer_id']
        self.api_version = config.get('api_version', '5.131')
        self.session = None
    
    async def connect(self) -> None:
        """Connect to VK"""
        self.session = aiohttp.ClientSession()
        self.running = True
        print("Connected to VK")
    
    async def send_data(self, data: bytes) -> None:
        """Send data via VK"""
        if not self.running or not self.session:
            return
        
        # VK specific encoding
        encoded_data = base64.b64encode(data).decode('utf-8')
        
        params = {
            'access_token': self.access_token,
            'v': self.api_version,
            'peer_id': self.peer_id,
            'message': encoded_data,
            'random_id': 0  # VK reqirement the random_id
        }
        
        async with self.session.post(
            'https://api.vk.com/method/messages.send', 
            params=params
        ) as response:
            pass  # Process response
    
    async def send_control(self, message: str) -> None:
        """Send control message via VK"""
        # VK specific logic for control messages
        control_message = f"--{message}"
        params = {
            'access_token': self.access_token,
            'v': self.api_version,
            'peer_id': self.peer_id,
            'message': control_message,
            'random_id': 0
        }
        
        if self.session:
            async with self.session.post(
                'https://api.vk.com/method/messages.send', 
                params=params
            ) as response:
                pass
    
    async def disconnect(self) -> None:
        """Disconnect from VK"""
        self.running = False
        if self.session:
            await self.session.close()