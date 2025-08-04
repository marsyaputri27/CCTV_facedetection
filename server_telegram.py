from flask import Flask, request
import cv2
import numpy as np
import requests
import telepot
import io



app = Flask(__name__)

BOT_TOKEN = '7592379058:AAH5DQEFcfDwhQ5jAW9vhRSNjapz98RYOmg'
CHAT_ID = '1645967530'
bot = telepot.Bot(BOT_TOKEN)

def detect_face(image_bytes):
    image_stream = io.BytesIO(image_bytes)
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if img is None:
        print("Gambar tidak bisa didecode, kemungkinan format tidak cocok.")
        return False

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return len(faces) > 0


@app.route('/', methods=['POST'])
def receive_image():
    image_bytes = request.data
    if image_bytes:
        if detect_face(image_bytes):
            print("Wajah terdeteksi, mengirim ke Telegram...")
            bot.sendPhoto(CHAT_ID, photo=io.BytesIO(image_bytes))  # ✅ FIX
        else:
            print("Tidak ada wajah, tidak dikirim.")
        return 'OK', 200
    else:
        return 'No image data', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
