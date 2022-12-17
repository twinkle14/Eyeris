import speech_recognition as sr
import os
import RPi.GPIO as GPIO
import time

from subprocess import call#to call espeak function


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
        time.sleep(1)
    
