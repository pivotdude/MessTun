from abc import ABC, abstractmethod
from typing import Any, Callable, Optional


class BaseDataTransport(ABC):
    """Abstract base class for all data transport types"""

    def __init__(self, config: dict[str, Any]):
        self.config: dict[str, Any] = config
        self.running: bool = False
        self._read_callback: Optional[Callable[[bytes], Any]] = None

    @abstractmethod
    async def setup(self) -> None:
        """Setup transport"""
        pass

    @abstractmethod
    async def read_data(self) -> bytes:
        """Read data from transport"""
        pass

    @abstractmethod
    async def write_data(self, data: bytes) -> None:
        """Write data to transport"""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass

    def set_read_callback(self, callback: Optional[Callable[[bytes], Any]]) -> None:
        """Setup callback for reading data"""
        self._read_callback = callback
