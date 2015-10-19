import re

import sys

import time

import socket

from os import path, stat


class ChillServer:
    ok_template = (
        'HTTP/1.1 200 OK\n'
        'Connection: close\n'
        'Date: %s\n'
        'Server: ChillServer\n'
        'Last-Modified: TODO\n'
        'Content-Length: %s\n'
        'Content-Type: %s\n\n'
    )
 
    not_mod_template = (
        'HTTP/1.1 304 Not Modified\n'
        'Date: %s\n'
        'Server: ChillServer\n\n'
    )

    def __init__(self, port):
        self.cool_port = port

    def get_time_info_string(self):
        time_zone = time.tzname[0]
        exact_time = time.strftime("%d %b %Y %H:%M:%S")
        return ("%s %s" % (exact_time, time_zone))

    def do_GET(self, request):
        response = None
        
        match = re.search(r'GET .+ HTTP/1.1', request)
        if match:
            #
            # Removes "GET" and "HTTP/1.1" from the file_name
            #
            file_name = match.group(0)[4:-9]
            last_mod_time = stat(file_name[1:]).st_mtime
            try:

                match = re.search('If-modified-since: .+', request) 

                if match:
                    if_mod_since = match.group(0)[18:]
                    if last_mod_time > float(if_mod_since):
                        response = not_mod_template % self.get_time_info_string()
                        return response.encode()

            except IndexError:
                pass

            if file_name == u'/' or file_name == '/':
                response = self.ok_template % (
                    self.get_time_info_string(),
                    path.getsize(file_name), 
                    'text/html',
                )

                response += (
                    'Welcome to the ChillServer. Have a cool stay!\r\n'
                    'And don\'t forget. What\'s cooler than being cool?\r\n'
                    'Ice cold!'
                )

                response = response.encode()

            else:
                #
                # Remove '/' from beginning of file name
                #
                file_name = file_name[1:]
                try:
                    if (
                        file_name[-3:] == 'htm' or 
                        file_name[-3:] == 'txt' or 
                        file_name[-4:] == 'html'
                    ):
                        with open(file_name, 'r') as f:
                            print(file_name[-3:])
                            file_type = 'text/html'
                            response = self.ok_template % (
                                self.get_time_info_string(),
                                path.getsize(file_name),
                                file_type,
                            )
                            response += f.read()
                            response = response.encode()

                    elif (
                        file_name[-4:] == 'jpeg' or 
                        file_name[-3:] == 'jpg'
                    ):
                        with open(file_name, 'rb') as f:
                            file_type = 'image/jpeg'
                            response = self.ok_template % (
                                self.get_time_info_string(),
                                path.getsize(file_name),
                                file_type,
                            )
                            #
                            # No need to encode the image. It's already in byte 
                            # format.
                            #
                            response = response.encode() + f.read()

                except FileNotFoundError:
                    response = 'HTTP/1.1 404 Not Found'.encode()

            return response

    request_commands = {
        'GET': do_GET,
        #'POST': self.do_POST
    }

    def handle_request(self, request):
        # request = request.decode().splitlines()
        request = request.decode()
        response = None
        for command in self.request_commands:
            if re.search(r'%s ' % command, request):
                response = self.request_commands[command](self, request)

                if response:
                    break

        if not response:
           respone = 'HTTP/1.1 404 Not Found'.encode()

        return response
 
    def serve_forever(self):
        """
        Starts the coolest server.

        """
        #
        # AF_INET = Internet Protocol v4
        # SOCK_STREAM = TCP
        #  
        cool_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#       self.cool_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cool_socket.bind(('', self.cool_port))
        cool_socket.listen(1)
       
        while True:
            client_connection, client_address = cool_socket.accept()
            request = client_connection.recv(1048576)
            print("REQUEST: %s" % request.decode())
            response = self.handle_request(request)
            print(response)

            if response:
                client_connection.sendmsg([response])
            # else:
            #    with open('errors.txt', 'a') as f:
            #        f.write('INVALID REQUEST: %s' % request.decode())

            client_connection.close()


if __name__ == '__main__':
    try:

        server = ChillServer(int(sys.argv[1]))
        server.serve_forever()

    except IndexError:
        print('Must enter a port number!')
