import numpy as np
import cv2
import uuid

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
def encrypt_value(value, key_pixel, y2, c1Prime, c2Prime):
    return ((value + c1Prime * key_pixel + c2Prime * y2) % 256)

# Function to decrypt pixel value
def decrypt_value(value, key_pixel, y2, c1Prime, c2Prime):
    return ((value - c1Prime * key_pixel - c2Prime * y2) % 256)

# Function to encrypt image using another image as key
def encrypt_image_with_key(key_image_path, original_image):
    key_image = cv2.imread(key_image_path, cv2.IMREAD_GRAYSCALE)
    c1Prime, c2Prime = key_func(key_image.flatten().tobytes().decode('ISO-8859-1'))
    encrypted_image = np.zeros_like(original_image, dtype=np.uint8)

    for i in range(original_image.shape[0]):
        for j in range(original_image.shape[1]):
            pixel = original_image[i, j]
            key_pixel = key_image[i % key_image.shape[0], j % key_image.shape[1]]
            encrypted_pixel = encrypt_value(pixel, key_pixel, y2_value, c1Prime, c2Prime)
            encrypted_image[i, j] = encrypted_pixel

    return encrypted_image

# Function to decrypt image
# Function to decrypt image
def decrypt_image(key_image_path, encrypted_image):
    key_image = cv2.imread(key_image_path, cv2.IMREAD_GRAYSCALE)
    c1Prime, c2Prime = key_func(key_image.flatten().tobytes().decode('ISO-8859-1'))
    decrypted_image = np.zeros_like(encrypted_image, dtype=np.uint8)

    for i in range(encrypted_image.shape[0]):
        for j in range(encrypted_image.shape[1]):
            pixel = encrypted_image[i, j]
            decrypted_pixel = decrypt_value(pixel, y1_value, y2_value, c1Prime, c2Prime)
            decrypted_image[i, j] = decrypted_pixel

    return decrypted_image
    c1Prime, c2Prime = key_func(key)
    decrypted_image = np.zeros_like(encrypted_image, dtype=np.uint8)

    for i in range(encrypted_image.shape[0]):
        for j in range(encrypted_image.shape[1]):
            pixel = encrypted_image[i, j]
            decrypted_pixel = decrypt_value(pixel, y1_value, y2_value, c1Prime, c2Prime)
            decrypted_image[i, j] = decrypted_pixel

    return decrypted_image

# Example usage
def encrypt_decrypt_image_with_key(key_image_path, original_image_path):
    original_image = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)

    encrypted_image = encrypt_image_with_key(key_image_path, original_image)
    decrypted_image = decrypt_image(key_image_path, encrypted_image)

    # Save images
    encrypted_image_path = "encrypted_" + str(uuid.uuid4()) + ".png"
    decrypted_image_path = "decrypted_" + str(uuid.uuid4()) + ".png"

    cv2.imwrite(encrypted_image_path, encrypted_image)
    cv2.imwrite(decrypted_image_path, decrypted_image)

    # Display images
    cv2.imshow('Original Image', original_image)
    cv2.imshow('Encrypted Image', encrypted_image)
    cv2.imshow('Decrypted Image', decrypted_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return encrypted_image_path, decrypted_image_path
    original_image = cv2.imread(original_image_path, cv2.IMREAD_GRAYSCALE)

    encrypted_image = encrypt_image_with_key(key_image_path, original_image)
    decrypted_image = decrypt_image(key_image_path, encrypted_image)  # Fix: Pass key_image_path instead of key

    # Save images
    encrypted_image_path = "encrypted_" + str(uuid.uuid4()) + ".png"
    decrypted_image_path = "decrypted_" + str(uuid.uuid4()) + ".png"

    cv2.imwrite(encrypted_image_path, encrypted_image)
    cv2.imwrite(decrypted_image_path, decrypted_image)

    # Display images
    cv2.imshow('Original Image', original_image)
    cv2.imshow('Encrypted Image', encrypted_image)
    cv2.imshow('Decrypted Image', decrypted_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return encrypted_image_path, decrypted_image_path

# Example usage
key_image_path = "aot8.jpg"
original_image_path = "meng.jpg"
encrypt_decrypt_image_with_key(key_image_path, original_image_path)
