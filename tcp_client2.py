import socket
import time


socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 5555

socket_client.connect((host, port)) # встановлення з'єднання

message = input("Enter message from client:\n")
socket_client.send(message.encode('utf-8'))
# server_responce = socket_client.recv(1024)
# print(server_responce.decode('utf-8'))
server_message = socket_client.recv(1024)
print('Message from server: ' + server_message.decode('utf-8'))
socket_client.close()
time.sleep(40)