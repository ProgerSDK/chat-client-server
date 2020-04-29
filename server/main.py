import socket
import threading
import socketserver
import time

HOST = '127.0.0.1'  # standard ip
PORT = 9090         # standard port


class RequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'utf-8')
        self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    host = HOST
    port = PORT

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
            if (input('Enter something to exit:\n-> ')):
                break

        server.shutdown()
