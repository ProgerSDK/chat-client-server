import socket
import threading
import socketserver
import time
import config
import struct
from command_manager import *
import sys


class RequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        debug_message('{}:{} connected'.format(*self.client_address))

    def handle(self):
        while True:
            # get size of user message
            size_of_request = self.request.recv(4)
            
            # close the socket if the client is closed
            if not size_of_request: break
            
            # unpack size of user message
            size_of_request = struct.unpack('i', size_of_request)[0]
            debug_message(f'Size of message: {size_of_request}')
            
            # get user request message
            message = self.request.recv(size_of_request)
            
            # and handle command in message
            response = handle_command(message)

            # send the response size first
            try:
                size_of_response = struct.pack('i', len(response))
            except:
                response = create_response(constants.SERVER_ERROR)
                size_of_response = struct.pack('i', len(response))
            
            self.request.send(size_of_response)

            # send response
            self.request.send(response)

    def finish(self):
        debug_message('{}:{} disconnected'.format(*self.client_address))



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
        
        # while True:
        #     try:
        #         time.sleep(1)
        #     except KeyboardInterrupt:
        #         break
        
        server.shutdown()
