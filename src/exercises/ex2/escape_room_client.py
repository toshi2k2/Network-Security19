import socket
import os
import subprocess

s = socket.socket()
host = '192.168.1.153'
port = 9999

s.connect((host, port))

while True:
    command = input()
    s.sendall(command)
    data = s.recv(1024)
    print(data)
    if command == 'quit':
        break