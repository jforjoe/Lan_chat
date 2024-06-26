import threading
import socket

class Chat_Client():
    def __init__(self, host, port):
        self.host=host
        self.port=port
        self.username=self.get_username()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))

        
            req = self.client_socket.recv(1024).decode('utf-8')
            if req == 'alias?':
                self.client_socket.send(self.username.encode('utf-8'))
            
            receive_thread = threading.Thread(target=self.receive_msg)
            receive_thread.start()

            self.send_msg()
        
        except:
            print("Failed to connect to server !!")
        finally:
            self.client_socket.close()

    def get_username(self):
        while True:
            username = input("Enter your username >> ")
            if not username.strip():
                print("Username cannot be empty !!!")
            else:
                return username
            
    def receive_msg(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    print(message)
            except:
                print("Connection lost with server!")
                self.client_socket.close()
                break


    def send_msg(self):
        while True:
            message=input("")
            self.client_socket.send(f'{self.username} : {message}'.encode('utf-8'))



host= socket.gethostbyname(socket.gethostname())
port= 8080
client = Chat_Client(host,port)
client.connect()




