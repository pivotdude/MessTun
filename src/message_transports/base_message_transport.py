from abc import ABC, abstractmethod
from typing import Callable, Optional
import asyncio


class MessageTransport(ABC):
    """Abstract base class for message transport"""
    
    def __init__(self):
        self._data_handler: Optional[Callable[[bytes], None]] = None
        self._control_handler: Optional[Callable[[str], None]] = None
        self.running = False
    
    @abstractmethod
    async def connect(self) -> None:
        """Connect to message service"""
        pass
    
    @abstractmethod
    async def send_data(self, data: bytes) -> None:
        """Send data (automatic encoding)"""
        pass
    
    @abstractmethod
    async def send_control(self, message: str) -> None:
        """Send control message"""
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from service"""
        pass
    
    def set_data_handler(self, handler: Callable[[bytes], None]) -> None:
        """Setup handler for data"""
        self._data_handler = handler
    
    def set_control_handler(self, handler: Callable[[str], None]) -> None:
        """Setup handler for control messages"""
        self._control_handler = handler
    
    async def _handle_incoming_data(self, data: bytes) -> None:
        """Internal method for processing data"""
        if self._data_handler:
            await asyncio.get_event_loop().run_in_executor(
                None, self._data_handler, data
            )
    
    async def _handle_incoming_control(self, message: str) -> None:
        """Internal method for processing control messages"""
        if self._control_handler:
            await asyncio.get_event_loop().run_in_executor(
                None, self._control_handler, message
            )
