import tkinter as tk
import socket
import threading
from Crypto.Cipher import DES
from mimesis import Person

host = 'localhost'
port = 8080


tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect((host, port))


class Crypt:
    def __init__(self, message, increment=2):
        self.message = message
        self.increment = increment
        self.key = b'ssssssss'
        self.des = DES.new(self.key, DES.MODE_ECB)

    def encrypt(self, ):
        text = self.message.encode('utf-8')
        print(type(text))
        while len(text) % 8 != 0:
            text += b' '
        encrypted_text = self.des.encrypt(text)
        return encrypted_text

    def decrypt(self):
        data = self.des.decrypt(self.message)
        return data


class Application(threading.Thread):
    def __init__(self, master=None):
        threading.Thread.__init__(self)
        person = Person('ja')
        self.nickname = person.username()
        master.title('Chat')
        canvas = tk.Canvas(root, height=700, width=400,)
        canvas.pack()

        self.create_interface()

    def create_interface(self):
        frame_output = tk.Frame(root, bg='#000000', bd=3)
        frame_output.place(relx=0.5, rely=0.4, relwidth=0.85,
                           relheight=0.7, anchor='center')

        self.label = tk.Listbox(frame_output, bg='#9c9c9c', fg="black")
        self.label.place(relwidth=1, relheight=1)
        frame_input = tk.Frame(root, bg='#d1d1d1', bd=3)
        frame_input.place(relx=0.5, rely=0.8, relwidth=0.75,
                          relheight=0.15, anchor='n')

        self.frame_input = frame_input

        self.get_nick()

        message = EntryWithPlaceholder(frame_input, "Message", color='black')
        message.place(relwidth=0.72, relheight=0.62, rely=0.35)
        message['font'] = ('Hack', 14)

        button_sand = tk.Button(frame_input, text='sand', bg='#3C5846', fg='#AEB2AE',
                                font=40, command=lambda: self.send_message(message.get(), self.nickname))
        button_sand.place(relx=0.74, rely=0.35, relwidth=0.25, relheight=0.62)
        root.bind('<Return>', func=lambda event: self.send_message(message.get(), self.nickname))
        scrollbar = tk.Scrollbar(frame_output, orient="vertical")
        scrollbar.config(command=self.label.yview)
        scrollbar.pack(side="right", fill="y")

    def create_username_field(self):
        username = EntryWithPlaceholder(self.frame_input, f'{self.nickname}')
        username.place(relwidth=0.72, relheight=0.2, rely=0.1, )
        username['font'] = ('System', 12)
        my_button = tk.Button(self.frame_input, text='Ok', command=lambda: self.change_nick(username, my_button))
        my_button.place(relx=0.74, rely=0.1, relwidth=0.25,
                        relheight=0.2, )

    def change_nick(self, username_wgt, button_wgt):
        self.nickname = username_wgt.get()
        username_wgt.destroy()
        button_wgt.destroy()
        self.get_nick()

    def get_nick(self):
        change_nickname_btn = tk.Button(self.frame_input, text='change ', bg='#3C5846', fg='#AEB2AE',
                                        font=40, command=lambda: self.create_username_field())
        change_nickname_btn['font'] = ('System', 10)
        change_nickname_btn.place(relx=0.74, rely=0.1, relwidth=0.25,
                                  relheight=0.2,)
        nickname_field = tk.Label(self.frame_input, text=f'nickname: {self.nickname}')
        nickname_field.place(relwidth=0.72, relheight=0.2, rely=0.1)

    def send_message(self, message, nick):
        if message.strip() in ['', 'Message']:
            return

        crypt = Crypt(f'{nick.strip()}: {message.strip()}')
        tcp.send(crypt.encrypt())
        self.label.insert(tk.END, f'{nick.strip()}: {message.strip()}')
        self.label.see(tk.END)

    def run(self):
        receive_messages(self.label)


def receive_messages(label):

    while True:
        data = tcp.recv(1024)
        if not data:
            break
        crypt = Crypt(data)
        label.insert(tk.END, crypt.decrypt())
        label.see(tk.END)


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="placeholder", color='green'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


root = tk.Tk()
Application(root).start()
root.mainloop()

