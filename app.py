from flask import Flask, request, jsonify, render_template
import os
import subprocess
import json
from werkzeug.utils import secure_filename
import uuid
from photo import photo_app, process_image  # 导入 photo.py 的 Blueprint 和 process_image 函数

app = Flask(__name__)

# 将 photo_app 的路由注册到主应用
app.register_blueprint(photo_app)

UPLOAD_FOLDER = 'assets/uploads'
SAVED_FOLDER = 'assets/saved'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SAVED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_type = request.form.get('type')  # 'image' or 'video'
    
    # 使用 UUID 生成唯一的文件名，避免使用原始文件名
    unique_filename = f"{uuid.uuid4()}.{file.filename.rsplit('.', 1)[1].lower()}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(file_path)

    if file_type == 'image':
        # 直接调用处理图像的函数
        process_image(file_path)
    elif file_type == 'video':
        # 调用 video.py 处理视频
        subprocess.run(['python', 'video.py', file_path])

    return jsonify({'success': True, 'message': '文件处理完成'})

@app.route('/save', methods=['POST'])
def save_file():
    data = json.loads(request.data)
    file_type = data.get('type')
    filename = data.get('filename')
    
    # 使用 UUID 生成唯一的文件名，避免使用原始文件名
    unique_filename = f"{uuid.uuid4()}.{filename.rsplit('.', 1)[1].lower()}"
    source_path = os.path.join(UPLOAD_FOLDER, filename)
    save_path = os.path.join(SAVED_FOLDER, unique_filename)

    if os.path.exists(source_path):
        os.rename(source_path, save_path)
        return jsonify({'success': True, 'message': f'{file_type} 保存成功'})
    else:
        return jsonify({'success': False, 'message': '文件不存在'})

if __name__ == '__main__':
    app.run(debug=True)
