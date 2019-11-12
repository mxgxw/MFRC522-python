#!/usr/bin/python
import RPi.GPIO as GPIO
import MFRC522
import os
import time

buttonDebounceTime = 500

def button_volume_up(channel):
    cmd = 'mpc volume +5'
    print ("Command will be send: " + cmd)
    os.system(cmd) 

def button_volume_down(channel):
    cmd = 'mpc volume -5'
    print ("Command will be send: " + cmd)
    os.system(cmd) 

def button_pause(channel):
    cmd ='mpc toggle'
    print ("Command will be send: " + cmd)
    os.system(cmd)

def button_track_next(channel):
    cmd ='mpc next'
    print ("Command will be send: " + cmd)
    os.system(cmd)

def button_track_prev(channel):
    cmd ='mpc prev'
    print ("Command will be send: " + cmd)
    os.system(cmd)

GPIO.setmode(GPIO.BOARD) 

BUTTON_VOLUME_UP    = 18
BUTTON_VOLUME_DOWN  = 16
BUTTON_PAUSE        = 15
BUTTON_TRACK_PREV   = 11
BUTTON_TRACK_NEXT   = 13

GPIO.setup(BUTTON_VOLUME_UP, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_VOLUME_DOWN, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PAUSE, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_TRACK_PREV, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_TRACK_NEXT, GPIO.IN,  pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(BUTTON_VOLUME_UP,GPIO.FALLING,callback=button_volume_up,bouncetime=buttonDebounceTime) 
GPIO.add_event_detect(BUTTON_VOLUME_DOWN,GPIO.FALLING,callback=button_volume_down,bouncetime=buttonDebounceTime)
GPIO.add_event_detect(BUTTON_PAUSE,GPIO.FALLING,callback=button_pause,bouncetime=buttonDebounceTime)
GPIO.add_event_detect(BUTTON_TRACK_NEXT,GPIO.FALLING,callback=button_track_next,bouncetime=buttonDebounceTime)
GPIO.add_event_detect(BUTTON_TRACK_PREV,GPIO.FALLING,callback=button_track_prev,bouncetime=buttonDebounceTime)

lastCardUID = None

def read_card(reader, key):
    # Scan for cards    
    (status, tag_type) = reader.MFRC522_Request(reader.PICC_REQIDL)
    global lastCardUID


    # If a card is found
    if status != reader.MI_OK:
        (status, tag_type) = reader.MFRC522_Request(reader.PICC_REQIDL)
        if status != reader.MI_OK:
            if lastCardUID != None:
                print ("Card removed " + lastCardUID)
            lastCardUID = None
            return None
    print ("Card detected")
            
    # Get the UID of the card
    (status, uid) = reader.MFRC522_Anticoll()
    currentCard = ""

    first = True

    for token in uid:
        if not first: 
            currentCard += ":"
        first = False
        currentCard += str(token)


    # If we have the UID, continue
    if status != reader.MI_OK:
        print ("Error during card read.")
        lastCardUID = None
        return None

    # Print UID
    print ("Card read UID: " + currentCard)

    if currentCard == lastCardUID:
        return None

    # Select the scanned tag
    reader.MFRC522_SelectTag(uid)

    # Authenticate
    status = reader.MFRC522_Auth(reader.PICC_AUTHENT1A, 4, key, uid)

    # Check if authenticated
    if status != reader.MI_OK:
        print ("Authentication error")
        return None

    lastCardUID = currentCard

    if os.path.isfile("./writeCard"):
        print ("write file found")
        fobj = open("./writeCard")
        playlist = fobj.readline().strip()
        fobj.close()
        
        print ("Playlist name is " + playlist)

        writeData = [int("0x13", 0), int("0x37", 0), int("0xb3", 0), int("0x47", 0)]

        writeData.append(2) # Version 2
        writeData.append(0) # For version it was the  folder
        writeData.append(0) # Random value

        # Fill the data with 0xFF
        for x in range(7,16):
            writeData.append(0)
        
        print ("Sector 4 will now be filled with data. Length = " + str(len(writeData)) + " Data: " + str(writeData))
        # Write the data
        reader.MFRC522_Write(4, writeData)
        
        writeData = []
        # Fill the data with 0xFF
        for s in playlist:
            writeData.append(ord(s))
            
        nameLength = len(playlist)
        print ("The playlistname " + playlist + " has a length of " + str(nameLength))
        for x in  range(nameLength, 16):
            writeData.append(0)
        
        print ("Sector 5 will now be filled with data. Length = " + str(len(writeData)) + " Data: " + str(writeData))
        reader.MFRC522_Write(5, writeData)
        os.remove("./writeCard")

    data4 = reader.MFRC522_Read(4)
    if data4 != None and data4[4] != 1:
        data5 = reader.MFRC522_Read(5)
    else:
        data5 = None
    reader.MFRC522_StopCrypto1()
    if data4 == None:
        return None
    return (data4, data5)

def main():
    try:
        reader = MFRC522.MFRC522()

        # Welcome message
        print ("Welcome to the MFRC522 data read example")
        print ("Press Ctrl-C to stop.")

        # This is the default key for authentication
        key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        # This loop keeps checking for chips. If one is near it will get the UID and authenticate
        while True:
            time.sleep(1)
            cardData = read_card(reader, key) 
            if cardData != None:
                (data4, data5) = cardData
                random = data4[6] == 1 
                if data4[4] == 1:
                    os.system("mpc stop")
                    os.system("mpc clear")
                    cmd = 'mpc load ' + "{:02d}".format(data4[5]) 
                    
                if data4[4] == 2 :
                    if data5 == None:
                        lastCardUID = None
                    else :
                        playlistname = ""
                        for c in data5:
                            if c != 0:
                                playlistname += chr(c)
                        os.system("mpc stop")
                        os.system("mpc clear")
                        cmd = 'mpc load ' + playlistname
                
                os.system(cmd)
                if random:
                    os.system('mpc random on')
                else:
                    os.system('mpc random off')
                os.system('mpc play')
                
                
    
    except KeyboardInterrupt:
        print ("Ctrl+C captured, ending read.")
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()


