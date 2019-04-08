from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import time

IP="127.0.0.1"
PORT=80

window = tkinter.Tk()
window.title("Chat")

messageFrame = tkinter.Frame(window)
entryFieldString = tkinter.StringVar()  # For the messages to be sent.
entryFieldString.set("Type here")
scrollbar = tkinter.Scrollbar(messageFrame)  # To navigate through past messages.

# Following will contain the messages.
messageList = tkinter.Listbox(messageFrame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
messageList.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
#messageList.pack()
messageFrame.pack()

entryField = tkinter.Entry(window, textvariable=entryFieldString)
entryField.pack()

# Sockets
BUFFERSIZE = 1024

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((IP, PORT))

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.connect((IP, PORT))

def send():
    message = entryFieldString.get()
    messageList.insert(tkinter.END, "Me:  " + message)
    client_socket.sendto(bytes(message,"UTF-8"),(IP,PORT))
    entryFieldString.set("")

def receive():
    print("recieve started")
    while 1:
        #time.sleep(1)
        data , (client_ip , client_port)= serverSocket.recvfrom(BUFFERSIZE)
        print("RECIEVED:", data.decode("utf-8"))


receive_thread = Thread(target=receive)
receive_thread.start()

sendButton = tkinter.Button(window, text="Send", command=send)
sendButton.pack()

tkinter.mainloop()  # Starts GUI execution.