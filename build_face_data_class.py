# 传入要转换为人脸特征数据的图片 以及保存图片的路径
import os
import pickle
import json

class build_face_data():
	def run(self, client_json, face_recognition):
		if len(client_json) < 3:
			#参数数量不对
			return '{"result":false,"msg":"\u53c2\u6570\u6570\u91cf\u4e0d\u5bf9"}'

		rootPath = os.getcwd() + "/"
		image_path = rootPath + client_json[1]
		save_dir = rootPath + client_json[2]

		if not(os.path.isfile(image_path) or os.path.isdir(image_path)):
			#文件/文件夹路径错误
			return '{"result":false,"msg":"\u6587\u4ef6\/\u6587\u4ef6\u5939\u8def\u5f84\u9519\u8bef"}'

		imgLis = [];

		if os.path.isdir(image_path):
			allFile = os.walk(image_path)
			for path, d, filelist in allFile:
				for filename in filelist:
					if filename.endswith('jpg') or filename.endswith('png') or filename.endswith('jpeg'):
						imgLis.append(os.path.join(path, filename))
		else:
			imgLis = [image_path]

		#如果是文件夹获取所有的图片文件

		if not(os.path.exists(save_dir)):
			os.makedirs(save_dir)

		face_locationsArr = [];
		for image_path in imgLis:

			unknown_image = face_recognition.load_image_file(image_path)

			face_locations = face_recognition.face_locations(unknown_image)
			face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

			if len(face_encodings) != 1:
				return '{"result":false,"msg":"\u8bf7\u4e0a\u4f20\u53ea\u6709\u4e00\u5f20\u4eba\u8138\u7684\u7167\u7247"}'

			# 获取文件名不包含后缀
			(filepath, tempfilename) = os.path.split(image_path)
			(shotname, extension) = os.path.splitext(tempfilename)
			# 写文件
			with open(save_dir + "/" + shotname + '.dat', 'wb') as file_object:
				pickle.dump([face_encodings[0]], file_object)

			face_locationsArr.append(face_locations[0])

		retJson = {"result": True, "msg":face_locationsArr}
		return json.dumps(retJson)
