import speech_recognition as sr
import os
import RPi.GPIO as GPIO
import time




GPIO.setwarnings(False)
dotvb=21
dashvb=20
spacevb=16
GPIO.setmode(GPIO.BCM)
GPIO.setup((dotvb,dashvb,spacevb), GPIO.OUT)


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
        audio = r.listen(source,phrase_time_limit=3)
    try:
        texti= r.recognize_google(audio)
        print('Speaker said :' + texti)
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


while True:
    #lms=GPIO.input(Listen_mode)
    recv()
