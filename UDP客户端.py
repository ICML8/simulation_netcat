import socket

target_host = '127.0.0.1'
target_port = 9997

# 建立socket连接，SOCK_DGRAM代表使用UDP协议
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 用UDP协议，不需要先建立链接再发送数据，所以这里没有connect这一步
# 发送数据，使用sendto函数，除了要发送的数据外还需要给出目标主机的地址和端口
client.sendto(b'who are you?', (target_host, target_port))

# 使用recvfrom接收反馈数据和对方主机地址
data, adder = client.recvfrom(4096)

# 打印返回的数据并关闭socket连接
print(data.decode())
client.close()
