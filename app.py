from flask import Flask, render_template, request, jsonify
from deepface import DeepFace
import os

app = Flask(__name__)

known_image_path = "known_faces/admin.jpg"  # admin ni image

@app.route('/')
def home(): 
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    if not file:
        return jsonify({"success": False, "msg": "No file uploaded"})

    user_image_path = "temp_upload.jpg"
    file.save(user_image_path)

    try:
        result = DeepFace.verify(user_image_path, known_image_path)
        os.remove(user_image_path)
        if result["verified"]:
            return jsonify({"success": True, "name": "Admin"})
        else:
            return jsonify({"success": False, "msg": "Face does not match"})
    except Exception as e:
        os.remove(user_image_path)
        return jsonify({"success": False, "msg": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
