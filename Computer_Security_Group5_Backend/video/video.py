import math 
import uuid 
import cv2 
import soundfile as sf
import numpy as np
from PIL import Image

# Example Usage

# original_video_path = "original_video.png"
# encrypted_video_path = "encrypted_video.png"
# decrypted_video_path = "decrypted_video.png"  


input_c1 = -0.3
input_c2 = 0.3
input_y1 = 0.492
input_y2 = -0.133
key = "asdbgffdmsestuiu"


def video_keysystem(key):
    #empty arrays
    keyfunction_array = []
    temp = [] 
    
    #f function for the keys 
    temp = ord(key[0]) + input_c1 * input_y1+ input_c2 * input_y2 
    keyfunction_array.append(math.fmod(temp+1, 2.0) - 1) 
 
    temp = ord(key[1]) + input_c1 * keyfunction_array[0] + input_c2 * input_y1
    keyfunction_array.append(math.fmod(temp+1, 2.0) - 1) 
 
 
    for i in range(2, 16): 
        temp = ord(key[i]) + input_c1 * keyfunction_array[i - 1] + input_c2 * keyfunction_array[i - 2] 
        keyfunction_array.append(math.fmod(temp+1, 2.0) - 1) 
 
    for i in range(16): 
        if i == 14: 
            print("Key[14]: c1Prime: " + str(keyfunction_array[14])) 
        elif i == 15: 
            print("Key[15]: c2Prime: " + str(keyfunction_array[15])) 
        else: 
            print("Key"+str([i])+ ": "+str(keyfunction_array[i])) 
            
    c1Prime = keyfunction_array[14] 
    c2Prime = keyfunction_array[15] 
    
    return c1Prime, c2Prime


def f(x: float) -> float:
    return ((x + 1) % 2) - 1

def normalized(value): 
    return value / 256.0

def denormalized(value):
    return np.round(value * 256.0).astype(np.uint8)

def encrypt_value(value, y1, y2, c1Prime, c2Prime):
    return f(value + c1Prime * y1 + c2Prime * y2)

def decrypt_value(value, y1, y2, c1Prime, c2Prime):
    return f(value - c1Prime * y1 - c2Prime * y2)

def encrypt_func(key, original_values):
    normalized_original_values = []
    encrypted_values = []
    denormalized_encrypted_values = []
    c1Prime, c2Prime = video_keysystem(key)
    #Convert Values [0,255] to Values [-1,1]
    for i in range(len(original_values)): 
        normalized_original_values.append(normalized(original_values[i])) 

    #First Index , using While True to organize variables
    while True:
        temp_encrypted_value = encrypt_value(normalized_original_values[0], input_y1
    , input_y2, c1Prime, c2Prime)
        temp_denormalized_encrypted_value = normalized(denormalized(temp_encrypted_value)) # NORMALIZED_CEPTION

        # print("Encrypted: " + str(temp_denormalized_encrypted_value))
        # print("Original: " + str(normalized_original_values[0])) 

        encrypted_values.append(temp_denormalized_encrypted_value)
        break

    #Second Index , using While True to organize variables
    while True:
        temp_encrypted_value = encrypt_value(normalized_original_values[1], encrypted_values[0], input_y1,c1Prime, c2Prime)
        temp_denormalized_encrypted_value = normalized(denormalized(temp_encrypted_value)) # NORMALIZED_CEPTION

        # print("Encrypted: " + str(temp_denormalized_encrypted_value)) 
        # print("Original: " + str(normalized_original_values[1])) 

        encrypted_values.append(temp_denormalized_encrypted_value) 
        break
    
    #The Rest of the Indexes
    for i in range(2, len(normalized_original_values)):
        while True:
            temp_encrypted_value = encrypt_value(normalized_original_values[i], encrypted_values[i - 1], encrypted_values[i - 2], c1Prime, c2Prime)
            temp_denormalized_encrypted_value = normalized(denormalized(temp_encrypted_value)) # NORMALIZED_CEPTION

            # print("Encrypted: " + str(temp_denormalized_encrypted_value)) 
            # print("Original: " + str(normalized_original_values[i])) 

            encrypted_values.append(temp_denormalized_encrypted_value)
            break
    
    # Denormalized to [0, 255]
    for i in range(len(encrypted_values)):
        denormalized_encrypted_values.append(denormalized(encrypted_values[i]))

    return denormalized_encrypted_values

