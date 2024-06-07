import numpy as np
import cv2
        
def msgtobinary(msg):
    if type(msg) == str:
        result= ''.join([ format(ord(i), "08b") for i in msg ])
    
    elif type(msg) == bytes or type(msg) == np.ndarray:
        result= [ format(i, "08b") for i in msg ]
    
    elif type(msg) == int or type(msg) == np.uint8:
        result=format(msg, "08b")

    else:
        raise TypeError("Input type is not supported in this function")
    
    return result

def encode_img_data(img):
    data=input("\nEnter the data to be Encoded in Image :")    
    if (len(data) == 0): 
        raise ValueError('Data entered to be encoded is empty')
  
    nameoffile = input("\nEnter the name of the New Image (Stego Image) after Encoding :")    #since png format supports lossless compression which is required for LSB steganography
    
    no_of_bytes=(img.shape[0] * img.shape[1] * 3) // 8
    
    print("\t\nMaximum bytes to encode in Image :", no_of_bytes)
    
    if(len(data)>no_of_bytes):
        raise ValueError("Insufficient bytes Error, Need Bigger Image or give Less Data !!")
    
    data += 'abcd'   
    
    binary_data=msgtobinary(data)
    print("\n")
    print(binary_data)
    length_data=len(binary_data)
    
    print("\nThe Length of Binary data",length_data)
    
    index_data = 0
    
    for i in img:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data >= length_data:
                break
    cv2.imwrite(nameoffile,img)
    print("\nEncoded the data successfully in the Image and the image is successfully saved with name ",nameoffile)


def decode_img_data(img):
    data_binary = ""
    for i in img:
        for pixel in i:
            r, g, b = msgtobinary(pixel) 
            data_binary += r[-1]  
            data_binary += g[-1]  
            data_binary += b[-1]  
            total_bytes = [ data_binary[i: i+8] for i in range(0, len(data_binary), 8) ]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-4:] == "abcd": 
                    if decoded_data == "abcd":          #for edge case when delimiter is taken as text message
                        print("\n\nThe Encoded data which was hidden in the Image was :--  ",decoded_data[:4])
                        return
                    print("\n\nThe Encoded data which was hidden in the Image was :--  ",decoded_data[:-4])
                    return 
                
def img_steg():
    
    while True:
        print("\n\t\tIMAGE STEGANOGRAPHY OPERATIONS")
        print("You can perform the following operations:")
        print("- Type 'encode' to Encode the Text message")
        print("- Type 'decode' to Decode the Text message")
        print("- Type 'exit' to return to the main menu")
        command = input("\nEnter your command: ").strip().lower()
        
        if command == 'encode':
            image_path = "Sample_cover_files/cover_image.jpg"
            try:
                image = cv2.imread(image_path)
                if image is None:
                    print("Failed to load image. Please check the path and try again.")
                    continue
                encode_img_data(image)
            except Exception as e:
                print(f"An error occurred: {e}")
        
        elif command == 'decode':
            image_path = input("Enter the file name of the image to be decoded: ").lower().strip()
            try:
                image = cv2.imread(image_path)
                if image is None:
                    print("Failed to load image. Please check the path and try again.")
                    continue
                decode_img_data(image)
            except Exception as e:
                print(f"An error occurred: {e}")
        
        elif command == 'exit':
            print("Returning to the main menu.")
            break
        
        else:
            print("Invalid command. Please enter 'encode', 'decode', or 'exit'.")

def KSA(key):
    key_length = len(key)
    S=list(range(256)) 
    j=0
    for i in range(256):
        j=(j+S[i]+key[i % key_length]) % 256
        S[i],S[j]=S[j],S[i]
    return S

def PRGA(S,n):
    i=0
    j=0
    key=[]
    while n>0:
        n=n-1
        i=(i+1)%256
        j=(j+S[i])%256
        S[i],S[j]=S[j],S[i]
        K=S[(S[i]+S[j])%256]
        key.append(K)
    return key

def preparing_key_array(s):
    return [ord(c) for c in s]

def encryption(plaintext):
    print("Enter the key : ")
    key=input()
    key=preparing_key_array(key)

    S=KSA(key)

    keystream=np.array(PRGA(S,len(plaintext)))
    plaintext=np.array([ord(i) for i in plaintext])

    cipher=keystream^plaintext
    ctext=''
    for c in cipher:
        ctext=ctext+chr(c)
    return ctext

def decryption(ciphertext):
    print("Enter the key : ")
    key=input()
    key=preparing_key_array(key)

    S=KSA(key)

    keystream=np.array(PRGA(S,len(ciphertext)))
    ciphertext=np.array([ord(i) for i in ciphertext])

    decoded=keystream^ciphertext
    dtext=''
    for c in decoded:
        dtext=dtext+chr(c)
    return dtext


