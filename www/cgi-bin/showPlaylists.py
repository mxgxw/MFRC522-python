#!/usr/bin/env python

from telnetlib import Telnet

def readPlaylist():
    tn = Telnet('localhost', 6600)
    tn.read_until('OK'.encode('UTF-8'), 5).decode('UTF-8')

    tn.write('listplaylists\n'.encode('UTF-8'))

    result = tn.read_until('OK'.encode('UTF-8'), 5).decode('UTF-8')
    listResult = []
    for s in result.split('\n'):
        if 'playlist: ' in s and '[Radio Streams]' not in s:
            listResult.append( str(s[10:]))
    listResult = sorted(listResult, key=str.lower)
    return listResult

print 'Content-type: application/json'
print
#print '{"playlists": ["bla", "bla2", "bla3"]}'

print ('{"playlists": [')
firstEntry = True
for s in readPlaylist():
    if firstEntry:
        firstEntry = False
    else:
        print ',',
    print '"' + s + '"',

print (']}')
