import sys
import os
sys.path.append(os.path.abspath("/home/rahul/PycharmProjects/LSTM-blog/"))
from SCIT import lstm_word
####################
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from os import curdir, sep
import cgi
import cgitb
cgitb.enable()
hostName = "localhost"
hostPort = 9000

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'

        try:
            # Check the file extension required and
            # set the right mime type

            sendReply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True
                
            if sendReply == True:
                # Open the static file requested and send it
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(bytes(f.read(),'utf-8'))
                f.close()
                # self.wfile.close()
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode('utf-8')
            a = post_data.split(' ')
            a = ("+".join(a))

            print(a)
            result=lstm_word.predictor(a)
            self.send_response(200)
            self.send_header('Content-type', 'text')
            self.end_headers()
            self.wfile.write(bytes(result,'utf-8'))
            #send to Front-End

        except:
            print ("Exception")

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