def embed(frame):
    data=input("\nEnter the data to be Encoded in Video :") 
    data=encryption(data)
    print("The encrypted data is : ",data)
    if (len(data) == 0): 
        raise ValueError('Data entered to be encoded is empty')

    data +='abcd'
    
    binary_data=msgtobinary(data)
    length_data = len(binary_data)
    
    index_data = 0
    
    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2) 
                index_data += 1
            if index_data >= length_data:
                break
        return frame

def extract(frame):
    data_binary = ""
    final_decoded_msg = ""
    for i in frame:
        for pixel in i:
            r, g, b = msgtobinary(pixel) 
            data_binary += r[-1]  
            data_binary += g[-1]  
            data_binary += b[-1]  
            total_bytes = [ data_binary[i: i+8] for i in range(0, len(data_binary), 8) ]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-4:] == "abcd": 
                    if decoded_data == "abcd":          #for edge case when delimiter is taken as text message
                        print("\n\nThe Encoded data which was hidden in the Video was :-- ",decoded_data[:4])
                        return
                    for i in range(0,len(decoded_data)-4):
                        final_decoded_msg += decoded_data[i]
                    final_decoded_msg = decryption(final_decoded_msg)
                    print("\n\nThe Encoded data which was hidden in the Video was :-- ",final_decoded_msg)
                    return 

def encode_vid_data():
    # for video 
    cap=cv2.VideoCapture("Sample_cover_files/cover_video.mp4")
    vidcap = cv2.VideoCapture("Sample_cover_files/cover_video.mp4")  
      
    # for gif
    # cap = cv2.VideoCapture("Sample_cover_files/cover_gif.gif")
    # vidcap = cv2.VideoCapture("Sample_cover_files/cover_gif.gif")
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = int(vidcap.get(3))
    frame_height = int(vidcap.get(4))

    size = (frame_width, frame_height)
    nameoffile=input("Enter the name of the stego file in mp4 format :- ")
    out = cv2.VideoWriter(nameoffile,fourcc, 25.0, size)
    max_frame=0;
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame+=1
    cap.release()
    print("Total number of Frame in selected Video :",max_frame)
    print("Enter the frame number where you want to embed data : ")
    n=int(input())
    frame_number = 0
    while(vidcap.isOpened()):
        frame_number += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_number == n:    
            change_frame_with = embed(frame)
            frame_ = change_frame_with
            frame = change_frame_with
        out.write(frame)
    
    print("\nEncoded the data successfully in the video file.")
    return frame_

def decode_vid_data(frame_):
    cap = cv2.VideoCapture('stego_video.mp4')
    max_frame=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        max_frame+=1
    print("Total number of Frame in selected Video :",max_frame)
    print("Enter the secret frame number from where you want to extract data")
    n=int(input())
    nameofstegofile=input("Enter the name of the stego file to be decoded :- ")
    vidcap = cv2.VideoCapture(nameofstegofile)
    frame_number = 0
    while(vidcap.isOpened()):
        frame_number += 1
        ret, frame = vidcap.read()
        if ret == False:
            break
        if frame_number == n:
            extract(frame_)
            return

def vid_steg():

    video_encoded = None  # Placeholder for the encoded video data

    while True:
        print("\n\t\tVIDEO STEGANOGRAPHY OPERATIONS")
        print("You can perform the following operations:")
        print("- Type 'encode' to Encode the Text message into a video")
        print("- Type 'decode' to Decode the Text message from a video")
        print("- Type 'exit' to return to the main menu")
        command = input("\nEnter your command: ").strip().lower()

        if command == 'encode':
            try:
                video_encoded = encode_vid_data()
                print("Text message successfully encoded into the video.")
            except Exception as e:
                print(f"An error occurred during encoding: {e}")
        
        elif command == 'decode':
            if video_encoded is None:
                print("No video data available for decoding. Please encode a video first.")
            else:
                try:
                    decode_vid_data(video_encoded)
                    print("Text message successfully decoded from the video.")
                except Exception as e:
                    print(f"An error occurred during decoding: {e}")
        
        elif command == 'exit':
            print("Returning to the main menu.")
            break
        
        else:
            print("Invalid command. Please enter 'encode', 'decode', or 'exit'.")

def main():
    
    while True: 
        print("\t\t      WELCOME TO STEGANOGRAPHY TOOLKIT")
        print("You can perform the following steganography operations:")
        print("- Type 'image' to perform Image Steganography {Hiding Text in Image cover file}")
        print("- Type 'video' to perform Video Steganography {Hiding Text in Video cover file}")
        print("- Type 'exit' to exit the program")
 
        command = input("\nEnter your command: ").strip().lower()

        if command == 'image': 
            img_steg()
        elif command == 'video':
            vid_steg()
        elif command == 'exit':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid command. Please enter one of the following: 'image', 'text', 'audio', 'video', or 'exit'.")
        print("\n")

if __name__ == "__main__":
    main()


