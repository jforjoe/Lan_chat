import threading
import socket

def  get_default_gateway():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8',80))
        ip = sock.getsockname()[0]
        return ip
    except socket.error:
        return "127.0.0.1"
    finally:
        sock.close()
def handle_msg(prompt):
    
    '''If the entered message is empty string, user is asked to 
    enter it again untill it has some character'''
    
    message = input(prompt)
    while not message.strip():
        print('Please enter some characters!!')
        message = input(prompt)
    return message


def client_receive():

    '''once connected to the server the server sends a request for the username!!
    here we send the username to the server on request'''
    
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
        message = handle_msg(">>")
        client.send(f'{alias} : {message}'.encode("utf-8"))



alias = handle_msg("Enter your username >>> ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((get_default_gateway(), 55555))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

# Call the client_send function to allow the user to send messages
client_send()
