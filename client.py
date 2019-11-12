import tkinter as tk
import socket
import threading

# socket===inicio=======================

#   Definição da host
host = 'localhost'
port = 8080

#   Criação do socket TCP/IP
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect((host, port))


# criptografia e envio da mensagem==============


class Crypt:
    def __init__(self, message, increment=2):
        self.message = message
        self.increment = increment
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ç',
                         'á', 'à', 'ã', 'â', 'ä', 'é', 'è', 'ê', 'ë', 'í', 'ì', 'î', 'ï', 'ó', 'ò', 'õ', 'ô', 'ö', 'ú', 'ù', 'û', 'ü',
                         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Ç',
                         'Á', 'À', 'Ã', 'Â', 'Ä', 'É', 'È', 'Ê', 'Ë', 'Í', 'Ì', 'Î', 'Ï', 'Ó', 'Ò', 'Õ', 'Ô', 'Ö', 'Ú', 'Ù', 'Û', 'Ü',
                         '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#', '$', '%', '¨', '&', '*', '(', ')',
                         "'", '"', '¹', '²', '³', '£', '¢', '¬', '-', '=', '_', '+', '§',
                         '\\', '|', '´', '[', '~', ']', ',', '.', ';', '/', '`', '{', '^', '}', '<', '>', ':', '?', 'ª', 'º', '°', ' ']

    def encrypt(self):
        result = ''
        for msg in self.message:
            add = self.alphabet.index(msg) - self.increment
            result += self.alphabet[len(self.alphabet) +
                                    add if add < 0 else add]
        return result

    def decrypt(self):
        result = ''
        for msg in self.message:
            add = self.alphabet.index(msg) + self.increment
            result += self.alphabet[add - len(self.alphabet)
                                    if add >= len(self.alphabet) else add]
        return result


# seção de interface gráfica===================
class Application(threading.Thread):
    def __init__(self, master=None):
        threading.Thread.__init__(self)
        master.title('Krypto')
        canvas = tk.Canvas(root, height=500, width=500)
        canvas.pack()
        self.create_interface()
        root.iconbitmap('iconchat.ico')

    def create_interface(self):
        # seção de saída-------------------

        frame_output = tk.Frame(root, bg='#90d693', bd=3)
        frame_output.place(relx=0.5, rely=0.4, relwidth=0.85,
                           relheight=0.7, anchor='center')

        self.label = tk.Listbox(frame_output, bg='#9c9c9c', fg="black")
        self.label.place(relwidth=1, relheight=1)

        # seção de entrada-----------------

        frame_input = tk.Frame(root, bg='#d1d1d1', bd=3)
        frame_input.place(relx=0.5, rely=0.8, relwidth=0.75,
                          relheight=0.15, anchor='n')

        username = EntryWithPlaceholder(frame_input, "Digite seu nome", color='grey')
        username.place(relwidth=0.45, relheight=0.3, rely=0.02)
        username['font'] = ('Arial', 12)

        message = EntryWithPlaceholder(frame_input, "Digite uma mensagem", color='grey')
        message.place(relwidth=0.72, relheight=0.62, rely=0.35)
        message['font'] = ('Arial', 14)

        button = tk.Button(frame_input, text='Enviar', bg='#696969', fg='black',
                           font=40, command=lambda: self.send_message(message.get(), username.get()))
        button.place(relx=0.74, rely=0.35, relwidth=0.25, relheight=0.62)

        scrollbarH = tk.Scrollbar(frame_output, orient="horizontal")
        scrollbarH.config(command=self.label.xview)
        scrollbarH.pack(side="bottom", fill="x")

        scrollbarV = tk.Scrollbar(frame_output, orient="vertical")
        scrollbarV.config(command=self.label.yview)
        scrollbarV.pack(side="right", fill="y")


    def send_message(self, message, nick):
        if message.strip() in ['', 'Digite uma mensagem'] or nick.strip() in ['', 'Digite seu nome']:
            return

        #   Envia a mensagem para o servidor (socket)
        crypt = Crypt(f'{nick.strip()}: {message.strip()}')
        tcp.send(crypt.encrypt().encode('utf-8'))        
        self.label.insert(tk.END, f'{nick.strip()}: {message.strip()}')
        self.label.see(tk.END)
    def run(self):
        receive_messages(self.label)


def receive_messages(label):
    #   Lê e printa a mensagem enviada pelo server (socket)
    while True:
        data = tcp.recv(1024).decode('utf-8')
        if not data:
            break
        crypt = Crypt(data)      
        label.insert(tk.END, crypt.decrypt())
        label.see(tk.END)


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="placeholder", color='black'):
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
