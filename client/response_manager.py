import constants
import struct
import config
import json


def is_error(response: bytes) -> bool:
    if len(response) > 1:
        return False

    response_code = unpack_response_code(response)
    switcher = {
            constants.SERVER_ERROR: 'Server error!',
            # constants.INCORRECT_CONTENT_SIZE: 'Incorrect content size!',
            constants.SERIALIZATION_ERROR: 'Serialization error!',
            constants.INCORRECT_COMMAND: 'Incorrect command',
            constants.WRONG_PARAMS: 'Wrong params!',
            constants.LOGIN_WRONG_PASSWORD: 'Login wrong password!',
            constants.LOGIN_FIRST: 'Login first!',
            constants.FAILED_SENDING: 'Failed sending!',
        }

    # get the error from switcher dictionary
    error = switcher.get(response_code, -1)
    if (error != -1):
        print(error)
        return True
    else:
        return False



def unpack_response(cmd_code: int, response: bytes) -> None:
    if is_error(response):
        print()
        return
    
    cmd_func = select_command(cmd_code)
    try:
        cmd_func(response)
    except:
        print('Something went wrong...\n')



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



def ping(response):
    response_code = unpack_response_code(response)
    if (response_code == 2):
        print('Ping success!\n')


def echo(response):
    response_content = response.decode(config.ENCODING)
    print(response_content + '\n')


def login(response):
    response_code = unpack_response_code(response)
    if (response_code == constants.CMD_LOGIN_OK_NEW):
        print('Registration OK.\n')
    elif(response_code == constants.CMD_LOGIN_OK):
        print('Login OK.\n')


def logout(response):
    response_code = unpack_response_code(response)
    if (response_code == constants.CMD_LOGOUT_OK):
        print('Logout OK.\n')


def list_cmd(response):
    response_content = response.decode(config.ENCODING)
    users = json.loads(response_content)
    user_list = users['user_list']
    print(f'User list: {user_list}\n')    


def msg(response):
    response_code = unpack_response_code(response)
    if (response_code == constants.CMD_MSG_SENT):
        print('Message sent.\n')


def file_cmd(response):
    response_code = unpack_response_code(response)
    if (response_code == constants.CMD_FILE_SENT):
        print('File sent.\n')



def unpack_response_code(response: bytes) -> int:
    response_code = struct.unpack('b', response)[0]
    return response_code