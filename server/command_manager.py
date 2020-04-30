import config
import constants


def handle_command(message):
    # get user command from message
    command = message[0]
    print(f'Command: {command}')

    # get the function of a specific command
    cmd_func = select_command(command)

    # if there is content other than the command
    if (len(message) > 1):
        # print(len(message))
        args = message[1:]
        print(f'Content: {str(args, config.ENCODING)}')

    try:
        cmd_func(args)
    except:
        print('Wrong command')



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
