import socket

target_hosts = "127.0.0.1"
target_port = 9997

# 创建一个带有AF_INET和SOCK_STREAM参数的socket对象
# 建立socket连接，socket.AF_INET表示使用IPv4地址或主机名，SOCK_STREAM代表使用TCP协议
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 建立连接参数为目标主机的地址和端口
client.connect((target_hosts, target_port))

# 发送数据，这里是以bytes类型发送HTTP的请求头
client.send(b"who are you?")

# 接收反馈数据，4096是buf长度也就是一次接收数据的最大长度
response = client.recv(4096)

# 打印返回的数据并关闭socket连接
print(response.decode())
client.close()
