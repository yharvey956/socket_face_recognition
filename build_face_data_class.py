# 传入要转换为人脸特征数据的图片 以及保存图片的路径
import os
import pickle
import json

class build_face_data():
	def run(self, client_json, face_recognition):
		if len(client_json) < 3:
			return "{'result':false,'msg':'参数数量不对'}"

		rootPath = "D:/Code/Face_recognition/"
		image_path = rootPath + client_json[1]
		save_dir = rootPath + client_json[2]

		if not(os.path.isfile(image_path)):
			return "{'result':false,'msg':'文件/文件夹路径错误'}"

		if not(os.path.exists(save_dir)):
			os.makedirs(save_dir)

		unknown_image = face_recognition.load_image_file(image_path)

		face_locations = face_recognition.face_locations(unknown_image)
		face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

		if len(face_encodings) != 1:
			return "{'result':false,'msg':'请上传只有一张人脸的照片'}"

		# 获取文件名不包含后缀
		(filepath, tempfilename) = os.path.split(image_path)
		(shotname, extension) = os.path.splitext(tempfilename)
		# 写文件
		with open(save_dir + "/" + shotname + '.dat', 'wb') as file_object:
			pickle.dump([face_encodings[0]], file_object)

		retJson = {"result": True, "msg": face_locations[0]}
		return json.dumps(retJson)
