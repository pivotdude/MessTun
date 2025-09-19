import base64
from typing import Dict, Any
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from ..base_message_transport import MessageTransport

class TelegramMessageTransport(MessageTransport):
  """Telegram implementation of MessageTransport"""
    
  def __init__(self, config: Dict[str, Any]):
    super().__init__()
    self.api_id = config['api_id']
    self.api_hash = config['api_hash']
    self.peer_username = config['peer_username']
    self.session_string = config.get('session_string')
    self.session_name = config.get('session_name', 'telegram_transport')
    
    # Создание клиента
    if self.session_string:
      self.client = Client(
        name=self.session_name,
        api_id=self.api_id,
        api_hash=self.api_hash,
        session_string=self.session_string,
        in_memory=True,
      )
    else:
      self.client = Client(self.session_name, self.api_id, self.api_hash)



  async def connect(self) -> None:
    """Connect to Telegram"""
    await self.client.start()
    
    # Register message handler
    message_handler = MessageHandler(
      self._telegram_message_handler,
      filters.text
    )

    self.client.add_handler(message_handler)
    self.running = True
    
    print(f"Connected to Telegram as {(await self.client.get_me()).username}")    



  async def send_data(self, data: bytes) -> None:
    """Send data via Telegram"""
    if not self.running:
      return
    
    # Codec data to base64
    encoded_data = base64.b64encode(data).decode('utf-8')
    await self.client.send_message(self.peer_username, encoded_data)
  



  async def send_control(self, message: str) -> None:
    """Send control message"""
    if not self.running:
      return
    
    control_message = f"--{message}"
    await self.client.send_message(self.peer_username, control_message)
  


  
  async def _telegram_message_handler(self, client, message):
    """Telegram message handler - ALL TELEGRAM LOGIC IS HERE"""
    if not (message.from_user and message.from_user.username == self.peer_username and message.text):
      return
    
    # Process control messages
    if message.text.startswith('--'):
      control_msg = message.text[2:]  # Убираем "--"
      await self._handle_incoming_control(control_msg)
      return
    
    # Process data
    try:
      data = base64.b64decode(message.text)
      await self._handle_incoming_data(data)
    except Exception as e:
      print(f"Error decoding Telegram message: {e}")
    

    
  async def disconnect(self) -> None:
    """Disconnect from Telegram"""
    self.running = False
    if self.client:
      await self.client.stop()
