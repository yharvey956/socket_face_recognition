import os
import json
import pickle
import time

class face_rec():
    def run(self, client_json, face_recognition):
        if len(client_json) < 3:
            #参数数量不对
            return '{"result":false,"msg":"\u53c2\u6570\u6570\u91cf\u4e0d\u5bf9"}'

        start = time.clock()
        rootPath = "D:/Code/Face_recognition/"
        image_path = rootPath + client_json[1]
        child_pic_dir = rootPath + client_json[2]
        face_names = []
        coordinate = []
        if not(os.path.exists(child_pic_dir) and os.path.isfile(image_path)):
            #文件/文件夹路径错误
            return '{"result":false,"msg":"\u6587\u4ef6\/\u6587\u4ef6\u5939\u8def\u5f84\u9519\u8bef"}'

        # 获取所有的图片文件
        alist = []
        allFile = os.walk(child_pic_dir)
        for path, d, filelist in allFile:
            for filename in filelist:
                if filename.endswith('jpg') or filename.endswith('png') or filename.endswith('jpeg'):
                    alist.append(os.path.join(path, filename))

        # 获取对应的特征
        known_face_encodings = []
        known_face_names = []

        for filename in alist:
            # 获取文件名不包含后缀
            (filepath, tempfilename) = os.path.split(filename)
            (shotname, extension) = os.path.splitext(tempfilename)
            known_face_names.append(shotname)

            # 读文件
            with open(child_pic_dir + "/" + shotname + '.dat', 'rb') as file_object:
                known_face_encodings.append(pickle.load(file_object)[0])

        # 定位图中人脸的位置
        unknown_image = face_recognition.load_image_file(image_path)
       
        #opencv 获取人脸坐标的方法 记得要补回去 import cv2
        # face_locations = []
        # xmlPath = os.getcwd() + "/haarcascade_frontalface_alt2.xml"
        # if not(os.path.isfile(xmlPath)):
        #     return "{'result':false,'msg':'xml路径错误'}"

        # face_cascade=cv2.CascadeClassifier(xmlPath)
        # image = cv2.imread(image_path)           #读取图片
        # gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)  #灰度转换
        # faces = face_cascade.detectMultiScale(         #探测人脸
        #     gray,
        #     scaleFactor = 1.15,
        #     minNeighbors = 5,
        #     minSize = (5,5),
        # )
        # for(x,y,w,h) in faces:
        #     face_locations.append([int(y),int(w+x),int(y+h),int(x)])
        face_locations = face_recognition.face_locations(unknown_image,0)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        for key,face_encoding in enumerate(face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                face_names.append(name)
                coordinate.append(face_locations[key])

        end = time.clock()
        retJson = {"result": True, "msg": face_names,"coordinate":coordinate, "time": 'use time: %s S' % (end-start)}
        js = json.dumps(retJson)
        return js
