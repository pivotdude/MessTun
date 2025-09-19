import time

class TunnelStatistics:
    """Class for collecting tunnel statistics"""
    
    def __init__(self):
        self.start_time = time.time()
        self.bytes_sent = 0
        self.bytes_received = 0
        self.messages_sent = 0
        self.messages_received = 0
    
    def add_sent(self, bytes_count: int) -> None:
        """Add sent data"""
        self.bytes_sent += bytes_count
        self.messages_sent += 1
    
    def add_received(self, bytes_count: int) -> None:
        """Add received data"""
        self.bytes_received += bytes_count
        self.messages_received += 1
    
    def get_summary(self) -> str:
        """Get statistics summary"""
        uptime = time.time() - self.start_time
        return (f"Uptime: {uptime:.1f}s, "
                f"Sent: {self.bytes_sent} bytes ({self.messages_sent} msgs), "
                f"Received: {self.bytes_received} bytes ({self.messages_received} msgs)")
