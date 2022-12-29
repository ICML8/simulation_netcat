import socket

IP = '0.0.0.0'
PORT = 9997


def main():
    # 创建 socket 对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 设置 socket 超时时间
    server_socket.settimeout(5)
    # 绑定服务端地址和端口号
    server_socket.bind((IP, PORT))

    while True:
        try:
            # 接收数据
            data, client_address = server_socket.recvfrom(4096)

            # 处理数据
            print(f'[*] Listening on {IP}:{PORT}')
            print(f'[*] Accept connection from {data}:{client_address}')

            # 发送数据
            server_socket.sendto(b'I am fine', client_address)

        except socket.timeout:
            # 在超时时间内没有收到数据，继续等待
            continue


if __name__ == '__main__':
    main()
