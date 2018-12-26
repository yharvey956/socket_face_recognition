#传递未知人脸图片和已知人脸数据文件夹给socket服务器端 服务器返回相应的人脸对应的数组
import socket
import sys
import json

#接收参数 一是要识别图像的路径 二是已知的人脸特征数据位置
if len(sys.argv) < 2 :
    #参数数量不对
    print('{"result":false,"msg":"\u53c2\u6570\u6570\u91cf\u4e0d\u5bf9"}')
    exit()

hostport = ('127.0.0.1',8888)

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #创建TCP socket
    s.connect(hostport)  #链接套接字
except Exception:
    #连接失败
    print("{'result':false,'msg':'\u8fde\u63a5\u5931\u8d25'}")
    exit()

dic = sys.argv
dic.pop(0)
user_input = json.dumps(sys.argv)

s.send(bytes(user_input,'utf8')) #发送数据到套接字
while True:
    server_reply = s.recv(1024) #接收套接字数据
    print(str(server_reply, 'utf8'))  #打印输出
    break