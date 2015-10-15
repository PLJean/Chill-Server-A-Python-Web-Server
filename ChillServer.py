import os

import re

import sys

import time

import socket


class ChillServer:
   response_template = (
      '''HTTP/1.1 200 OK
Connection: close
Date: %s
Server: ChillServer (v. Approximately Over 9000)
Last-Modified: TODO
Content-Length: %s
Content-Type: TODO

%s
      '''
   )

   def __init__(self, port):
      self.cool_port = port

   def get_time_info_string(self):
      time_zone = time.tzname[0]
      exact_time = time.strftime("%d %b %Y %H:%M:%S")
      return ("%s %s" % (exact_time, time_zone))
 
   def do_GET(self, request_lines):
      response = None
      if request_lines[0][0:3] == 'GET':
         match = re.search(r'GET .+ HTTP/1.1', request_lines[0])
         #
         # Removes "GET" and "HTTP/1.1" from the file_name
         #
         file_name = match.group(0)[4:-9]
         if file_name == u'/' or file_name == '/':
            response = self.response_template % (
               self.get_time_info_string(),
               os.path.getsize(file_name),
               '''Welcome to the ChillServer. Have a cool stay!
               
And don't forget. What's cooler than being cool? Ice cold!
               '''
            )

      else:
         try:
	   
            with open(file_name) as f:
               response = self.response_template % (
                  self.get_time_info_string(),
                  os.path.getsize(match.group(0)),
  		  f
               )
 
            except AttributeError:
               response = 'HTTP/1.1 404 Not Found'

      return response

   request_commands = {
      'GET': do_GET,
      #'POST': self.do_POST
   }

   def handle_request(self, request):
      request_lines = request.decode().splitlines()
      response = None
      for command in self.request_commands:
         if re.search(r'%s ' % command, request_lines[0]):
            response = self.request_commands[command](self, request_lines)
            if response:
               break

      return response
 
   def serve_forever(self):
      """
      Starts the coolest server. 

      """
      
      # AF_INET = Internet Protocol v4; SOCK_STREAM = TCP 
      self.cool_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#      self.cool_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.cool_socket.bind(('', self.cool_port))
      self.cool_socket.listen(1)
       
      while True:
         client_connection, client_address = self.cool_socket.accept()
         request = client_connection.recv(8192)
         print("REQUEST: %s" % request.decode().split('\n'))
         response = self.handle_request(request)
	 print(response)
	 
         if response:
            client_connection.sendmsg([http_response])
         else:
            with open('errors.txt', 'a') as f:
               f.write('INVALID REQUEST: %s' % request.decode())
 	 
         client_connection.close()


if __name__ == '__main__':
   try: 

      server = ChillServer(int(sys.argv[1]))
      server.serve_forever()

   except IndexError: 
       print('Must enter a port number!')
