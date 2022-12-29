import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading


# 创建接受一条命令并执行的execute函数，并将结果作为一段字符串输出
def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    # 用subprocess这个库中它的check_output函数，这个函数会在本机运行一条命令，并返回该命令的输出
    return output.decode()


# 创建类并初始化Netcat对象
class Netcat:
    # 程序的初始化
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        # 创建socket对象
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 执行函数
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()
        # run函数是Netcat对象的执行入口
        # 如果我们是接受方，我们就执行listen，如果我们是发送方，我们就执行send

    # 发送send函数
    def send(self):
        # 先连接目标地址和对应端口
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            # 如果缓冲区里有数据的话，就先把这些数据发过去
            # 然后创建一个try/catch块，用Ctrl+C 手动关闭连接
            while True:
                # while true大循环，一轮一轮地接收目标返回的数据
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        # 嵌套一个小循环，用来读取socket本轮返回的数据
                        # 如果socket里的数据目前已经读到头，就退出小循环
                        break

                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
                    # 检查刚才有没有读出什么东西来，如果读出了什么，就输出到屏幕上
                    # 并暂停，等待用户输入新的内容，再把新的内容发给目标
                    # 接着开始下一轮大循环
        except KeyboardInterrupt:
            print('用户终止.')
            self.socket.close()
            sys.exit()
            # 大循环将一直持续下去
            # 直到你按下Ctrl+C触发KeyboardInterrupt中断循环，关闭socket对象

    # 监听listen函数
    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        # 把socket对象绑定到target和port上
        self.socket.listen(5)
        # 用循环来监新的连接
        while True:
            client_socket, _ = self.socket.accept()
            # 把已经连接的对象传递给handle函数进行控制
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()

    # handle控制函数
    # handle函数会根据它收到的命令行参数来执行相应的任务：
    # 执行命令、上传文件，或是打开一个shell
    def handle(self, client_socket):
        if self.args.execute:
            # 执行命令
            # handle函数就会把该命令传递给execute函数，然后把输出结果通过socket发回去
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        elif self.args.upload:
            # 上传文件
            # 建一个循环来接收socket传来的文件内容，再将收到的全部数据写到参数指定的文件里
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'saved file {self.args.upload}'
            client_socket.send(message.encode())

        elif self.args.command:
            # 创建一个shell
            # 创建一个循环，向发送方发一个提示符，然后等待其发回命令。
            # 每收到一条命令，就用execute函数执行它，然后把结果发回发送方。
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'nc: #>')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'服务器断开 {e}')
                    self.socket.close()
                    sys.exit()
                    # shell收到换行符后才执行命令，兼容原版netcat。
                    # 可用它来做接收方，用原版的netcat做发送方。
                    # 如果用自己写的Python客户端做发送方的话
                    # 一定不要忘记加换行符。在send函数里
                    # 我们每次读取用户输入之后，都会在结尾加一个换行符（\n）


if __name__ == '__main__':
    # 使用标准库里的argparse库创建一个带命令行界面的程序，传递不同的参数，执行不同的操作
    # 帮助信息，程序启动的时候如果发现 --help参数，就会显示这段信息。
    parser = argparse.ArgumentParser(description='                                                      \n'
                                                 '  ███╗   ██╗███████╗████████╗ ██████╗ █████╗ ████████╗\n'
                                                 '  ████╗  ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗╚══██╔══╝\n'
                                                 '  ██╔██╗ ██║█████╗     ██║   ██║     ███████║   ██║   \n'
                                                 '  ██║╚██╗██║██╔══╝     ██║   ██║     ██╔══██║   ██║   \n'
                                                 '  ██║ ╚████║███████╗   ██║   ╚██████╗██║  ██║   ██║   \n'
                                                 '  ╚═╝  ╚═══╝╚══════╝   ╚═╝    ╚═════╝╚═╝  ╚═╝   ╚═╝   \n'
                                                 '                  \033[1;31m---Info：IcML0x824\033[0m \n',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''
                                     示例：
                                     netcat.py -t 192.168.1.1 -p 4444 -l -c                    # 提供命令行shell
                                     netcat.py -t 192.168.1.1 -p 4444 -l -u=mytest.txt         # 上传文件
                                     netcat.py -t 192.168.1.1 -p 4444 -l -e=\"cat etc/passwd\" # 执行命令
                                     echo 'ABC' | ./netcat.py -t 192.168.1.1 -p 135            # 回显本地文本
                                     netcat.py -t 192.168.1.1 -p 4444                          # 连接到服务器
                                     '''))
    # 添加6个参数，用来控制程序的行为
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.31.133', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    # 收到-c参数，打开一个交互式的命令行shell
    # 收到-e参数，执行一条命令
    # 收到-l参数，创建一个监听器
    # -p参数用来指定要通信的端口
    # -t参数用来指定要通信的目标IP地址
    # -u参数用来指定要上传的文件

    args = parser.parse_args()
    # 确定要进行监听，在缓冲区里填上空白数据，把空白缓冲区传给NetCat对象
    # 反之，就把stdin里的数据通过缓冲区传进去。最后调用NetCat类的run函数来启动它
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = Netcat(args, buffer.encode())
    nc.run()
