from tkinter import *
import socket
import _thread

IP = "127.0.0.1"
PORT = 50007
BUFSIZE = 1024

receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiverSocket.bind((IP, PORT))
receiverSocket.setblocking(True)

window = Tk()
# window.state("zoomed")
window.geometry("200x300")
window.title("Old Chatterhand")

messageFrame = Frame(window)

scrollbar = Scrollbar(messageFrame)
scrollbar.pack(side=RIGHT, fill=Y)


listBox = Listbox(messageFrame, height=15, width=50, yscrollcommand=scrollbar.set)
listBox.pack(side=LEFT, fill=BOTH)
scrollbar.config(command=listBox.yview)

messageFrame.pack()

def send(message):

    textBox.delete(0, END)
    listBox.insert(END, "Me: {}".format(message))
    receiverSocket.sendto(message.encode('utf-8'), (IP, PORT))


def enterPress(event=""):
    send(textBox.get())


window.bind('<Return>', enterPress)

textBox = Entry(window)
textBox.pack(side=BOTTOM)

btn = Button(window, text="Send", command=enterPress)
btn.pack()


def listen():
    while 1:
        data, (client_ip, client_port) = receiverSocket.recvfrom(BUFSIZE)
        stringdata = data.decode('utf-8')
        #listBox.insert(END, "{}: {}".format(client_ip, stringdata))
        print(str("{}: {}".format(client_ip, stringdata)))

    receiverSocket.close()


_thread.start_new(listen, ())
window.mainloop()
