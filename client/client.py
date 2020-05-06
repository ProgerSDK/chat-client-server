import socket
import struct
import time


class Client:

    def __init__(self):
        # Create a socket (SOCK_STREAM means a TCP socket)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connect(self, host, port):
        self.sock.connect((host, port))


    def handle(self, request) -> bytes:
        # convert query size to bytes (int 4)
        size_of_request = struct.pack('i', len(request))

        # send the request size first
        self.sock.send(size_of_request)
        time.sleep(0.5)

        # send request
        self.sock.send(request)
        time.sleep(0.5)

        # get size of server response
        recv_size = self.sock.recv(4)
        # and unpack it
        recv_size = struct.unpack('i', recv_size)[0]

        # receive data from the server
        response = self.sock.recv(recv_size)
        
        return response


    def __del__(self):
        self.sock.close()
