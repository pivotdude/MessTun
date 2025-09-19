import socket
import socks
import asyncio
from ..base_data_transport import BaseDataTransport
from typing import Any, Optional


class SocksTransport(BaseDataTransport):
    """SOCKS proxy transport"""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.socket: Optional[socket.socket] = None
        self.proxy_host = config.get("proxy_host", "127.0.0.1")
        self.proxy_port = config.get("proxy_port", 9050)
        self.target_host = config.get("target_host")
        self.target_port = config.get("target_port")

    async def setup(self) -> None:
        """Setup SOCKS connection"""
        if not self.target_host or not self.target_port:
            raise ValueError("target_host and target_port must be specified in configuration")
        
        self.socket = socks.socksocket()
        self.socket.set_proxy(socks.SOCKS5, self.proxy_host, self.proxy_port)
        await asyncio.get_event_loop().run_in_executor(
            None, self.socket.connect, (self.target_host, self.target_port)
        )
        print(f"connected to {self.target_host}:{self.target_port} successful")
        self.running = True

    async def read_data(self) -> bytes:
        """Reading data through SOCKS"""
        if not self.socket or not self.running:
            return b""

        return await asyncio.get_event_loop().run_in_executor(
            None, self.socket.recv, 4096
        )

    async def write_data(self, data: bytes) -> None:
        """Writing data through SOCKS"""
        if self.socket and self.running:
            try:
                await asyncio.get_event_loop().run_in_executor(None, self.socket.send, data)
            except (socket.error, OSError) as e:
                self.running = False
                raise ConnectionError(f"Error writing data through SOCKS: {e}")

    async def cleanup(self) -> None:
        """Closing SOCKS connection"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except (socket.error, OSError):
                pass  # Ignore errors when closing
