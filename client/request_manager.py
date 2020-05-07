import constants
import struct
import config
import json


def create_request(command: dict) -> bytes:
    cmd_code = command['cmd_code']
    args = command['args']

    cmd_func = select_command(cmd_code)
    request = cmd_func(args)
    return request



def select_command(cmd_code: int):
    switcher = {
        constants.CMD_PING: ping,
        constants.CMD_ECHO: echo,
        constants.CMD_LOGIN: login,
        constants.CMD_LOGOUT: logout,
        constants.CMD_LIST: list_cmd,
        constants.CMD_MSG : msg,
        constants.CMD_FILE: file_cmd,
        constants.CMD_RECEIVE_MSG: recv_msg,
        constants.CMD_RECEIVE_FILE: recv_file,
    }

    # Get the function from switcher dictionary
    func = switcher.get(cmd_code, "nothing")
    # Return command function
    return func


def ping(args=None):
    print('ping')
    request = get_request_code(constants.CMD_PING)
    return request


def echo(args=None):
    print('echo')
    request = get_request_code(constants.CMD_ECHO)
    
    if (args):
        response_message = bytes(f'{" ".join(args)}', config.ENCODING)
        request += response_message

    return request


def login(args=None):
    print('login')
    request = get_request_code(constants.CMD_LOGIN)

    try:
        login = args[0]
        password = args[1]
    except:
        return get_request_code(constants.WRONG_PARAMS)

    login_dict = {
        'login': login,
        'password': password
    }
    request_json = json.dumps(login_dict)
    request_args = bytearray(request_json, config.ENCODING)
    return request + request_args


def logout(args=None):
    print('logout')
    request = get_request_code(constants.CMD_LOGOUT)
    return request 


def list_cmd(args=None):
    print('list')
    request = get_request_code(constants.CMD_LIST)
    return request


def msg(args=None):
    print('msg')
    request = get_request_code(constants.CMD_MSG)
    
    try:
        receiver = args[0]
        message = ' '.join(args[1:])
    except:
        return get_request_code(constants.WRONG_PARAMS)

    msg_dict = {
        'receiver': receiver,
        'message': message
    }
    if (len(receiver) == 0) or (len(message) == 0):
        return get_request_code(constants.WRONG_PARAMS)

    request_json = json.dumps(msg_dict)
    request_args = bytearray(request_json, config.ENCODING)
    return request + request_args


def file_cmd(args=None):
    print('file')
    request = get_request_code(constants.CMD_FILE)
    
    try:
        receiver = args[0]
        filepath = args[1]
    except:
        return get_request_code(constants.WRONG_PARAMS)

    file_dict = {
        'receiver': receiver,
        'filename': 'filename',
        'file_content': 'file_content'
    }

    if (len(receiver) == 0) or (len(filepath) == 0):
        return get_request_code(constants.WRONG_PARAMS)

    request_json = json.dumps(file_dict)
    request_args = bytearray(request_json, config.ENCODING)
    return request + request_args



def get_request_code(code: int) -> bytes:
    request = struct.pack('b', code)
    return request



def recv_msg(args=None):
    print('receive msg')
    request = get_request_code(constants.CMD_RECEIVE_MSG)
    return request



def recv_file(args=None):
    print('receive file')
    request = get_request_code(constants.CMD_RECEIVE_FILE)
    return request