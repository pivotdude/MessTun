# MessTun - Universal Messenger Tunnel

**MessTun** is a hybrid tunneling tool that allows redirecting network traffic through popular messengers (Telegram, VK) using various transport protocols (TUN, SOCKS).

## 🎯 Purpose

MessTun is designed for secure bypass of network restrictions and censorship. Main use cases:

- **Bypassing blocks**: Routing traffic through messengers that are rarely blocked
- **Anonymization**: Hiding the real traffic source behind encrypted communication channels
- **Tunneling**: Creating virtual network interfaces for IP traffic redirection
- **Security testing**: Testing network infrastructure for penetration

## ✨ Key Features

### 🔄 Multi-protocol Support
- **Messengers**: Telegram and VKontakte
- **Transport protocols**: TUN interfaces and SOCKS5 proxy
- **Hybrid configurations**: Any combination of transport and messenger

### 🛡️ Security
- **Encryption**: Built-in Base64 encoding for data transmission
- **Control messages**: Connection management system through special commands
- **Statistics**: Monitoring traffic and tunnel uptime

### 🎛️ Flexible Configuration
- **YAML configuration**: Convenient settings management
- **Transport factories**: Extensible architecture for adding new protocols
- **Dependency Injection**: Clean architecture with dependency injection

## 🏗️ Architecture

```
MessTun
├── Message Transports    # Message transport
│   ├── Telegram          # Telegram API integration
│   └── VK                # VK API integration
├── Data Transports       # Data transport
│   ├── TUN               # Virtual network interfaces
│   └── SOCKS             # SOCKS5 proxy
├── Core                  # Core logic
│   └── TunnelManager     # Tunnel management
└── Utils                 # Utilities
    ├── Statistics        # Work statistics
    └── MessageEncoder    # Message encoding
```

## 🚀 Quick Start

### Requirements
- Python 3.8+
- sudo privileges for creating TUN interfaces
- Telegram or VK account for transport setup

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd MessTun
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure settings**:
```bash
cp config.example.yml config.yml
```

4. **Edit `config.yml`** with your data

## 🖥️ Server & Client Setup

MessTun works as a peer-to-peer tunnel where one side acts as the server and the other as the client. The setup depends on your transport configuration.

### Server Setup (Listener Side)

The server side listens for incoming connections and routes traffic through the messenger.

#### Telegram Server Configuration

```yaml
# Server config (listener side)
message_transport:
  type: telegram
  telegram:
    api_id: 12345678
    api_hash: your_api_hash
    peer_username: @your_server_bot  # Your bot that will receive messages
    session_string: your_session_string

data_transport:
  type: tun
  tun:
    src_ip: 10.8.0.1  # Server IP
    dst_ip: 10.8.0.2  # Client IP
    mask: 255.255.255.0
    mtu: 1500
    interface_name: messtun
```

#### VK Server Configuration

```yaml
# Server config (listener side)
message_transport:
  type: vk
  vk:
    access_token: your_server_access_token
    peer_id: 123456789  # Server's chat/user ID
    api_version: 5.131

data_transport:
  type: socks
  socks:
    proxy_host: 0.0.0.0  # Listen on all interfaces
    proxy_port: 1080     # SOCKS proxy port
    target_host: 0.0.0.0
    target_port: 0
```

### Client Setup (Connector Side)

The client side initiates the connection to the server through the messenger.

#### Telegram Client Configuration

```yaml
# Client config (connector side)
message_transport:
  type: telegram
  telegram:
    api_id: 12345678
    api_hash: your_api_hash
    peer_username: @your_server_bot  # Same bot as server
    session_string: your_session_string

data_transport:
  type: tun
  tun:
    src_ip: 10.8.0.2  # Client IP
    dst_ip: 10.8.0.1  # Server IP
    mask: 255.255.255.0
    mtu: 1500
    interface_name: messtun
```

#### VK Client Configuration

```yaml
# Client config (connector side)
message_transport:
  type: vk
  vk:
    access_token: your_client_access_token
    peer_id: 123456789  # Same chat/user ID as server
    api_version: 5.131

data_transport:
  type: socks
  socks:
    proxy_host: 127.0.0.1  # Local proxy
    proxy_port: 1080       # SOCKS proxy port
    target_host: example.com  # Target to connect through
    target_port: 80
```

### Telegram Transport Setup

