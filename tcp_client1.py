import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5555)) # встановлення з'єднання

message = input("Enter message from client:\n")
client_socket.sendall(message.encode('utf-8'))
client_socket.close()
time.sleep(40)