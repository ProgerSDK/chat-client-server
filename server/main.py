import socket
import threading
import socketserver
import time
import config
import struct
from command_manager import *


class RequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # get size of user message
        size = self.request.recv(4)
        size_of_message = struct.unpack('i', size)
        
        print(f'\n\nSize of message: {size_of_message[0]}')
        
        # get user message
        message = self.request.recv(size_of_message[0])
        # and check command in message
        handle_command(message)

        # send response
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, message), config.ENCODING)
        self.request.sendall(response)



class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    pass



if __name__ == '__main__':
    host = config.HOST
    port = config.PORT

    server = ThreadedTCPServer((host, port), RequestHandler)
    with server:    
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)

        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)
        
        # Exit when user enters something
        while True:
            if (input('Enter something to exit: -> ')):
                break

        server.shutdown()
