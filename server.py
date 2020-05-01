import socket
import threading

host = 'localhost'
port = 8080

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind((host, port))
tcp.listen(10)

connections = []

print(f'Listening for connections on {host}:{port}...')


def socket_connection(socket, address):
    print(f'Receiving connection from {address}')
    while True:
        try:
            msg = socket.recv(1024)
        except ConnectionResetError:
            break

        if not msg:
            break

        for sockets in connections:
            if sockets != socket:
                sockets.send(msg)

        print(f'Sending: {msg[:3] + "....."}')
    print(f'Ending client connection {address}')

    connections.remove(socket)
    socket.close()


while True:
    socket, address = tcp.accept()
    thread = threading.Thread(target=socket_connection, args=(socket, address))
    thread.start()
    connections.append(socket)
