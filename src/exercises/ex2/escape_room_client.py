import socket
import sys
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('--port', required=False, help='port value', type=int, default=9999)
#
# opt = parser.parse_args()
port = 9999
host = '127.0.0.1'

if len(sys.argv) > 1:
    if ':' in sys.argv[1]:
        s_in = sys.argv[1].split(':')
        host = s_in[0]
        port = int(s_in[1])
        # print("port: ", host, port)
    else:
        port = int(sys.argv[1])

s = socket.socket()

# port = opt.port

s.connect((host, port))

while True:
    command = input(">> ")
    s.sendall(command.encode('utf-8'))
    data = s.recv(1024)

    decoded_data = data.decode('utf-8')
    if decoded_data[-5:] == 'died!' or decoded_data[-8:] == 'escaped!':
        print(decoded_data)
        sys.exit()
    print(decoded_data)
    if command == 'quit':
        sys.exit()