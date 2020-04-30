import sys
import socket
import constants
import struct
import time
import config


# Read args from user
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((config.HOST, config.PORT))
    ping = constants.CMD_RECEIVE_FILE

    ping_message = struct.pack('b', ping)
    message = bytearray('Hello!!!', config.ENCODING)
    size = struct.pack('i', len(message)+1)

    sock.send(size)
    time.sleep(1)

    sock.send(ping_message + message)
    time.sleep(1)
    
    # Receive data from the server and shut down
    received = str(sock.recv(1024), config.ENCODING)

    if (input()):
        pass

print("Sent:     {}".format(data))
print("Received: {}".format(received)) 
