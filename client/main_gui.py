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
root['bg'] = 'black'
root.option_add("*Font", "10")

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
top_login.geometry('310x160')
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

def select_user():
    try:
        clicked_item = lbox.curselection()[0]
        selected_username = lbox.get(clicked_item)
        receiver_entry.delete(0, END)
        receiver_entry.insert(0, selected_username)
    except IndexError as e:
        messagebox.showinfo('Select user error', 'Select user first!')
        return


frame_users = Frame(root, bg="green", width=130)
frame_users.pack(anchor=W, fill=Y, expand=False, side=LEFT) 

lbl_users = Label(frame_users, text = "Registered Users", bg='green')
lbl_users.pack(anchor=N)

btn_sel_user = Button(frame_users, text='Select user', command=select_user, bg='blue')
btn_sel_user.pack(anchor=S, pady=5)

lbox = Listbox(frame_users, width=12, bg='green', bd='0', font=font.Font(size=14))
lbox.pack(anchor=W, fill=Y, side=LEFT)

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

# messages_frame = Frame(content_frame, bg="white", height=290, width=360)
# messages_frame.pack(anchor=N, side=TOP, pady=5, padx=5)

messages_frame = ScrollableFrame(content_frame)
# messages_frame.config(bg='orange')
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
    response = client.handle(request)
    
    if is_error(response):
        messagebox.showerror('Sent Message Error', 'Please, try again!', parent=root)
        return
    
    msg_val = f'Me -> {receiver_val}:\n{message_val}'
    messageVar = Message(messages_frame.scrollable_frame, text = msg_val, width=350) 
    # messageVar.config(bg='lightgreen') 
    messageVar.pack(anchor=W, pady=2, padx=2)

    receiver_entry.delete(0, END)
    message_entry.delete(0, END)


def send_file():
    receiver_val = receiver_entry.get()
    if not filepath_val:
        messagebox.showerror('Error sent file!', 'Select a file!')
        return

    cmd_dict = {
        'cmd_code': constants.CMD_FILE,
        'args': [receiver_val, filepath_val]
    }
    request = create_request(cmd_dict)
    response = client.handle(request)
    
    if is_error(response):
        messagebox.showerror('Sent Message Error', 'Please, try again!', parent=root)
        return

    receiver_entry.delete(0, END)


send_frame = Frame(content_frame)
send_frame.pack(anchor=S, fill=X, expand=True, side=TOP)

Label(send_frame, text='To:').grid(row=0, pady=10, padx=10) 
Label(send_frame, text='Message:').grid(row=1, padx=10)
Label(send_frame, text='File:').grid(row=2, pady=10, padx=10) 
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
    print(filepath_val)


select_file_btn = Button(send_frame, text='Select a file', command=sel_file)
select_file_btn.grid(row=2, column=1)

send_file_btn = Button(send_frame, text='Send', command=lambda: send_file())
send_file_btn.grid(row=2, column=2, padx=10)

# END of SEND FRAME
##################################################################



root.resizable(False, False)
root.mainloop()










