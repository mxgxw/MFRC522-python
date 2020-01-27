import time

from telnetlib import Telnet

def readState():
    tn = Telnet('localhost', 6600)
    tn.read_until('OK'.encode('UTF-8'), 5).decode('UTF-8')

    tn.write('status\n'.encode('UTF-8'))

    result = tn.read_until('OK'.encode('UTF-8'), 5).decode('UTF-8')
    
    tn.write('currentsong\n'.encode('UTF-8'))

    result = result + tn.read_until('OK'.encode('UTF-8'), 5).decode('UTF-8')
    
    return result.split('\n')
    
def sendCommand(cmd):
    sendCommands([cmd])
    pass

def sendCommands(cmds):
    tn = Telnet('localhost', 6600)

    tn.read_until('OK'.encode('UTF-8'), 5).decode('UTF-8')

    if currentVolume() == 0 and "play" in cmds:
        cmds.insert(0, 'setvol 20')

    for cmd in cmds:
        cmdToSend = cmd
        if not cmdToSend.endswith('\n'):
            cmdToSend = cmdToSend + '\n'

        print("Telnet command will be send to mpd: " + cmdToSend[0:len(cmdToSend)-1])

        tn.write(cmdToSend.encode('UTF-8'))
        tn.read_until('OK'.encode('UTF-8'), 5).decode('UTF-8')

    tn.close()
    return

def changeVolume(volumeChange):
    oldVolume = currentVolume()
    newVolume = oldVolume + volumeChange
    setVolume(newVolume)

def setVolume(newVolume):
    if newVolume < 0:
        newVolume = 0
    
    if newVolume > 100:
        newVolume = 100

    sendCommand('setvol ' + str(newVolume))
    print("Current Volume is now " + str(currentVolume()))
 

def currentVolume():
    volume = 0
    resultList = readState()
    for line in resultList:
        #print(line)
        tokens = line.split(": ", 1)
        if 'volume' == tokens[0]:
            volume = int(tokens[1])
        #print("Volume is currently set to " + str(volume))
    return volume


def play():
    sendCommand('play')
    pass
    
    

def isPlaying():
    radio = False
    playing = False
    resultList = readState()
    for line in resultList:
        #print(line)
        tokens = line.split(": ", 1)
        if 'file' == tokens[0] and 'http' in tokens[1]:
            radio = True
        if 'state'==tokens[0] and 'play'==tokens[1]:
            playing = True
            
    return playing, radio

if __name__ == "__main__":

    print(isPlaying())
    pass