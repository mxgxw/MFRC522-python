#!/usr/bin/env python
 
import BaseHTTPServer
import CGIHTTPServer
import os
import cgitb; cgitb.enable()  ## This line enables CGI error reporting
 
HTTP_SERVER_PORT = 80

class RadioHttpServer:

        # parameterized constructor 
    def __init__(self, wwwPath): 
        self.wwwPath = wwwPath

    def startHttpServer(self, args):
        web_dir = os.path.join(os.path.dirname(__file__), self.wwwPath)
        os.chdir(web_dir)

        print ("Staring HTTP server on port " + str(HTTP_SERVER_PORT))
        self.server = BaseHTTPServer.HTTPServer
        handler = CGIHTTPServer.CGIHTTPRequestHandler
        server_address = ("", HTTP_SERVER_PORT)
        handler.cgi_directories = ["/cgi-bin"]

        self.httpd = self.server(server_address, handler)
        self.httpd.serve_forever()


    def stopHttpServer(self):
        self.httpd.shutdown()

if __name__ == "__main__":
    httpServer = RadioHttpServer('www')
    httpServer.startHttpServer(None)
