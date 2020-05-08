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
from tkinter import filedialog, ttk, font
from additional_tkinter import ScrollableFrame
import os


def create_receiver(response, request):
    response_code = struct.unpack('b', response)[0]
    
    if ((response_code == constants.CMD_LOGIN_OK_NEW) 
        or (response_code == constants.CMD_LOGIN_OK)):
        
        # create new thread
        receiver_thread = threading.Thread(target=auto_receiver.create_receiver, args=(request, messages_frame, lbox))

        # exit the receiver thread when the main thread terminates
        receiver_thread.daemon = True
        receiver_thread.start()


root = Tk()
root.title('Chat client')
root.geometry('560x440')
root.option_add("*Font", "Helvetica 11")
root.config(background="#2D2D44")
root.option_add("*selectBackground", "white")
root.option_add("*selectForeground", "#1E1E2C")
root.option_add("*Button.Background", "#1E1E2C")
root.option_add("*Button.Foreground", "white")


client = None
def connect_to_server(host, port):
    global client
    try:
        client = Client()
        client.connect(host, port)
    except ConnectionRefusedError as e:
        messagebox.showerror('Connection Error', 'Wrong params or server is shutdown!')
        exit()


##################################################################
# LOGIN

def enter_ip():
    host = host_entry.get()
    port_val = port_entry.get()

    if len(host) == 0 or len(port_val) == 0:
        messagebox.showinfo('Empty fields', 'Enter parameters!')
        return

    try:
        port = int(port_val)
    except:
        messagebox.showinfo('Wrong port', 'The port must be a number!')
        return

    connect_to_server(host, port)
    config.HOST = host
    config.PORT = port
    top_ip.destroy()
    create_top_login()


top_ip = Toplevel(bg='#2D2D44')
top_ip.title('Enter IP/PORT')
top_ip.attributes('-topmost', 'true')
top_ip.geometry('250x160')
top_ip.resizable(False, False)
top_ip.focus_force()

Label(top_ip, text='Host:', bg='#2D2D44', fg='white').grid(row=0, pady=20, padx=10) 
Label(top_ip, text='Port:', bg='#2D2D44', fg='white').grid(row=1,padx=10) 
host_entry = Entry(top_ip) 
port_entry = Entry(top_ip) 
host_entry.grid(row=0, column=1, columnspan=2) 
port_entry.grid(row=1, column=1, columnspan=2) 

btn_enter_ip = Button(top_ip, text='Connect', command=enter_ip) 
btn_enter_ip.grid(row=3, column=1, pady=20)


def create_top_login():

    def login_cmd():
        login_val = login_entry.get()
        pass_val = pass_entry.get()

        cmd_dict = {
            'cmd_code': constants.CMD_LOGIN,
            'args': [login_val, pass_val]
        }
        request = create_request(cmd_dict)
        response = client.handle(request)
        
        if is_error(response, top_login):
            return
        
        create_receiver(response, request)
        top_login.destroy()


    top_login = Toplevel(bg='#2D2D44')
    top_login.title('Login/Register')
    top_login.attributes('-topmost', 'true')
    top_login.geometry('310x160')
    top_login.resizable(False, False)
    top_login.focus_force()

    Label(top_login, text='Login:', bg='#2D2D44', fg='white').grid(row=0, pady=20, padx=10) 
    Label(top_login, text='Password:', bg='#2D2D44', fg='white').grid(row=1,padx=10) 
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

def select_user():
    try:
        clicked_item = lbox.curselection()[0]
        selected_username = lbox.get(clicked_item)
        receiver_entry.delete(0, END)
        receiver_entry.insert(0, selected_username)
    except IndexError as e:
        messagebox.showinfo('Select user error', 'Select user first!')
        return


frame_users = Frame(root, bg="#2D2D44", width=130)
frame_users.pack(anchor=W, fill=Y, expand=False, side=LEFT) 

lbl_users = Label(frame_users, text = "Users List", bg='#2D2D44', fg="white")
lbl_users.pack(anchor=N)

btn_sel_user = Button(frame_users, text='Select user', command=select_user)
btn_sel_user.pack(anchor=S, pady=5)

lbox = Listbox(frame_users, width=12, bg='#2D2D44', bd='0', font=font.Font(size=14), fg='white', highlightbackground='#1E1E2C')
lbox.pack(anchor=W, fill=Y, side=LEFT)

# END of USERS FRAME
##################################################################


##################################################################
# CONTENT FRAME

content_frame = Frame(root, bg="#2D2D44")
content_frame.pack(anchor=N, fill=BOTH, expand=True, side=LEFT )

# END of CONTENT FRAME
##################################################################



##################################################################
# MESSAGES FRAME

messages_frame = ScrollableFrame(content_frame)
messages_frame.pack(anchor=N, side=TOP, pady=5)

# END of MESSAGES FRAME
##################################################################



##################################################################
# SEND FRAME

def send_msg():
    receiver_val = receiver_entry.get()
    message_val = message_entry.get()

    cmd_dict = {
        'cmd_code': constants.CMD_MSG,
        'args': [receiver_val, message_val]
    }
    request = create_request(cmd_dict)
    if is_error(request):
        return

    response = client.handle(request)
    if is_error(response):
        return
    
    msg_val = f'Me -> {receiver_val}:\n{message_val}'
    messageVar = Message(messages_frame.scrollable_frame, text = msg_val, width=350) 
    messageVar.pack(anchor=W, pady=2, padx=2)

    receiver_entry.delete(0, END)
    message_entry.delete(0, END)


def send_file():
    global filepath_val
    receiver_val = receiver_entry.get()
    if not filepath_val:
        messagebox.showinfo('File not found!', 'Select a file!')
        return

    cmd_dict = {
        'cmd_code': constants.CMD_FILE,
        'args': [receiver_val, filepath_val]
    }
    request = create_request(cmd_dict)
    if is_error(request):
        return

    response = client.handle(request)
    
    if is_error(response):
        return

    filename = None
    with open(filepath_val) as f:
        filename = os.path.basename(f.name)

    msg_val = f'Me -> {receiver_val}:\nSent a "{filename}" file.'
    messageVar = Message(messages_frame.scrollable_frame, text = msg_val, width=350) 
    messageVar.pack(anchor=W, pady=2, padx=2)

    receiver_entry.delete(0, END)


send_frame = Frame(content_frame, bg='#2D2D44')
send_frame.pack(anchor=S, fill=X, expand=True, side=TOP)

Label(send_frame, text='To:', bg='#2D2D44', fg='white').grid(row=0, pady=10, padx=10) 
Label(send_frame, text='Message:', bg='#2D2D44', fg='white').grid(row=1, padx=10)
Label(send_frame, text='File:', bg='#2D2D44', fg='white').grid(row=2, pady=10, padx=10) 
receiver_entry = Entry(send_frame) 
message_entry = Entry(send_frame) 
file_entry = Entry(send_frame) 

receiver_entry.grid(row=0, column=1) 
message_entry.grid(row=1, column=1)

send_msg_btn = Button(send_frame, text='Send', command=send_msg)
send_msg_btn.grid(row=1, column=2, padx=10)

filepath_val = None
def sel_file():
    global filepath_val
    send_frame.filename = filedialog.askopenfile(title='Select a file') 
    filepath_val = send_frame.filename.name


select_file_btn = Button(send_frame, text='Select a file', command=sel_file)
select_file_btn.grid(row=2, column=1)

send_file_btn = Button(send_frame, text='Send', command=send_file)
send_file_btn.grid(row=2, column=2, padx=10)

# END of SEND FRAME
##################################################################


root.resizable(False, False)
root.mainloop()
