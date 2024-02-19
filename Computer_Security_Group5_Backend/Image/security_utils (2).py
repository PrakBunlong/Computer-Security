from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import cv2
import uuid

app = Flask(__name__)

# Parameters for encryption
c1_value = -0.5
c2_value = 0.5
y1_value = 0.7
y2_value = -0.2

# Function to generate keys for encryption
def key_func(key):
    y_array = []
    temp = ord(key[0]) + c1_value * y1_value + c2_value * y2_value
    y_array.append(temp % 256)

    temp = ord(key[1]) + c1_value * y_array[0] + c2_value * y1_value
    y_array.append(temp % 256)

    for i in range(2, 16):
        temp = ord(key[i]) + c1_value * y_array[i - 1] + c2_value * y_array[i - 2]
        y_array.append(temp % 256)

    c1Prime = y_array[14]
    c2Prime = y_array[15]
    return c1Prime, c2Prime

# Function to encrypt pixel value
def encrypt_value(value, y1, y2, c1Prime, c2Prime):
    return ((value + c1Prime * y1 + c2Prime * y2) % 256)

# Function to decrypt pixel value
def decrypt_value(value, y1, y2, c1Prime, c2Prime):
    return ((value - c1Prime * y1 - c2Prime * y2) % 256)

# Function to encrypt image
def encrypt_image(key, original_image_path):
    c1Prime, c2Prime = key_func(key)
    original_image = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)
    encrypted_image = np.zeros_like(original_image, dtype=np.uint8)

    for i in range(original_image.shape[0]):
        for j in range(original_image.shape[1]):
            pixel = original_image[i, j]
            encrypted_pixel = encrypt_value(pixel, y1_value, y2_value, c1Prime, c2Prime)
            encrypted_image[i, j] = encrypted_pixel

    encrypted_image_path = "encrypted_" + str(uuid.uuid4()) + ".png"
    cv2.imwrite(encrypted_image_path, encrypted_image)
    return encrypted_image_path

# Function to decrypt image
def decrypt_image(key, encrypted_image_path):
    c1Prime, c2Prime = key_func(key)
    encrypted_image = cv2.imread(encrypted_image_path, cv2.IMREAD_GRAYSCALE)
    decrypted_image = np.zeros_like(encrypted_image, dtype=np.uint8)

    for i in range(encrypted_image.shape[0]):
        for j in range(encrypted_image.shape[1]):
            pixel = encrypted_image[i, j]
            decrypted_pixel = decrypt_value(pixel, y1_value, y2_value, c1Prime, c2Prime)
            decrypted_image[i, j] = decrypted_pixel

    decrypted_image_path = "decrypted_" + str(uuid.uuid4()) + ".png"
    cv2.imwrite(decrypted_image_path, decrypted_image)
    return decrypted_image_path

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the uploaded image to a temporary file
    filename = str(uuid.uuid4()) + ".png"
    file.save(filename)

    return jsonify({'filename': filename})

@app.route('/api/encrypt', methods=['POST'])
def encrypt():
    key = request.json.get('key', '')
    filename = request.json.get('filename', '')

    encrypted_image_path = encrypt_image(key, filename)

    return jsonify({'encrypted_image_path': encrypted_image_path})

@app.route('/api/decrypt', methods=['POST'])
def decrypt():
    key = request.json.get('key', '')
    encrypted_image_path = request.json.get('encrypted_image_path', '')

    decrypted_image_path = decrypt_image(key, encrypted_image_path)

    return jsonify({'decrypted_image_path': decrypted_image_path})

if __name__ == '__main__':
    app.run(debug=True)
