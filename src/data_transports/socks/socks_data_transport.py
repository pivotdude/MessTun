import socket
import socks
import asyncio
from ..base_data_transport import BaseDataTransport
from typing import Any, Optional, Callable


class SocksTransport(BaseDataTransport):
    """SOCKS proxy client transport для обработки входящих запросов"""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.socket: Optional[socket.socket] = None
        self.proxy_host = config.get("proxy_host", "127.0.0.1")
        self.proxy_port = config.get("proxy_port", 9050)
        # Убираем target_host и target_port - они не нужны
        self.request_handler: Optional[Callable] = config.get("request_handler")

    async def setup(self) -> None:
        """Setup SOCKS connection для прослушивания входящих данных"""
        self.socket = socks.socksocket()
        self.socket.set_proxy(socks.SOCKS5, self.proxy_host, self.proxy_port)
        
        # Подключаемся к SOCKS серверу без конкретного адреса назначения
        # Сервер будет перенаправлять нам входящие запросы
        try:
            # Устанавливаем соединение с прокси
            await asyncio.get_event_loop().run_in_executor(
                None, self.socket.connect, (self.proxy_host, self.proxy_port)
            )
            print(f"Connected to SOCKS proxy {self.proxy_host}:{self.proxy_port}")
            self.running = True
            
            # Запускаем обработку входящих данных
            asyncio.create_task(self.listen_for_incoming_data())
            
        except Exception as e:
            print(f"Failed to connect to SOCKS proxy: {e}")
            raise

    async def listen_for_incoming_data(self) -> None:
        """Прослушивает входящие данные от SOCKS сервера"""
        while self.running:
            try:
                # Читаем данные от прокси сервера
                data = await self.read_data()
                if data:
                    # Обрабатываем входящий запрос
                    await self.process_incoming_request(data)
                else:
                    # Если данных нет, небольшая пауза
                    await asyncio.sleep(0.1)
                    
            except Exception as e:
                print(f"Error listening for incoming data: {e}")
                if self.running:
                    await asyncio.sleep(1)  # Пауза перед повторной попыткой

    async def process_incoming_request(self, data: bytes) -> None:
        """Обрабатывает входящий запрос от клиента через прокси"""
        try:
            # Здесь ваша логика обработки входящих запросов
            print(f"Received data: {len(data)} bytes")
            
            if self.request_handler:
                # Используем пользовательский обработчик
                response = await self.request_handler(data)
                if response:
                    await self.write_data(response)
            else:
                # Базовая обработка - просто логируем
                print(f"Raw data: {data[:100]}...")  # Первые 100 байт
                
                # Отправляем простой ответ обратно
                response = b"HTTP/1.1 200 OK\r\nContent-Length: 12\r\n\r\nHello World!"
                await self.write_data(response)
                
        except Exception as e:
            print(f"Error processing incoming request: {e}")

    async def read_data(self) -> bytes:
        """Reading data from SOCKS proxy"""
        if not self.socket or not self.running:
            return b""

        try:
            # Используем неблокирующий режим для чтения
            data = await asyncio.get_event_loop().run_in_executor(
                None, self.socket.recv, 4096
            )
            return data
        except (socket.error, OSError) as e:
            if self.running:
                print(f"Error reading data: {e}")
            return b""

    async def write_data(self, data: bytes) -> None:
        """Writing response data back through SOCKS"""
        if self.socket and self.running:
            try:
                await asyncio.get_event_loop().run_in_executor(
                    None, self.socket.send, data
                )
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

    @staticmethod
    async def test_request_handler(data: bytes) -> bytes:
        """Test request handler for SOCKS proxy"""
        try:
            # Analyze request data
            request_str = data.decode('utf-8', errors='ignore')
            print(f"Processing test request: {request_str[:200]}...")
            
            # Process request
            if data.startswith(b'GET '):
                # Process GET requests
                if b'/hello' in data:
                    response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello from SOCKS proxy!"
                elif b'/status' in data:
                    response = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"status\": \"ok\", \"proxy\": \"running\"}"
                else:
                    response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nSOCKS proxy test endpoint"
                    
            elif data.startswith(b'POST '):
                # Process POST requests
                response = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"received\": true, \"length\": " + str(len(data)).encode() + b"}"
                
            elif b'SOCKS' in data:
                # Process SOCKS requests
                response = b"SOCKS5 response: Connection established"
                
            else:
                # Process unknown requests
                response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nUnknown request type handled by SOCKS proxy"
            
            print(f"Sending response: {len(response)} bytes")
            return response
            
        except Exception as e:
            print(f"Error in test request handler: {e}")
            return b"HTTP/1.1 500 Internal Server Error\r\n\r\nError processing request"
