import socket
import threading
import struct
import select
import redis
import random

SOCKS_VERSION = 5

class Socks5Server:
    def __init__(self, host='192.168.3.137', port=1080, redis_host='localhost', redis_port=6379, redis_password='Aa987987.', redis_db=8):
        self.host = host
        self.port = port
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, db=redis_db)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f'SOCKS5 server started on {self.host}:{self.port}')
        self.username = "tkniubi"
        self.password = "aa987987"

    def get_proxy(self):
        try:
            proxy_ips = list(self.redis_client.smembers("proxy:ips"))
            if proxy_ips:
                proxy_url = random.choice(proxy_ips).decode('utf-8')
                print(f"Using proxy URL: {proxy_url}")
                # 解析 SOCKS5 URL，提取用户名、密码、IP 和端口
                proxy_info = proxy_url.split('://')[1]
                auth_info, proxy_ip_port = proxy_info.split('@')
                username, password = auth_info.split(':')
                proxy_ip, proxy_port = proxy_ip_port.split(':')
                return proxy_ip, int(proxy_port), username, password
            else:
                print("No proxy IPs found in Redis")
                return None, None, None, None
        except Exception as e:
            print(f"Error fetching proxy IP: {e}")
            return None, None, None, None

    def handle_client(self, client_socket):
        try:
            # 读取初始 SOCKS5 握手请求
            request = client_socket.recv(4096)
            if request[0] != SOCKS_VERSION:
                client_socket.close()
                return

            nmethods = request[1]
            methods = request[2:2 + nmethods]

            # 检查是否支持用户名/密码认证方式，不支持则断开连接
            if 2 not in set(methods):
                client_socket.sendall(struct.pack("!BB", SOCKS_VERSION, 0xFF))
                client_socket.close()
                return

            # 发送协商响应数据包
            client_socket.sendall(struct.pack("!BB", SOCKS_VERSION, 2))

            # 校验用户名和密码
            if not self.verify_credentials(client_socket):
                return

            # 读取客户端的请求
            request = client_socket.recv(4096)
            mode = request[1]
            if mode != 1:  # 仅支持 CONNECT 请求
                client_socket.close()
                return

            addr_type = request[3]
            if addr_type == 1:  # IPv4
                address = socket.inet_ntoa(request[4:8])
                port = int.from_bytes(request[8:10], 'big')
            elif addr_type == 3:  # 域名
                domain_length = request[4]
                address = request[5:5 + domain_length].decode()
                port = int.from_bytes(request[5 + domain_length:5 + domain_length + 2], 'big')
            else:
                client_socket.close()
                return

            # 获取代理 IP 地址和端口以及认证信息
            proxy_ip, proxy_port, username, password = self.get_proxy()
            if proxy_ip is None:
                client_socket.close()
                return

            # 连接到代理服务器
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.connect((proxy_ip, proxy_port))

            # 发送 SOCKS5 认证请求
            remote_socket.sendall(b"\x05\x01\x02")
            response = remote_socket.recv(4096)
            if response[1] != 0x02:
                client_socket.close()
                return

            # 发送用户名和密码认证
            remote_socket.sendall(b"\x01" + bytes([len(username)]) + username.encode() + bytes([len(password)]) + password.encode())
            response = remote_socket.recv(4096)
            if response[1] != 0x00:
                client_socket.close()
                return

            # 发送 SOCKS5 连接请求
            remote_socket.sendall(b"\x05\x01\x00\x03" + bytes([len(address)]) + address.encode() + port.to_bytes(2, 'big'))
            response = remote_socket.recv(4096)
            if response[1] != 0x00:  # 连接未成功
                client_socket.close()
                return

            # 通知客户端连接已建立
            client_socket.sendall(b"\x05\x00\x00\x01" + socket.inet_aton("0.0.0.0") + (1080).to_bytes(2, 'big'))

            # 在客户端和远程服务器之间转发数据
            self.forward_data(client_socket, remote_socket)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

    def verify_credentials(self, client_socket):
        """校验用户名和密码"""
        version = ord(client_socket.recv(1))
        if version != 1:
            client_socket.close()
            return False

        username_len = ord(client_socket.recv(1))
        username = client_socket.recv(username_len).decode('utf-8')
        password_len = ord(client_socket.recv(1))
        password = client_socket.recv(password_len).decode('utf-8')

        if username == self.username and password == self.password:
            # 验证成功, status = 0
            response = struct.pack("!BB", version, 0)
            client_socket.sendall(response)
            return True

        # 验证失败, status != 0
        response = struct.pack("!BB", version, 0xFF)
        client_socket.sendall(response)
        client_socket.close()
        return False

    def forward_data(self, client_socket, remote_socket):
        try:
            while True:
                ready_sockets, _, _ = select.select([client_socket, remote_socket], [], [])
                if client_socket in ready_sockets:
                    data = client_socket.recv(4096)
                    if len(data) == 0:
                        break
                    remote_socket.sendall(data)
                if remote_socket in ready_sockets:
                    data = remote_socket.recv(4096)
                    if len(data) == 0:
                        break
                    client_socket.sendall(data)
        except Exception as e:
            print(f"Forwarding error: {e}")
        finally:
            client_socket.close()
            remote_socket.close()

    def start(self):
        print("Starting SOCKS5 server...")
        while True:
            client_socket, addr = self.server_socket.accept()
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    server = Socks5Server()
    server.start()
