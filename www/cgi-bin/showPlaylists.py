#!/usr/bin/env python3

from telnetlib import Telnet

def readPlaylist():
    tn = Telnet('localhost', 6600)
    tn.read_until('OK'.encode('UTF-8'), 5).decode('UTF-8')

    tn.write('listplaylists\n'.encode('UTF-8'))

    result = tn.read_until('OK'.encode('UTF-8'), 5).decode('UTF-8')
    listResult = []
    for s in result.split('\n'):
        if 'playlist: ' in s and '[Radio Streams]' not in s:
            listResult.append( s[10:])
    listResult = sorted(listResult)
    return listResult

print ('Content-type: application/json\r\n\r\n')

#print ('{"playlists": ["Test", "Test1", "Test2"]}')
print ('{"playlists": [')
firstEntry = True
for s in readPlaylist():
    if firstEntry:
        firstEntry = False
    else:
        print (',')
    #print ('"Blabla"')
    print(f"\"{s}\"")
print (']}')
