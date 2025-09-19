import subprocess
from typing import Any, Optional
from pytun_pmd3 import TunTapDevice
from ..base_data_transport import BaseDataTransport


class TunDataTransport(BaseDataTransport):
    """TUN interface for IP packet tunneling"""

    def __init__(self, config: dict[str, Any]):
        super().__init__(config)
        self.tun: Optional[TunTapDevice] = None
        self.interface_name = config.get("interface_name", "teletun")

    async def setup(self) -> None:
        """Setup TUN interface"""
        src_ip = self.config.get("src_ip", "10.8.0.2")
        dst_ip = self.config.get("dst_ip", "10.8.0.1")
        mtu = self.config.get("mtu", 1500)
        
        # Check, that mtu is an integer
        try:
            mtu = int(mtu)
        except (ValueError, TypeError):
            raise ValueError(f"MTU must be an integer, received: {mtu}")

        try:
            # Create TUN interface
            _ = subprocess.run(
                ["sudo", "ip", "tuntap", "add", self.interface_name, "mode", "tun"],
                check=True,
                capture_output=True,
            )

            # Setup addresses
            _ = subprocess.run(
                [
                    "sudo",
                    "ip",
                    "addr",
                    "add",
                    f"{src_ip}",
                    "peer",
                    f"{dst_ip}",
                    "dev",
                    self.interface_name,
                ],
                check=True,
                capture_output=True,
            )

            # Bring interface up
            _ = subprocess.run(
                ["sudo", "ip", "link", "set", self.interface_name, "up"],
                check=True,
                capture_output=True,
            )

            self.tun = TunTapDevice(name=self.interface_name)
            self.tun.mtu = mtu
            print(f"connected to TUN interface {self.interface_name} successful")
            self.running = True

        except subprocess.CalledProcessError as e:
            # Try to use existing interface
            self.tun = TunTapDevice(name=self.interface_name)
            self.tun.mtu = mtu
            print(f"connected to TUN interface {self.interface_name} successful (using existing)")
            self.running = True
        except Exception as e:
            raise RuntimeError(f"Error setting up TUN interface: {e}")

    async def read_data(self) -> bytes:
        """Reading data from TUN interface"""
        if not self.tun or not self.running:
            return b""

        try:
            return self.tun.read(self.tun.mtu)
        except (OSError, IOError) as e:
            self.running = False
            raise ConnectionError(f"Error reading data from TUN interface: {e}")

    async def write_data(self, data: bytes) -> None:
        """Writing data to TUN interface"""
        if self.tun and self.running:
            try:
                self.tun.write(data)
            except (OSError, IOError) as e:
                self.running = False
                raise ConnectionError(f"Error writing data to TUN interface: {e}")

    async def cleanup(self) -> None:
        """Cleanup resources"""
        self.running = False
        if self.tun:
            try:
                self.tun.close()
            except (OSError, IOError):
                pass  # Ignore errors when closing
