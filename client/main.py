import socket
import struct
import config
import time
from input_manager import get_command
from request_manager import create_request
from response_manager import unpack_response, is_error
from constants import CMD_EXIT, CMD_LOGOUT, CMD_LOGIN
import constants
import threading
import auto_receiver


def create_receiver(response, request):
    response_code = struct.unpack('b', response)[0]
    
    if ((response_code == constants.CMD_LOGIN_OK_NEW) 
        or (response_code == constants.CMD_LOGIN_OK)):
        
        # create new thread
        receiver_thread = threading.Thread(target=auto_receiver.create_receiver, args=(request,))

        # exit the receiver thread when the main thread terminates
        receiver_thread.daemon = True
        receiver_thread.start()



# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server
    sock.connect((config.HOST, config.PORT))

    while True:

        # get the command number and args of cmd in dict
        # from user input
        command = get_command()
        if (command['cmd_code'] == CMD_EXIT):
            print('\nShutdown the client...')
            break
        
        # get cmd_come to get response
        cmd_code = command['cmd_code']

        # then create request using the command
        request = create_request(command)

        # check for errors
        if is_error(request):
            print('Please retry!\n')
            continue

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
        
        if (cmd_code == CMD_LOGIN):
            create_receiver(response, request)

        # and unpack it
        unpack_response(cmd_code, response)
     