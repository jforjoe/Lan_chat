import socket
import threading

host = "192.168.96.107"
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
aliases = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)

            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat !'.encode('utf-8'))
            aliases.remove(alias)
            break

def receive():
    while True:
        print("Server is running and listening ......")
        client, address = server.accept()
        print(f"Connection established {str(address)}")
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f"The alias of the client is {alias}".encode('utf-8'))
        broadcast(f'{alias} has entered the chatroom ......'.encode('utf-8'))
        client.send("You are now connected!".encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()