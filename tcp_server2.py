import socket
from datetime import datetime
import time
import sys


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost' #ip - адреса хоста
port = 5555 #номер порта

server_socket.bind((host, port)) # зв'язування ip адреси з номером порта
server_socket.listen(5)
print('The server is waiting for connection......')

# while True:
client_socket, addr = server_socket.accept()
    # print('Got a connection from {}'.format(addr))
    # clientsocket.send('What is your name?'.encode('utf-8'))
client_message = client_socket.recv(1024).decode('utf-8')
print('Client message: ' + client_message +
      "\nTime to receive the message: " + str(datetime.now()))
time.sleep(5)
size_resv_bytes = client_socket.send(client_message.encode('utf-8'))
if size_resv_bytes == len(client_message): # перевірка, чи всі дані були надіслані
    print("All data sent successfully")
else:
    print("!!!Error when sending data!!!")
server_socket.close()
time.sleep(40)