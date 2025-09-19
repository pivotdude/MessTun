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

3. **Configure settings**:
```yaml
message_transport:
  type: telegram
  telegram:
    api_id: your_api_id
    api_hash: your_api_hash
    peer_username: @recipient_username
    session_string: your_session_string
```

### TUN Interface Setup

1. **Prepare system**:
```bash
# For Linux/macOS
sudo apt-get install tunctl  # Debian/Ubuntu
# or
brew install tunctl         # macOS
```

2. **Run setup script**:
```bash
sudo bash bin/tun.sh
```

3. **Configure settings**:
```yaml
data_transport:
  type: tun
  tun:
    src_ip: 10.8.0.2
    dst_ip: 10.8.0.1
    mask: 255.255.255.0
    mtu: 1500
    interface_name: messtun
```

### Running

```bash
python main.py
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