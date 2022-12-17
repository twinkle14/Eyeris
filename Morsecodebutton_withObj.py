import speech_recognition as sr
import os
import RPi.GPIO as GPIO
import time

import numpy as np
import sys
import imutils
import cv2

from subprocess import call#to call espeak function

global lms
global sms
GPIO.setwarnings(False)
Listen_mode=16
Speak_mode=18
dot=37
dash=35
space=33
end=31
dotvb=40
dashvb=38
spacevb=36
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Listen_mode, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Speak_mode, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dot, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dash, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(space, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(end, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup((dotvb,dashvb,spacevb), GPIO.OUT)

#espeak
cmd_beg = "espeak "
#text ="This is a sample code to speal in Raspberry PI"
cmd_out=" -ven+m1 -s 150 -a 300"


r = sr.Recognizer()

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-'} 
 
 
 
a="/home/pi/Desktop/GLOS/MobileNetSSD_deploy.prototxt.txt"
b="/home/pi/Desktop/GLOS/MobileNetSSD_deploy.caffemodel"
# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "fan", "bicycle", "fan", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(a, b)



vs = cv2.VideoCapture(0)

time.sleep(2.0)

detected_objects = [] 
 
 
def obj():
    #lms=GPIO.input(Listen_mode)
    #sms=GPIO.input(Speak_mode)
    while 1:
        lms=GPIO.input(Listen_mode)
        sms=GPIO.input(Speak_mode)
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        
        ret, frame = vs.read()
        
        frame = imutils.resize(frame, width=800)
            
        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
            0.007843, (300, 300), 127.5)

        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()
        
        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > 0.8:
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(CLASSES[idx],
                    confidence * 100)
                detected_objects.append(label)
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                    COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                print(CLASSES[idx])
                text=CLASSES[idx]
                result = encrypt(text.upper())
                print (result)
                for ele in encrypt(text.upper()):
                    if (ele=='.'):
                        GPIO.output(dotvb,1)
                        time.sleep(0.3)
                        GPIO.output(dotvb,0)
                        time.sleep(0.1)
                    elif (ele=='-'):
                        GPIO.output(dashvb,1)
                        time.sleep(0.3)
                        GPIO.output(dashvb,0)
                        time.sleep(0.1)
                    elif (ele==' '):
                        GPIO.output(spacevb,1)
                        time.sleep(0.3)
                        GPIO.output(spacevb,0)
                        time.sleep(0.1)
        
        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if ((key == ord("q")) or ((lms==0 or sms==0))):
            cv2.destroyAllWindows()
            break   
 
 
#{
#input from Microphone
def get_text():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source,phrase_time_limit=5)
    try:
        texti= r.recognize_google(audio)
        print('Speaker said' + texti)
    except sr.UnknownValueError:
        print("could not understand audio")
        texti="e"
    except sr.RequestError as e:
        print("error; {0}".format(e))
        texti="e"
    return texti

#}

#{
# Function to encrypt the string 
# according to the morse code chart 
def encrypt(message): 
    cipher = '' 
    for letter in message: 
        if letter != ' ': 
  
            # Looks up the dictionary and adds the 
            # correspponding morse code 
            # along with a space to separate 
            # morse codes for different characters 
            cipher += MORSE_CODE_DICT[letter] + ' '
        else: 
            # 1 space indicates different characters 
            # and 2 indicates different words 
            cipher += ' '
  
    return cipher
def decrypt(message): 
  
    # extra space added at the end to access the 
    # last morse code 
    message += ' '
  
    decipher = '' 
    citext = ''
    for letter in message: 
  
        # checks for space 
        if (letter != ' '): 
  
            # counter to keep track of space 
            i = 0
  
            # storing morse code of a single character 
            citext += letter 
  
        # in case of space 
        else: 
            # if i = 1 that indicates a new character 
            i += 1
  
            # if i = 2 that indicates a new word 
            if i == 2 : 
  
                 # adding space to separate words 
                decipher += ' '
            else: 
  
                # accessing the keys using their values (reverse of encryption) 
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT 
                .values()).index(citext)] 
                citext = '' 
  
    return decipher 

#}


#{
def recv():
    #text = input("Enter text:")
    text = get_text()
    result = encrypt(text.upper())
    print (result)
    for ele in encrypt(text.upper()):
        if (ele=='.'):
            GPIO.output(dotvb,1)
            time.sleep(0.3)
            GPIO.output(dotvb,0)
            time.sleep(0.1)
        elif (ele=='-'):
            GPIO.output(dashvb,1)
            time.sleep(0.3)
            GPIO.output(dashvb,0)
            time.sleep(0.1)
        elif (ele==' '):
            GPIO.output(spacevb,1)
            time.sleep(0.3)
            GPIO.output(spacevb,0)
            time.sleep(0.1)
     
    #return texti
#}

#{
def listToString(c):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in c:  
        str1 += ele   
    
    # return string   
    return str1  
def send():
    print ('\n\na means "." \ns means "-" \nd means space \nEnter morse code:')
    c=[]
    while (sms==0):
        
        #d=input()
        dots= GPIO.input(dot)
        dashs=GPIO.input(dash)
        spaces=GPIO.input(space)
        ends=GPIO.input(end)
        if dots==0:
        #if d=='a':
            time.sleep(0.5)
            c.append('.');
            print(c)
        elif dashs==0:
        #elif d=='s':
            time.sleep(0.5)
            c.append('-');
            print(c)
        elif spaces==0:
        #elif d=='d':
            time.sleep(0.5)
            c.append(' ');
            print(c)
        elif ends==0:
        #else:
            break
    f=''.join(str(e) for e in c)
    print(f) 
    result = decrypt(listToString(c)) 
    print (result)
    call(cmd_beg+"\""+result+"\""+cmd_out,shell=True)

#}


while True:
    
    lms=GPIO.input(Listen_mode)
    sms=GPIO.input(Speak_mode)
    
    if(lms==0):
        print("Entered into Listen Mode")
        recv()
        continue
    elif(sms==0):
        print("Entered into Speak Mode")
        send()
        continue
    else:
        print('Idle')
        obj()
        continue
        time.sleep(1)
    
