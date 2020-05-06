from tkinter import *
from request_manager import create_request
from response_manager import is_error, unpack_response
from client import Client
import constants
import config
from tkinter import messagebox


root = Tk()
root.title('Chat client')


try:
    client = Client()
    client.connect(config.HOST, config.PORT)
except ConnectionRefusedError as e:
    messagebox.showerror('Connection Refused', 'Run server first!')
    exit()



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
    
    top_login.destroy()




##################################################################
# LOGIN

top_login = Toplevel()
top_login.title('Login/Register')
top_login.attributes('-topmost', 'true')
top_login.geometry('260x160')

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


root.mainloop()










# def create_receiver(response, request):
#     response_code = struct.unpack('b', response)[0]
    
#     if ((response_code == constants.CMD_LOGIN_OK_NEW) 
#         or (response_code == constants.CMD_LOGIN_OK)):
        
#         # create new thread
#         receiver_thread = threading.Thread(target=auto_receiver.create_receiver, args=(request,))

#         # exit the receiver thread when the main thread terminates
#         receiver_thread.daemon = True
#         receiver_thread.start()