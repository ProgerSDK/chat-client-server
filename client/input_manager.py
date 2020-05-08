import constants


def get_command() -> dict:
    while True:
        user_input = get_user_input()
        command = handle_input(user_input)

        if (command['cmd_code'] == constants.CMD_HELP):
            help_cmd()
        elif (command['cmd_code'] != -1):
            return command



def get_user_input() -> str:
    while True:
        print('Please enter command:')
        user_input = input('-> ')
        if (len(user_input) != 0):
            return user_input



def handle_input(input: str) -> dict:
    cmd_list = input.split()
    cmd_code = get_cmd_code(cmd_list[0]) # [0] - command name

    args = None
    if (len(cmd_list) > 1):
        args = cmd_list[1:]

    cmd_dict = {
        'cmd_code': cmd_code,
        'args': args
    }
    return cmd_dict



def get_cmd_code(command: str) -> int:
    switcher = {
            "ping": constants.CMD_PING,
            "echo": constants.CMD_ECHO,
            "login": constants.CMD_LOGIN,
            "logout": constants.CMD_LOGOUT,
            "list": constants.CMD_LIST,
            "msg": constants.CMD_MSG,
            "file": constants.CMD_FILE,
            "help": constants.CMD_HELP,
            "exit": constants.CMD_EXIT,
            "recv_msg": constants.CMD_RECEIVE_MSG,
            "recv_file": constants.CMD_RECEIVE_FILE,
        }

    # get the cmd code from switcher dictionary
    cmd_code = switcher.get(command, -1)
    return cmd_code



def help_cmd() -> None:
    print()
    print(" ping  - test the ability of the source computer to reach a server;")
    print(" echo  - display line of text/string that are passed as an argument;")
    print(" login - establish a new session with the server;")
    print(" list  - list all users on the server;")
    print(" msg   - send a message to a specific user;")
    print(" file  - send a file to a specific user;")
    print(" exit  - close the client.")
    print()