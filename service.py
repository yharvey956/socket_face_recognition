#根据已知文件夹人脸数据 从未知图中对比出图片里面的人脸对应的人
import socket
import json
import face_recognition

mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HostPort = ('127.0.0.1',8888)
mysocket.bind(HostPort)  #绑定地址端口
mysocket.listen(5)  #监听最多5个连接请求

while True:
    print('server socket waiting...')
    client,addr = mysocket.accept()  #阻塞等待链接，创建套接字c链接和地址信息addr
    while True:
        try:
            client_data = client.recv(1024) #接收客户端数据
            if str(client_data,'utf8') == 'quit':
                client.close()
                break
        except Exception:
            #无数据
            client.send(bytes('{"result":false,"msg":"\u65e0\u6570\u636e"}','utf8')) 
            break
        #检测json数据
        try:
            client_json = json.loads(client_data, encoding='utf-8')
        except ValueError:
            #不是合法的数据
            client.send(bytes('{"result":false,"msg":"\u4e0d\u662f\u5408\u6cd5\u7684\u6570\u636e"}','utf8'))
            break
        #是否为数组
        if not(isinstance(client_json,list) and len(client_json) > 1):
            #非数组/或者数组长度不够
            client.send(bytes('{"result":false,"msg":"\u975e\u6570\u7ec4\/\u6216\u8005\u6570\u7ec4\u957f\u5ea6\u4e0d\u591f"}','utf8'))
            break

        #建立人脸特征数据
        def build_face_data_func():
            import build_face_data_class
            return build_face_data_class.build_face_data()

        #对比人脸
        def face_rec_func():
            import face_rec_class
            return face_rec_class.face_rec()

        def other():
            #无对应的操作方法
            return '{"result":false,"msg":"\u65e0\u5bf9\u5e94\u7684\u64cd\u4f5c\u65b9\u6cd5"}'


        def runfunction(x):
            #定义一个map，相当于定义case：func()
            swicher = {
                1:build_face_data_func,
                2:face_rec_func
            }
            func = swicher.get(x,other) #从map中取出方法
            return func().run(client_json,face_recognition)   #执行

        client.send(bytes(runfunction(int(client_json[0])),'utf8'))  #发送数据给客户端
        print('clientINFO:',str(client_data, 'utf8'))