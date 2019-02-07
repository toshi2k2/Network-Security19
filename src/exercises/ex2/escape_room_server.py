import socket
import sys
from escape_room import EscapeRoom
import _thread

if len(sys.argv) > 1:
    port = int(sys.argv[1])
    # print("port: ", port)
else:
    port = 9999

host = ""

s = socket.socket()

# binding socket

try:
    # print("Binding the port " + str(port))

    s.bind((host, port))
    s.listen(1)

except socket.error as msg:
    # print("Socket binding error: ", str(msg) + '\n' + "Retry....")
    pass

# establish connection with client (socket must be listening)


def new_client(conn, addr):
    while True:
        room = EscapeRoom()
        room.start()
        while room.status() == 'locked':
            cmd = str(conn.recv(1024), "utf-8")
            # print("command received:", cmd, " from: ", addr)

            out = room.command(cmd)
            if room.status() == 'dead':
                out = out + '\n' + 'You died!'
            elif room.status() == 'escaped':
                out = out + '\n' + 'You escaped!'
            conn.send(str.encode(out))

            if cmd == 'quit':
                # print("closing connection from: ", addr)
                conn.close()  # close connection
                # s.close()  # close socket
                sys.exit()  # close cmd
        conn.close()
        sys.exit()


# send commands to client
while True:  # for keeping connection open
    conn, address = s.accept()
    # print("Connection has been established ! " + "IP" + address[0] + " Port" + str(address[1]))
    _thread.start_new_thread(new_client, (conn, address))

s.close()
    # sys.exit()

