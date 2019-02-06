import socket
import sys

s = socket.socket()
host = '127.0.0.1'
port = 9999

s.connect((host, port))

while True:
    command = input(">> ")
    s.sendall(command.encode('utf-8'))
    data = s.recv(1024)

    decoded_data = data.decode('utf-8')
    if decoded_data[-5:] == 'died!' or decoded_data[-8:] == 'escaped':
        print(decoded_data)
        sys.exit()
    print(decoded_data)
    if command == 'quit':
        break