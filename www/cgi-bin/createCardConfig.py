#!/usr/bin/env python
 
import cgi
import configparser
import logging
 
WRITE_CARD_FILE = "/var/run/radioControl/writeCard"

form = cgi.FieldStorage()
 
playlist = form.getvalue('playlist')
random = form.getvalue('random')

print ("Playlistname: " + str(playlist))
print ("Random: " + str(random))

config = configparser.ConfigParser()
config.add_section('Card')
config.set('Card', 'playlist',str(playlist))
config.set('Card', 'random', str(random))

# Writing our configuration file to 'example.cfg'
with open(WRITE_CARD_FILE, 'wb') as configfile:
    config.write(configfile)

print str(form)

print 'Content-type: text/html' 
print
print '<html><head><title>Test URL Encoding</title></head><body>'
print 'Hello my name is %s %s' % (playlist, random)
print '</body></html>' 