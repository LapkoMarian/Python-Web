import socket


socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 5555

socket_client.connect((host, port)) # встановлення з'єднання
while True:
    message = input("Enter message from client:\n")
    socket_client.send(message.encode('utf-8'))
    if message == 'stop':
        socket_client.close()
        break