# 基于Python的人脸识别和对比
------
使用**Face Recognition**人脸识别库检测识别对比人脸。

测试环境

        Python 3.6.4
        Windows 10
        Anaconda 4.5.12
        Dlib 19.16.0
        Face_Recognition 1.2.3
        cmake 3.13.2
        Visual Studio 2017

Face_Recognition安装

        安装好Python，Anaconda运行环境，打开Anaconda Prompt
        1.安装cmake：pip install cmake
        2.安装dlib：pip intsall dlib
        3.安装Face_Recognition：pip install face_recognition

使用
    
        service.py 将开启一个socket服务
        通过 client.py 调用不同的方法
    
1生成人脸数据文件 

	    python client.py 1 img\obama.jpg faces

![Image text](https://raw.githubusercontent.com/hongmaju/light7Local/master/img/productShow/20170518152848.png)

       提取传入图片的人脸特征数据存储到faces文件夹
       
       执行成功返回数据为人脸位置的左上右下两个坐标点

2对比人脸

	    python client.py 2 img\unknown.jpg faces
	    
![Image text](https://raw.githubusercontent.com/hongmaju/light7Local/master/img/productShow/20170518152848.png)	    
	    
        提取传入图片的人脸特征数据与faces文件夹里存储的人脸数据进行对比查找对应的人
       
        执行成功返回数据为识别的人以及人脸位置的左上右下两个坐标点，在40张已有人脸数据下识别两个人脸，消耗时间大约为0.15s
    
    

    
    