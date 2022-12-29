import socket
import threading

IP = '0.0.0.0'
PORT = 9997


def main():
    # 创建一个带有AF_INET和SOCK_STREAM参数的socket对象
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 指定服务器要监听地址与端口
    server.bind((IP, PORT))
    # 设置最大的连接数
    server.listen(5)
    # 输出正在监听的客户端
    print(f'[*] Listening on {IP}:{PORT}')

    while True:
        # accept函数监听连接，收到连接返回一个套接字和地址
        client, address = server.accept()
        print(f'[*] Accept connection from {address[0]}:{address[1]}')
        # 建立线程处理连接
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


def handle_client(client_sock=None):
    with client_sock as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf_8")}')
        sock.send(b'ACK')


if __name__ == '__main__':
    main()
