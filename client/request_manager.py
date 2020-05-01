import constants
import struct
import config


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
    return request


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
    return request


def file_cmd(args=None):
    print('file')
    request = get_request_code(constants.CMD_FILE)
    return request


def get_request_code(code: int) -> bytes:
    request = struct.pack('b', code)
    return request