1. **Get API credentials**:
   - Register an app with [@BotFather](https://t.me/BotFather)
   - Get `api_id` and `api_hash`

2. **Generate session string**:
```bash
cp .env.example .env
# Add API_ID and API_HASH to .env
python bin/generate_session.py
```

3. **Create a bot** for communication:
```bash
# Contact @BotFather
/newbot
# Follow the prompts to create your bot
```

### TUN Interface Setup

1. **Prepare system**:
```bash
# For Linux/macOS
sudo apt-get install tunctl  # Debian/Ubuntu
# or
brew install tunctl         # macOS
```

2. **Run setup script** (on both server and client for TUN mode):
```bash
sudo bash bin/tun.sh
```

### Running the Application

#### Server Mode
```bash
# Start the server (listener)
python main.py
```

#### Client Mode
```bash
# Start the client (connector)
python main.py
```

#### Systemd Service (Optional)

Create a service file for auto-start:

```bash
# /etc/systemd/system/messtun.service
[Unit]
Description=MessTun Tunnel Service
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/MessTun
ExecStart=/usr/bin/python3 /path/to/MessTun/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable messtun
sudo systemctl start messtun
```

## 💡 Usage Examples

### Example 1: TUN Tunnel (Full Network Access)

**Server Setup** (on your server):
```yaml
message_transport:
  type: telegram
  telegram:
    api_id: 12345678
    api_hash: your_api_hash
    peer_username: @your_tunnel_bot
    session_string: your_session_string

data_transport:
  type: tun
  tun:
    src_ip: 10.8.0.1
    dst_ip: 10.8.0.2
    mask: 255.255.255.0
    mtu: 1500
    interface_name: messtun
```

**Client Setup** (on your local machine):
```yaml
message_transport:
  type: telegram
  telegram:
    api_id: 12345678
    api_hash: your_api_hash
    peer_username: @your_tunnel_bot
    session_string: your_session_string

data_transport:
  type: tun
  tun:
    src_ip: 10.8.0.2
    dst_ip: 10.8.0.1
    mask: 255.255.255.0
    mtu: 1500
    interface_name: messtun
```

**Usage**:
```bash
# On client machine, configure routing
sudo ip route add default via 10.8.0.1

# Test connectivity
ping 8.8.8.8
curl https://example.com
```

### Example 2: SOCKS Proxy (Application-Level)

SOCKS mode creates a SOCKS5 proxy server that forwards traffic through the messenger. This is useful for application-level proxying without full network access.

**Server Setup** (SOCKS Proxy Server):
```yaml
message_transport:
  type: telegram
  telegram:
    api_id: 12345678
    api_hash: your_api_hash
    peer_username: @your_socks_bot
    session_string: your_session_string

data_transport:
  type: socks
  socks:
    proxy_host: 0.0.0.0      # Listen on all interfaces
    proxy_port: 1080         # SOCKS proxy port
    target_host: 0.0.0.0     # Will be set by connecting clients
    target_port: 0           # Will be set by connecting clients
```

**Client Setup** (SOCKS Proxy Client):
```yaml
message_transport:
  type: telegram
  telegram:
    api_id: 12345678
    api_hash: your_api_hash
    peer_username: @your_socks_bot
    session_string: your_session_string

data_transport:
  type: socks
  socks:
    proxy_host: 127.0.0.1    # Local SOCKS proxy
    proxy_port: 1080         # Same port as server
    target_host: example.com # Target server to connect to
    target_port: 443         # Target port
```

**Running SOCKS Mode**:

1. **Start the Server** (on your server/machine with internet access):
```bash
python main.py
# Server will start listening on 0.0.0.0:1080
```

2. **Start the Client** (on your restricted network machine):
```bash
python main.py
# Client will connect to server through Telegram
```

3. **Configure Applications to Use SOCKS Proxy**:

**For curl**:
```bash
curl --socks5 127.0.0.1:1080 https://example.com
curl --socks5-hostname 127.0.0.1:1080 https://example.com
```

**For wget**:
```bash
wget --execute="use_proxy on" --proxy=on --socks-proxy=127.0.0.1:1080 https://example.com
```

**For Firefox/Chrome**:
1. Go to proxy settings
2. Select "Manual proxy configuration"
3. Set SOCKS Host: `127.0.0.1` Port: `1080`
4. Check "Proxy DNS when using SOCKS v5"

**For system-wide proxy** (Linux):
```bash
# Set environment variables
export SOCKS_SERVER=127.0.0.1:1080
export ALL_PROXY=socks5://127.0.0.1:1080

# Or use proxychains
sudo apt-get install proxychains
sudo nano /etc/proxychains.conf
# Add: socks5  127.0.0.1 1080

# Use with any application
proxychains curl https://example.com
proxychains wget https://example.com
proxychains firefox
```

**Testing SOCKS Proxy**:
```bash
# Test basic connectivity
curl --socks5 127.0.0.1:1080 ifconfig.co

# Test specific protocols
curl --socks5 127.0.0.1:1080 https://api.ipify.org
nc -X 5 -x 127.0.0.1:1080 example.com 80

# Test DNS resolution through proxy
curl --socks5 127.0.0.1:1080 https://google.com
```

**SOCKS vs TUN Comparison**:

| Feature | SOCKS Mode | TUN Mode |
|---------|------------|----------|
| **Network Level** | Application level | Network layer |
| **Setup Complexity** | Simple | Complex (requires root) |
| **Performance** | Good for HTTP/HTTPS | Better for all protocols |
| **Protocol Support** | Limited to SOCKS5 | All IP protocols (TCP, UDP, ICMP) |
| **Configuration** | Per-application | System-wide |
| **Use Case** | Browser, specific apps | Full network access |
| **Firewall Bypass** | Limited | Complete |

### Example 3: Hybrid Setup (Telegram + SOCKS)

**Server**:
```yaml
message_transport:
  type: telegram
  telegram:
    api_id: 12345678
    api_hash: your_api_hash
    peer_username: @your_bot
    session_string: your_session_string

data_transport:
  type: socks
  socks:
    proxy_host: 0.0.0.0
    proxy_port: 9050
    target_host: 0.0.0.0
    target_port: 0
```

**Client**:
```yaml
message_transport:
  type: telegram
  telegram:
    api_id: 12345678
    api_hash: your_api_hash
    peer_username: @your_bot
    session_string: your_session_string

data_transport:
  type: socks
  socks:
    proxy_host: 127.0.0.1
    proxy_port: 9050
    target_host: example.com
    target_port: 443
```

### Example 4: Multiple Clients

You can set up multiple clients connecting to one server:

**Server Configuration**:
```yaml
# Server config (accepts multiple clients)
message_transport:
  type: telegram
  telegram:
    api_id: 12345678
    api_hash: your_api_hash
    peer_username: @multi_client_bot
    session_string: your_session_string

data_transport:
  type: tun
  tun:
    src_ip: 10.8.0.1
    dst_ip: 10.8.0.100  # Start range for clients
    mask: 255.255.255.0
    mtu: 1500
    interface_name: messtun
```

**Client 1**:
```yaml
data_transport:
  type: tun
  tun:
    src_ip: 10.8.0.100  # First client
    dst_ip: 10.8.0.1
    mask: 255.255.255.0
    mtu: 1500
    interface_name: messtun
```

**Client 2**:
```yaml
data_transport:
  type: tun
  tun:
    src_ip: 10.8.0.101  # Second client
    dst_ip: 10.8.0.1
    mask: 255.255.255.0
    mtu: 1500
    interface_name: messtun
```

## ⚙️ Configuration

### Configuration Example (Telegram + TUN)

```yaml
# MessTun Configuration

# Message Transport Settings
message_transport:
  type: telegram
  telegram:
    api_id: 12345678
    api_hash: your_api_hash
    peer_username: your_peer_username
    session_string: optional_session_string
    session_name: telegram_transport

# Data Transport Settings  
data_transport:
  type: tun
  tun:
    src_ip: 10.8.0.2
    dst_ip: 10.8.0.1
    mask: 255.255.255.0
    mtu: 1500
    interface_name: messtun

# General Settings
general:
  debug: false
  log_level: INFO
```

### Configuration Example (VK + SOCKS)

```yaml
message_transport:
  type: vk
  vk:
    access_token: your_vk_access_token
    peer_id: 123456789
    api_version: 5.131

data_transport:
  type: socks
  socks:
    proxy_host: 127.0.0.1
    proxy_port: 9050
    target_host: example.com
    target_port: 80
```

## 🔧 Supported Combinations

| Messenger | Transport | Description |
|-----------|-----------|-------------|
| Telegram  | TUN       | IP tunnel through Telegram |
| Telegram  | SOCKS     | Proxy tunnel through Telegram |
| VK        | TUN       | IP tunnel through VK |
| VK        | SOCKS     | Proxy tunnel through VK |

## 📊 Statistics

The application collects tunnel operation statistics:
- Uptime
- Bytes transferred
- Message count
- Transfer speed

Statistics are displayed when the tunnel stops.

## 🛡️ Security

- **Traffic encryption**: All data is Base64 encoded before sending
- **Authentication**: Access control through unique credentials
- **Leak protection**: Traffic isolation in encrypted channels
- **Connection control**: Ping-pong system for activity checking

## 📝 License

This project is distributed under the MIT license. See the [LICENSE](LICENSE) file for details.

## ⚠️ Important Notes

1. **Legality**: Use must comply with your country's laws
2. **Confidentiality**: Do not transmit sensitive data through unsecured channels
3. **Performance**: Tunneling through messengers may be slow
4. **Reliability**: Depends on messenger availability and internet connection quality

## 🤝 Contributing

Contributions are welcome! Please create issues and pull requests to improve the project.

## 📞 Contact

For questions and suggestions, please use the project's GitHub Issues system.