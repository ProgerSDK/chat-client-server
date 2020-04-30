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
        size_of_request = self.request.recv(4)
        size_of_request = struct.unpack('i', size_of_request)
        debug_message(f'Size of message: {size_of_request[0]}')
        
        # get user request message
        message = self.request.recv(size_of_request[0])
        
        # and handle command in message
        response = handle_command(message)

        # send first size of response
        self.request.send(len(response))

        # send response
        self.request.sendall(response)
        # //cur_thread = threading.current_thread()
        # //response = bytes("{}: {}".format(cur_thread.name, message), config.ENCODING)



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
            if (input('Enter something to exit:\n')):
                break

        server.shutdown()
