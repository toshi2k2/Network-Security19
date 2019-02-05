import socket
import os
import subprocess

s = socket.socket()
host = '10.194.111.27'
port = 9999

s.connect((host, port))

while True:
    command = input(">> ")
    s.sendall(command.encode('utf-8'))
    data = s.recv(1024)
    print(data.decode('utf-8'))
    if command == 'quit':
        break