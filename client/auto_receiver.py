import constants
import struct
import time
import config
import json
import socket
import tkinter as tk

messages_frame = None

def create_receiver(request, frame):
    global messages_frame
    messages_frame = frame

    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server
        sock.connect((config.HOST, config.PORT))

        # convert query size to bytes (int 4)
        size_of_request = struct.pack('i', len(request))

        # send the request size first
        sock.send(size_of_request)
        time.sleep(0.5)

        # send request
        sock.send(request)
        time.sleep(0.5)

        # get size of server response
        recv_size = sock.recv(4)
        # and unpack it
        recv_size = struct.unpack('i', recv_size)[0]
        
        # receive data from the server
        response = sock.recv(recv_size)

        while True:
            time.sleep(2)
            command = {
                'cmd_code': constants.CMD_RECEIVE_MSG,
                'args': None
            }
            
            # get cmd_come to get response
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
            time.sleep(0.5)

            # get size of server response
            recv_size = sock.recv(4)
            # and unpack it
            recv_size = struct.unpack('i', recv_size)[0]

            # receive data from the server
            response = sock.recv(recv_size)

            # and unpack it
            unpack_response(constants.CMD_RECEIVE_MSG, response)



def create_request(command: dict) -> bytes:
    cmd_code = command['cmd_code']
    request = get_request_code(constants.CMD_RECEIVE_MSG)
    return request


def unpack_response(cmd_code: int, response: bytes) -> None:
    if (len(response) == 1):
        return
    
    response_content = response.decode(config.ENCODING)
    msg = json.loads(response_content)
    
    msg_val = f'{msg["sender"]}:\n{msg["message"]}'
    messageVar = tk.Message(messages_frame.scrollable_frame, text = msg_val, width=320) 
    # messageVar.config(bg='lightgreen') 
    messageVar.pack(anchor=tk.W, pady=2, padx=2)
    
    # print('\nYou have a new message!')
    # print(f'From: {msg["sender"]}')
    # print(f'Message: {msg["message"]}')
    


def get_request_code(code: int) -> bytes:
    request = struct.pack('b', code)
    return request


def unpack_response_code(response: bytes) -> int:
    response_code = struct.unpack('b', response)[0]
    return response_code

