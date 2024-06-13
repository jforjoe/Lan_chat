import threading
import socket

alias = input("Enter your username >>> ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.96.107', 55555))

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'alias?':
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print("Error !!!")
            client.close()
            break

def client_send():
    while True:
        message = f'{alias}: {input(">> ")}'
        client.send(message.encode("utf-8"))

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

# Call the client_send function to allow the user to send messages
client_send()