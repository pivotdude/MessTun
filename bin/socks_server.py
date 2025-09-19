import socket, threading, struct

def handle_socks(client):
    try:
        client.recv(262)
        client.send(b'\x05\x00')
        data = client.recv(1024)
        if data[1] == 1:  # CONNECT
            if data[3] == 1:  # IPv4
                addr = socket.inet_ntoa(data[4:8])
                port = struct.unpack('!H', data[8:10])[0]
            elif data[3] == 3:  # Domain
                addr_len = data[4]
                addr = data[5:5+addr_len].decode()
                port = struct.unpack('!H', data[5+addr_len:7+addr_len])[0]
            remote = socket.socket()
            remote.connect((addr, port))
            client.send(b'\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00')
            def forward(s1, s2):
                while True:
                    try: s2.send(s1.recv(4096))
                    except: break
            threading.Thread(target=forward, args=(client, remote)).start()
            threading.Thread(target=forward, args=(remote, client)).start()
    except: pass
server = socket.socket()
server.bind(('0.0.0.0', 1080))
server.listen(5)
print('SOCKS server on port 1080')
while True:
    client, addr = server.accept()
    threading.Thread(target=handle_socks, args=(client,)).start()