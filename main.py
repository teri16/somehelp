import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'  

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return '没有文件部分', 400
    file = request.files['image']
    message = request.form['message']

    if file.filename == '':
        return '没有选择文件', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

    
        encoded_file_path = lsb_embed(file_path, message, coordinates)

        if encoded_file_path:
            return send_file(encoded_file_path, as_attachment=True, download_name='encoded_' + filename)
        else:
            return '处理图像时出现问题', 500

    return '上传失败', 500

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png']

def lsb_embed(image_path, message, coordinates):
    try:
        image = Image.open(image_path)
        encoded = image.copy()
        pixels = encoded.load()

       
        binary_message = ''.join(format(ord(char), '08b') for char in message)[:len(coordinates)]

        
        for bit, coord in zip(binary_message, coordinates):
            x, y = coord
            pixel = list(pixels[x, y])
            
            pixel[1] = (pixel[1] & ~1) | int(bit)
            pixels[x, y] = tuple(pixel)

        
        encoded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encoded_' + os.path.basename(image_path))
        encoded.save(encoded_file_path, format='PNG')  
        return encoded_file_path
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

coordinates = [
    
( 57, 57),
( 58, 8),
( 63, 54),
( 94, 46),
( 96, 160),
( 135, 88),
( 138, 110),
( 157, 169),
( 4, 184),
( 6, 59),
( 25, 0),
( 63, 178),
( 84, 90),
( 144, 177),
( 145, 123),
( 149, 91),
( 40, 56),
( 55, 153),
( 101, 157),
( 108, 9),
( 131, 55),
( 134, 115),
( 186, 153),
( 194, 36)

]

if __name__ == '__main__':
    app.run(debug=True)
    #架設在127.0.0.1 port5000


#if __name__ == '__main__':
   # app.run(host='192.168.53.249', debug=True)
