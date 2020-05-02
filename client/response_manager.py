import constants
import struct

def is_error(response: bytes) -> bool:
    if len(response) > 1:
        return False

    response = struct.unpack('b', response)[0]
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
    error = switcher.get(response, -1)
    if (error != -1):
        print(error)
        return True
    else:
        return False



def unpack_response(cmd_code: int, response: bytes) -> None:
    pass


def select_command(cmd_code: int):
    pass


def ping(args=None):
    pass


def echo(args=None):
    pass


def login(args=None):
    pass


def logout(args=None):
    pass   


def list_cmd(args=None):
    pass


def msg(args=None):
    pass


def file_cmd(args=None):
    pass