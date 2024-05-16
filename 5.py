import socket
import threading
import select

class Socks5Server:
    def __init__(self, host='192.168.3.137', port=1080):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f'SOCKS5 server started on {self.host}:{self.port}')

    def handle_client(self, client_socket):
        try:
            # 读取SOCKS5初始握手数据
            request = client_socket.recv(4096)
            # 仅处理简单的SOCKS5握手 (无认证)
            client_socket.sendall(b"\x05\x00")

            # 读取客户端请求数据
            request = client_socket.recv(4096)
            mode = request[1]
            if mode != 1:  # 仅支持CONNECT请求
                client_socket.close()
                return

            addr_type = request[3]
            if addr_type == 1:  # IPv4
                address = socket.inet_ntoa(request[4:8])
                port = int.from_bytes(request[8:10], 'big')
            elif addr_type == 3:  # 域名
                domain_length = request[4]
                address = request[5:5+domain_length].decode()
                port = int.from_bytes(request[5+domain_length:5+domain_length+2], 'big')
            else:
                client_socket.close()
                return

            # 连接目标服务器
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.connect((address, port))

            # 通知客户端连接已建立
            client_socket.sendall(b"\x05\x00\x00\x01" + socket.inet_aton("0.0.0.0") + (1080).to_bytes(2, 'big'))

            # 转发数据
            self.forward_data(client_socket, remote_socket)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

    def forward_data(self, client_socket, remote_socket):
        sockets = [client_socket, remote_socket]
        while True:
            read_sockets, _, error_sockets = select.select(sockets, [], sockets)
            if error_sockets:
                break
            for sock in read_sockets:
                data = sock.recv(4096)
                if not data:
                    return
                if sock is client_socket:
                    remote_socket.sendall(data)
                else:
                    client_socket.sendall(data)

    def start(self):
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                print(f'Accepted connection from {addr}')
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_handler.start()
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    server = Socks5Server()
    server.start()
