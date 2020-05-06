from tkinter import *
from request_manager import create_request
from response_manager import is_error, unpack_response
from client import Client
import constants
import config
from tkinter import messagebox
import struct
import threading
import auto_receiver


def create_receiver(response, request):
    response_code = struct.unpack('b', response)[0]
    
    if ((response_code == constants.CMD_LOGIN_OK_NEW) 
        or (response_code == constants.CMD_LOGIN_OK)):
        
        # create new thread
        receiver_thread = threading.Thread(target=auto_receiver.create_receiver, args=(request,))

        # exit the receiver thread when the main thread terminates
        receiver_thread.daemon = True
        receiver_thread.start()


root = Tk()
root.title('Chat client')
root.geometry('480x400')


try:
    client = Client()
    client.connect(config.HOST, config.PORT)
except ConnectionRefusedError as e:
    messagebox.showerror('Connection Refused', 'Run server first!')
    exit()


##################################################################
# LOGIN

def login_cmd():
    login_val = login_entry.get()
    pass_val = pass_entry.get()

    cmd_dict = {
        'cmd_code': constants.CMD_LOGIN,
        'args': [login_val, pass_val]
    }
    request = create_request(cmd_dict)
    response = client.handle(request)
    
    if is_error(response):
        messagebox.showerror('Login Error', 'Please, try again!', parent=top_login)
        return
    
    create_receiver(response, request)
    top_login.destroy()


top_login = Toplevel()
top_login.title('Login/Register')
top_login.attributes('-topmost', 'true')
top_login.geometry('260x160')
top_login.resizable(False, False)
top_login.focus_force()

Label(top_login, text='Login:').grid(row=0, pady=20, padx=5) 
Label(top_login, text='Password:').grid(row=1,padx=5) 
login_entry = Entry(top_login) 
pass_entry = Entry(top_login, show="*") 
login_entry.grid(row=0, column=1, columnspan=2) 
pass_entry.grid(row=1, column=1, columnspan=2) 

button = Button(top_login, text='Login', command=login_cmd) 
button.grid(row=3, column=1, pady=20) 

# END of LOGIN
##################################################################


##################################################################
# USERS FRAME

frame_users = Frame(root, bg="green", width=130)
frame_users.pack(anchor=W, fill=Y, expand=False, side=LEFT)  

# END of USERS FRAME
##################################################################


##################################################################
# CONTENT FRAME

content_frame = Frame(root, bg="orange")
content_frame.pack(anchor=N, fill=BOTH, expand=True, side=LEFT )

# END of CONTENT FRAME
##################################################################


##################################################################
# MESSAGES FRAME

messages_frame = Frame(content_frame, bg="orange", height=300)
messages_frame.pack(anchor=N, fill=X, expand=True , side=TOP)

# END of MESSAGES FRAME
##################################################################


##################################################################
# SEND FRAME

content_frame = Frame(content_frame, bg="white", height=180)
content_frame.pack(anchor=S, fill=X, expand=True, side=TOP)

# END of SEND FRAME
##################################################################



root.resizable(False, False)
root.mainloop()










