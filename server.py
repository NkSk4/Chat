import socket
import threading

#   Definição da host
host = 'localhost'
port = 8080

#   Criação do server (socket) TCP/IP
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind((host, port))
tcp.listen(10)

#   Armazena os sockets conectados
connections = []

print(f"┏{'━'*27}┓\n┃{'Awaiting connections...':^27}┃\n┗{'━'*27}┛")

#   Recebe a conexão do client (socket)
def socket_connection(socket, address):
    print(f'Receiving connection from {address}')
    while True:
        #   Lê a mensagem enviada pelo client (socket)
        try:
            msg = socket.recv(1024).decode('utf-8')
        except ConnectionResetError:
            break

        #   Cancela o laço caso não haja mensagem
        if not msg:
            break

        #   Envia a mensagem a todos os sockets conectados no momento
        for sockets in connections:
            if sockets != socket:
                sockets.send(msg.encode('utf-8'))

        print(f'Sending: {msg}')
    print(f'Ending client connection {address}')

    #   Remove o socket da lista de sockets conectados
    connections.remove(socket)
    #   Fecha a conexão com o socket
    socket.close()


while True:
    #   Aceita a conexão com o client (socket)
    socket, address = tcp.accept()

    #   Cria um "thread" para receber conexões simultaneas
    thread = threading.Thread(target=socket_connection, args=(socket, address))
    thread.start()

    #   Adiciona o socket a lista de sockets conectados
    connections.append(socket)
