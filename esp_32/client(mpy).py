import usocket as socket
import _thread
from machine import Pin, SoftI2C
import ssd1306

class Chat_Client():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.username = self.get_username()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



        #Initializing the display
        self.i2c = SoftI2C(sda=Pin(21),scl=Pin(22))
        self.display = ssd1306.SSD1306_I2C(128,32, self.i2c)
        self.display.show()
        self.line = 0


    def update_display(self,message):
        self.display.fill(0)
        self.display.text(message, 0, self.line, 1)
        self.display.show()
        self.line += 10         #  Move to the next line
        if self.line >= 32:     # If out of display lines, reset to top
            self.line = 0



    
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
                    self.update_display(message)
            except:
                print("Connection lost with server!")
                self.client_socket.close()
                break

    def send_msg(self):
        while True:
            message = input("")
            self.client_socket.send(f'{self.username} : {message}'.encode('utf-8'))

host = '192.168.182.107'  # Use the IP address of your server
port = 8080
client = Chat_Client(host, port)
client.connect()
