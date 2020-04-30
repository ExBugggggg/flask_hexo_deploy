# -*- coding: utf-8 -*-
import os
import subprocess
import time
import hashlib
from flask import Flask, request, url_for, jsonify
from werkzeug.utils import secure_filename


app = Flask(__name__)
# Your hexo posts path
app.config['UPLOAD_FOLDER'] = '/www/hexo_site/source/_posts/'
# app.config['UPLOAD_FOLDER'] = '/Users/Cc/Desktop/flask_app/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SHELL_PATH'] = '/www/flask_app/nohup_blog.sh'
app.config['DELETE_SHELL'] = '/www/flask_app/del_blog.sh'
# param for check, Your encrpty salt
app.config['AUTH_CONFIRM'] = '1997-08-21'


@app.route('/deploy', methods=['POST'])
def deploy():
    if request.method == 'POST':
        if not request.form.get("auth") or not token_chk(request.form.get("auth")):
            return jsonify({'code': 401, 'status': 'wrong: bad auth'})

        if run_shell(app.config['SHELL_PATH']):
            return jsonify({'code': 200, 'status': 'success'})
        else:
            return jsonify({'code': 403, 'status': 'wrong: execute command'})


@app.route('/delete', methods=['GET'])
def delete():
    if request.method == 'POST':
        if not request.form.get("auth") or not token_chk(request.form.get("auth")):
            return jsonify({'code': 401, 'status': 'wrong: bad auth'})

        file_name = request.form.get("file_name")
        if not allow_extension(file_name):
            return jsonify({'code': 400, 'status': 'wrong: file extension'})

        if del_shell(app.config['DELETE_SHELL'], file_name):
            return jsonify({'code': 200, 'status': 'success'})
        else:
            return jsonify({'code': 400, 'status': 'wrong: no this file'})


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file_name = file.filename
        if not request.form.get("auth") or not token_chk(request.form.get("auth")):
            return jsonify({'code': 401, 'status': 'wrong: bad auth'})
        if file and allow_extension(file_name):
            file_name = secure_filename(file_name)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            return jsonify({'code': 200, 'status': 'success'})
        else:
            return jsonify({'code': 400, 'status': 'wrong: file extension'})
    else:
        return jsonify({'code': 500, 'status': 'wrong: http request method'})


def allow_extension(filename: str) -> bool:
    file_ext = ['md']

    if '.' not in filename:
        return False
    file_list = filename.split('.', -1)

    # 判断是否有除了.以外的特殊字符
    special_character = ["`~!@#$%^&*()_-+=[]{ };:\"'<,>?/\\"]
    for i in special_character:
        if i in filename:
            return jsonify({'code': 400, 'status': 'wrong: character'})

    if len(file_list) != 2 or file_list[1] not in file_ext:
        return False
    return True


def run_shell(shell_path: str) -> bool:
    ret_pid = subprocess.Popen(
        'bash {}'.format(shell_path), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ret_pid.wait()
    if ret_pid.returncode == 0:
        return True
    else:
        return False


def del_shell(shell_path: str, file_name: str) -> bool:
    run_sh = 'bash {} {}'.format(shell_path, file_name)
    ret_pid = subprocess.Popen(
        run_sh, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ret_pid.wait()
    if ret_pid.returncode == 0:
        return True
    else:
        return False


def token_chk(token: str) -> bool:
    now_time = int(time.time() / 30)
    src_str = str(now_time) + app.config['AUTH_CONFIRM']
    enc = hashlib.sha256()
    enc.update(src_str.encode(encoding='utf-8'))
    enc_str = enc.hexdigest()
    if enc_str == token:
        return True
    else:
        return False
