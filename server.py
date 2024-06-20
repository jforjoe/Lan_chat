import socket
import threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.aliases = []

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f'Server is running on {self.host}:{self.port}')

        while True:
            print("Server is listening ......")
            client, address = self.server.accept()
            print(f"Connection established from {address[0]}:{address[1]}")
            
            client.send('alias?'.encode('utf-8'))
            alias = client.recv(1024).decode('utf-8')
            self.aliases.append(alias)

            self.broadcast(f'{alias} has entered the chatroom ......'.encode('utf-8'))

            self.clients.append(client)
            print(f'Alias: {alias}')
            print('------------------------------------------------------------')
            
            client.send("You are now connected!".encode('utf-8'))
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024)
                if not message:
                    break  # If message is empty, client has disconnected

                self.action(message, client)
                self.broadcast(message, sender=client)
            except Exception as e:
                print(f"Exception occurred in handle_client: {e}")
                break

        self.disconnect_client(client)

    def action(self, message, client):
        msg = message.decode('utf-8').split(' ')
        if msg[-1] == 'quit_':
            client.send('You have been disconnected !!!'.encode('utf-8'))
            self.disconnect_client(client)
            

    def disconnect_client(self, client):
        try:
            index = self.clients.index(client)
            alias = self.aliases[index]
            self.clients.remove(client)
            self.aliases.remove(alias)
            client.close()
            self.broadcast(f'{alias} has left the chat !'.encode('utf-8'))
            

            # Notify client via UDP
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_address = client.getpeername()  # Get client's address
            disconnect_message = 'You have been disconnected from the chat server.'.encode('utf-8')
            udp_socket.sendto(disconnect_message, client_address)
            udp_socket.close()

        except ValueError:
            pass  # Handle case where client not found in list

    def broadcast(self, message, sender=None):
        for cl in self.clients:
            if cl != sender:
                try:
                    cl.send(message)
                except Exception as e:
                    print(f"Error broadcasting message to {cl.getpeername()}: {e}")

if __name__ == "__main__":
    host = socket.gethostbyname(socket.gethostname())
    port = 55555  # Adjust this port as needed

    server = ChatServer(host, port)
    server.start()
