# import sys
import socket
import struct
import config
from request_manager import create_request
from response_manager import unpack_response
from input_manager import *
import time


# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server
    sock.connect((config.HOST, config.PORT))
    
    while True:
        user_input = get_user_input()

        if (user_input.lower() == 'exit'):
            break
        
        # get the command number and args of cmd in dict
        command = handle_input(user_input)
        cmd_code = command['cmd_code']

        # then create request using the command
        request = create_request(command)
        
        # convert query size to bytes (int 4)
        size_of_request = struct.pack('i', len(request))

        # send the request size first
        sock.send(size_of_request)
        time.sleep(0.5)

        # send request
        sock.send(request)
        time.sleep(1)

        # get size of server response
        recv_size = sock.recv(4)
        # and unpack it
        recv_size = struct.unpack('i', recv_size)[0]

        # receive data from the server
        response = sock.recv(recv_size)
        # and unpack it
        unpack_response(cmd_code, response)
    