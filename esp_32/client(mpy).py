import usocket as socket
import _thread
from display import Display
from machine import Pin

class Chat_Client():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.username = self.get_username()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Initializing the display
        self.display = Display()

        #Initializing Buttons
        self.left_button = Pin(4, Pin.IN, Pin.PULL_UP)
        self.right_button = Pin(15, Pin.IN, Pin.PULL_UP)
    
        #Button Interrupts
        self.left_button.irq(trigger=Pin.IRQ_FALLING, handler=self.left_button_pressed)
        self.right_button.irq(trigger=Pin.IRQ_FALLING, handler=self.right_button_pressed)



    def get_username(self):
        while True:
            username = input("Enter your username >> ")
            if not username.strip():
                print("Username cannot be empty !!!")
            else:
                return username



    def left_button_pressed(self, pin):
            self.display.prev_page()
            print('D')


    def right_button_pressed(self, pin):
            self.display.next_page()
            print('U')



    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))

            req = self.client_socket.recv(1024).decode('utf-8')
            if req == 'alias?':
                self.client_socket.send(self.username.encode('utf-8'))
            
            _thread.start_new_thread(self.receive_msg, ())

            self.send_msg()
        
        except Exception as e:
            print(f'Connection failed: {e}')

        finally:
            self.client_socket.close()



    
            
    def receive_msg(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    print(message)
                    self.display.add_message(message)
            except:
                print("Connection lost with server!")
                self.client_socket.close()
                break

    def send_msg(self):
        while True:
            message = input("")
            self.client_socket.send(f'{self.username} : {message}'.encode('utf-8'))

host = '192.168.73.107'  # Use the IP address of your server
port = 8080
client = Chat_Client(host, port)
client.connect()