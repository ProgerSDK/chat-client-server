import config
import constants
import struct
import threading
import json
import users_data


def handle_command(message):
    # get user command from message
    command = message[0]
    debug_message(f'Command: {command}')

    # get the function of a specific command
    cmd_func = select_command(command)

    args = None
    # if there is args of the command
    if (len(message) > 1):
        args = message[1:].decode(config.ENCODING)
        debug_message(f'Content: {args}')

    try:
        response = cmd_func(args)
    except:
        debug_message('Wrong command')
        response = create_response(constants.INCORRECT_COMMAND)

    debug_message(f'authorized users: {users_data.AUTHORIZED_USERS}')

    return response


def select_command(command):
    func_ping  = ping
    func_echo  = echo
    func_login = login
    func_logout = logout
    func_list  = list_cmd
    func_msg   = msg
    func_file  = file_cmd

    switcher = {
        constants.CMD_PING: func_ping,
        constants.CMD_ECHO: func_echo,
        constants.CMD_LOGIN: func_login,
        constants.CMD_LOGOUT: func_logout,
        constants.CMD_LIST: func_list,
        constants.CMD_MSG : func_msg,
        constants.CMD_FILE: func_file,
        constants.CMD_RECEIVE_MSG: recv_msg,
        constants.CMD_RECEIVE_FILE: recv_file,
    }

    # Get the function from switcher dictionary
    func = switcher.get(command, "nothing")
    # Return command function
    return func



def ping(args=None):
    debug_message('ping')
    response_code = constants.CMD_PING_RESPONSE
    response = struct.pack('b', response_code)
    return response


def echo(args=None):
    debug_message('echo')
    if (args):
        response = bytearray(f'ECHO: {args}', config.ENCODING)
    else:
        response = bytearray(f'ECHO:', config.ENCODING)
    
    return response


def login(args=None):
    debug_message('login')
    
    if not (args):
        return create_response(constants.WRONG_PARAMS)
        
    userdata = json.loads(args)
    if not (('login' in userdata) and ('password' in userdata)):
        return create_response(constants.WRONG_PARAMS)

    registered = False
    auth_success = False

    # check if user is registered
    for user in users_data.REGISTERED_USERS:
        if (userdata['login'] == user['login']):
            registered = True
            if (userdata['password'] == user['password']):
                auth_success = True
            break

    # add new user if not registered
    if not registered:
        users_data.REGISTERED_USERS.append(userdata)
        userdata['id'] = threading.current_thread().native_id
        users_data.AUTHORIZED_USERS.append(userdata)
        return create_response(constants.CMD_LOGIN_OK_NEW)
    
    # if wrong password
    if not auth_success:
        return create_response(constants.LOGIN_WRONG_PASSWORD)

    # check if user is authorized
    for user in users_data.AUTHORIZED_USERS:
        if (userdata['login'] == user['login']):
            return create_response(constants.CMD_LOGIN_OK)
    
    # if not authorized:
    # add new user if not registered
    userdata['id'] = threading.current_thread().native_id
    users_data.AUTHORIZED_USERS.append(userdata)
    return create_response(constants.CMD_LOGIN_OK)



def logout(args=None):
    debug_message('logout')

    # check if user is authorized
    for user in users_data.AUTHORIZED_USERS:
        if (threading.current_thread().native_id == user['id']):
            users_data.AUTHORIZED_USERS.remove(user)
            return create_response(constants.CMD_LOGOUT_OK)
    
    # if not authorized:
    return create_response(constants.LOGIN_FIRST)    



def list_cmd(args=None):
    debug_message('list')

    authorized = False

    # check if user is authorized
    for user in users_data.AUTHORIZED_USERS:
        if (threading.current_thread().native_id == user['id']):
            authorized = True

    if authorized:
        user_list = list(map(lambda x: x['login'], users_data.AUTHORIZED_USERS))
        response_dict = {'user_list': user_list}
        response = json.dumps(response_dict)
        return bytearray(response, config.ENCODING)

    return create_response(constants.LOGIN_FIRST)



def msg(args=None):
    debug_message('msg')

    if not (args):
        return create_response(constants.WRONG_PARAMS)

    try:
        msg_data = json.loads(args)
    except:
        return create_response(constants.SERIALIZATION_ERROR)
 
    if not (('receiver' in msg_data) and ('message' in msg_data)):
        return create_response(constants.WRONG_PARAMS)

    authorized = False
    username = None
    # check if user is authorized
    for user in users_data.AUTHORIZED_USERS:
        if (threading.current_thread().native_id == user['id']):
            username = user['login']
            authorized = True

    if not authorized:
        return create_response(constants.LOGIN_FIRST)
   
    # if authorized
    msg_data['sender'] = username
    users_data.USERS_MESSAGES.append(msg_data)
    debug_message(f'messages: {users_data.USERS_MESSAGES}')
    return create_response(constants.CMD_MSG_SENT)



def file_cmd(args=None):
    debug_message('file')

    if not (args):
        return create_response(constants.WRONG_PARAMS)

    try:
        file_data = json.loads(args)
    except:
        return create_response(constants.SERIALIZATION_ERROR)
 
    if not (('receiver' in file_data) and ('filename' in file_data)
            and ('file_content' in file_data)):
        return create_response(constants.WRONG_PARAMS)

    authorized = False
    username = None
    # check if user is authorized
    for user in users_data.AUTHORIZED_USERS:
        if (threading.current_thread().native_id == user['id']):
            username = user['login']
            authorized = True

    if not authorized:
        return create_response(constants.LOGIN_FIRST)
   
    # if authorized
    file_data['sender'] = username
    users_data.USERS_FILES.append(file_data)
    debug_message(f'files: {users_data.USERS_FILES}')
    return create_response(constants.CMD_FILE_SENT)



def create_response(code):
    response = struct.pack('b', code)
    return response



def debug_message(message):
    print('-'*35)
    print(f'|debugging| {threading.current_thread().native_id}: {message}')



def recv_msg(args=None):
    authorized = False
    username = None
    # check if user is authorized
    for user in users_data.AUTHORIZED_USERS:
        if (threading.current_thread().native_id == user['id']):
            username = user['login']
            authorized = True
    
    if not authorized:
        return create_response(constants.LOGIN_FIRST)

    # if authorized
    # check if there is new messages
    msg = None
    new_msg = False
    for message in users_data.USERS_MESSAGES:
        if (username == message['receiver']):
            msg = dict(message)
            users_data.USERS_MESSAGES.remove(message)
            new_msg = True
            break

    if (new_msg):
        response_json = json.dumps(msg)
        response = bytearray(response_json, config.ENCODING)
        return response
    else:
        return create_response(constants.CMD_RECEIVE_MSG_EMPTY) 



def recv_file(args=None):
    authorized = False
    username = None
    # check if user is authorized
    for user in users_data.AUTHORIZED_USERS:
        if (threading.current_thread().native_id == user['id']):
            username = user['login']
            authorized = True
    
    if not authorized:
        return create_response(constants.LOGIN_FIRST)

    debug_message('here')

    # if authorized
    # check if there is new files
    file_msg = None
    new_file = False
    for file_dict in users_data.USERS_FILES:
        if (username == file_dict['receiver']):
            file_msg = dict(file_dict)
            users_data.USERS_FILES.remove(file_dict)
            new_file = True
            break

    debug_message('here1')

    if (new_file):
        response_json = json.dumps(file_msg)
        response = bytearray(response_json, config.ENCODING)
        return response
    else:
        return create_response(constants.CMD_RECEIVE_FILE_EMPTY) 