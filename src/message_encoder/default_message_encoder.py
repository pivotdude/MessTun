import base64

class DefaultMessageEncoder:
    """Class for encoding/decoding messages"""
    
    @staticmethod
    def encode_data(data: bytes) -> str:
        """Encoding data to base64"""
        return base64.b64encode(data).decode('utf-8')
    
    @staticmethod
    def decode_data(encoded_data: str) -> bytes:
        """Decoding data from base64"""
        return base64.b64decode(encoded_data)
    
    @staticmethod
    def is_control_message(message: str) -> bool:
        """Check if message is control message"""
        return message.startswith('--')
