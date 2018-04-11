# -*- coding: utf-8 -*-

import sys
from flask import Flask, request, render_template
import os
from flask_uploads import UploadSet, configure_uploads, TEXT,IMAGES, patch_request_class
import time
from yidian.data.common.file_job import *
from yidian.data.common.date import *
from service import run


FILE_PATH = os.getcwd()+'/files/'
MULTI_FILE_PATH = os.getcwd()+'/files/%s/%s/'


reload(sys)
sys.setdefaultencoding('utf-8')


class options_init(object):
	def __init__(self, kws, users, province, city, age, gender, path, file):
		self.kws = kws
		self.users = users
		self.province = province
		self.city = city
		self.age = age
		self.gender = gender
		self.path = path
		self.file = file


app = Flask(__name__)

app.config['UPLOADS_DEFAULT_DEST'] = os.getcwd()  # 文件储存地址
app.config['ALLOWED_EXTENSIONS'] = set(['txt'])


files = UploadSet('files', TEXT)
configure_uploads(app, files)
patch_request_class(app)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/signin', methods=['GET'])
def generate_user_profile():
    return render_template('form.html')


@app.route('/signin', methods=['POST'])
def generate():
	print('接受请求生成用户画像')
	files_url = ''
	path_url = MULTI_FILE_PATH % (request.form['users'], time.strftime('%Y-%m-%d',time.localtime(time.time())))

	if 'file' in request.files:
		print('网页端请求通过解析文件查询，且正在在上传文件')
		filename = files.save(request.files['file'])
		print(request.files['file'])
		files_url = FILE_PATH+filename
		print('已经保存文件'+filename+'到'+files_url)
	elif 'path[]' in request.files:
		run_command('mkdir -p %s' % path_url)
		filelist = request.files.getlist("path[]")
		print(filelist)
		for file in filelist:
			print('---ALL',file)
			if file and allowed_file(file.filename):
				print('xxxFileName',file.filename)
				print('+++Filter',file)
				url = file.filename.split('/')[-1]
				multi_file_url = path_url + url
				muliti_filename = file.save(multi_file_url)
				print(muliti_filename)
	kws = request.form['kws']
	users = request.form['users']
	print(type(users))
	province = request.form['province']
	city = request.form['city']
	age = request.form['age']
	gender = request.form['gender']
	path = path_url
	file = files_url
	print(type(file))

	options = options_init(kws, users, province, city, age, gender, path, file)
	print('初始化生成参数:')
	print(options.__dict__)
	run(options)
	print('用户画像生成结束，且网页已经展示')
	return render_template('form.html')


if __name__ == '__main__':
    app.run()