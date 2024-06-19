import socket
import threading

class Server:
    # All variable declarations are done here
    def __init__(self, host=None, port=None):
        self.host = host if host else socket.gethostbyname(socket.gethostname())
        self.port = port if port else 55555
        self.server = None
        self.server_address = None
        self.clients = []
        self.aliases = []

    # Starting the server and running
    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server_address = self.server.getsockname()
        print(f"Server is running on {self.server_address[0]}:{self.server_address[1]}")
        self.server.listen()
        self.receive()

    # Accepting new clients
    def receive(self):
        while True:
            print("Server is Listening ......")
            client, address = self.server.accept()
            print(f"Connection established {address[0]}:{address[1]}")

            client.send('alias?'.encode('utf-8'))
            alias = client.recv(1024).decode('utf-8')
            self.aliases.append(alias)
            self.clients.append(client)

            self.broadcast(f"{alias} has entered the chatroom ......".encode('utf-8'))
            print(f'alias: {alias}')
            print('------------------------------------------------------------')

            client.send("You are now connected!".encode('utf-8'))
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

    # Handling client communication
    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.action(message, client)
                self.broadcast(message, sender=client)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                alias = self.aliases[index]
                self.broadcast(f"{alias} has left the chat !".encode('utf-8'))
                self.aliases.remove(alias)
                break

    # Executing client requests
    def action(self, message, client):
        msg = message.decode('utf-8').split(' ')

        if msg[-1] == 'quit_':
            client.send("You have been disconnected !!!".encode('utf-8'))
            index = self.clients.index(client)
            self.clients.remove(client)
            client.close()
            alias = self.aliases[index]
            self.broadcast(f"{alias} has left the chat !".encode('utf-8'))
            self.aliases.remove(alias)
        else:
            pass

    # Broadcasting messages to all clients
    def broadcast(self, message, sender=None):
        for client in self.clients:
            if client != sender:
                try:
                    client.send(message)
                except:
                    print(f"{client.getpeername()} disconnected during message broadcast!!!")

if __name__ == "__main__":
    my_server = Server()
    my_server.start_server()
