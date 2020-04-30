import config
import constants
import struct
import threading


def handle_command(message):
    # get user command from message
    command = message[0]
    debug_message(f'Command: {command}')

    # get the function of a specific command
    cmd_func = select_command(command)

    # if there is content other than the command
    if (len(message) > 1):
        # print(len(message))
        args = message[1:]
        debug_message(f'Content: {str(args, config.ENCODING)}')

    try:
        response = cmd_func(args)
    except:
        debug_message('Wrong command')
        response = create_error_response(constants.INCORRECT_COMMAND)

    return response


def select_command(command):
    func_ping  = ping
    func_echo  = echo
    func_login = login
    func_list  = list_cmd
    func_msg   = msg
    func_file  = file_cmd

    switcher = {
        constants.CMD_PING: func_ping,
        constants.CMD_ECHO: func_echo,
        constants.CMD_LIST: func_login,
        constants.CMD_LIST: func_list,
        constants.CMD_MSG : func_msg,
        constants.CMD_FILE: func_file,
    }

    # Get the function from switcher dictionary
    func = switcher.get(command, "nothing")
    # // Execute the function
    # Return command function
    return func



def ping(args=None):
    print('ping')
    response_code = constants.CMD_PING_RESPONSE
    response_message = struct.pack('b', response_code)
    return response_message


def echo(args=None):
    print('echo')


def login(args=None):
    print('login')


def list_cmd(args=None):
    print('list')


def msg(args=None):
    print('msg')


def file_cmd(args=None):
    print('file')



def create_error_response(error_code):
    response_message = struct.pack('b', error_code)
    return response_message



def debug_message(message):
    print('-'*35)
    print(f'|debugging| {threading.current_thread().native_id}: {message}')