def decrypt_func(key, encrypted_values):
    normalized_encrypted_values = []
    decrypted_values = []
    denormalized_decrypted_values = []
    c1Prime, c2Prime = video_keysystem(key)
    #Convert Values [0,255] to Values [-1,1]
    for i in range(len(encrypted_values)): 
        normalized_encrypted_values.append(normalized(encrypted_values[i])) 

    #First Index
    decrypted_values.append(decrypt_value(normalized_encrypted_values[0], input_y1
, input_y2, c1Prime, c2Prime))
    #Second Index
    decrypted_values.append(decrypt_value(normalized_encrypted_values[1], normalized_encrypted_values[0], input_y1
, c1Prime, c2Prime))

    #The Rest of the Indexes
    for i in range(2, len(normalized_encrypted_values)): 
        decrypted_values.append(decrypt_value(normalized_encrypted_values[i], normalized_encrypted_values[i - 1], normalized_encrypted_values[i - 2], c1Prime, c2Prime))

    # Denormalized to [0, 255]
    for i in range(len(decrypted_values)):
        denormalized_decrypted_values.append(denormalized(decrypted_values[i]))
        
    return denormalized_decrypted_values


def encrypt_decrypt_image(key, og_frame):
    print("Encrypting Each Frame") 
    # Check if the image is loaded successfully
    if og_frame is None:
        print("Cannot encrypt frame.")
        return None
    else:
        # Reshape the image array to a one-dimensional array
        flattened_image = og_frame.ravel() # -1 means automatic calculation of the size

        # Print the flattened array of pixel values
        # print("Flattened pixel values array:\n", flattened_image) 
        # print("Original Length: " + str(len(flattened_image)))

        print("Encrypt: ")
        flattened__encrypted_image = encrypt_func(key, flattened_image)
        encrypted_image = np.reshape(flattened__encrypted_image, og_frame.shape)
        # Print the flattened array of pixel values
        # print("Encrypted pixel values array:\n", encrypted_image) 
        # print("Encrypted Length: " + str(len(encrypted_image))) 
        
        encrypted_image_path = "Computer_Security_Group5_Backend/video/videos/encrypted_frame/image_" + str(uuid.uuid4()) + ".png"
        cv2.imwrite(encrypted_image_path, encrypted_image, [cv2.IMWRITE_PNG_COMPRESSION, 0])

        # print("Flattened pixel values array:\n", flattened__encrypted_image) 
        # print("Original Length: " + str(len(flattened__encrypted_image)))
        # print("Decrypt: ") 
        
        decrypted_image = decrypt_func(key, flattened__encrypted_image)
        decrypted_image = np.reshape(decrypted_image, encrypted_image.shape)
        # Print the flattened array of pixel values
        # print("Decrypted pixel values array:\n", decrypted_image) 
        # print("Decrypted Length: " + str(len(decrypted_image))) 
        decrypted_image_path = "Computer_Security_Group5_Backend/video/videos/decrypted_frame/image_" + str(uuid.uuid4()) + ".png"
        cv2.imwrite(decrypted_image_path, decrypted_image)

        return encrypted_image_path, decrypted_image_path 
    
#encrypt_decrypt_image(key, cv2.imread(og_frame_path))

def encrypt_decrypt_video(key, video_path):
    cap = cv2.VideoCapture(video_path)

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    encrypted_video_path = "Computer_Security_Group5_Backend/video/videos/encrypted/video_" + str(uuid.uuid4()) + ".mp4"
    outEncrypted = cv2.VideoWriter(encrypted_video_path, fourcc, fps, (width, height))
    decrypted_video_path = "Computer_Security_Group5_Backend/video/videos/decrypted/video_" + str(uuid.uuid4()) + ".mp4"
    outDecrypted = cv2.VideoWriter(decrypted_video_path, fourcc, fps, (width, height))
    
    print ("Frame Count: " + str(frame_count))
    print ("FPS: " + str(fps))
    
    for _ in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break

        # Assuming you have an encrypt_image function
        # Replace "encrypt_image" with your actual encryption function
        encrypted_frame, decrypted_frame = encrypt_decrypt_image(key, frame)

        # You can also modify this part to save the frames in a temporary folder

        encrypted_frame_img = cv2.imread(encrypted_frame)
        decrypted_frame_img = cv2.imread(decrypted_frame)

        outEncrypted.write(encrypted_frame_img)
        outDecrypted.write(decrypted_frame_img)

        # Display the resulting frames
        cv2.imshow('Encrypted Frame', encrypted_frame_img)
        cv2.imshow('Decrypted Frame', decrypted_frame_img)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    outEncrypted.release()
    outDecrypted.release()
    cv2.destroyAllWindows()  # Close all the frames
    print ("Frame Count: " + str(frame_count))
    print ("FPS: " + str(fps))


video_path = 'Computer_Security_Group5_Backend/video/duck.mp4'
encrypt_decrypt_video(key, video_path)