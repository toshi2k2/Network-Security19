import socket
import sys
from escape_room import EscapeRoom

# create socket
host = ""
port = 9999
s = socket.socket()
# binding socket
try:
    print("Binding the port " + str(port))

    s.bind((host, port))
    s.listen(1)

except socket.error as msg:
    print("Socket binding error: ", str(msg) + '\n' + "Retry....")

# establish connection with client (socket must be listening)

# send commands to client
while True:  # for keeping connection open
    conn, address = s.accept()
    print("Connection has been established ! " + "IP" + address[0] + " Port" + str(address[1]))

    room = EscapeRoom()
    room.start()
    while room.status() == 'locked':
        cmd = str(conn.recv(1024), "utf-8")
        print("command received:", cmd)
        if cmd == 'quit':
            conn.close()  # close connection
            s.close()  # close socket
            sys.exit()  # close cmd

        out = room.command(cmd)
        if room.status() == 'dead':
            out = out + '\n' + 'You died!'
        elif room.status() == 'escaped':
            out = out + '\n' + 'You escaped!'
        conn.send(str.encode(out))
    print("closing connection")
    conn.close()
    s.close()
    sys.exit()

