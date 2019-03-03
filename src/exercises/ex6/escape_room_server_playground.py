import asyncio
import sys
from escape_room import EscapeRoom
import playground

class EscapeServer(asyncio.Protocol):
    def connection_made(self, transport):
        # peername = transport.get_extra_info('peername')
        # print('Connection from {}'.format(peername))
        self.transport = transport
        self.room = EscapeRoom()
        self.room.start()

    def data_received(self, raw_data):
        try:
            message = raw_data.decode('utf-8')[:-1]
            # print(message)
        except UnicodeDecodeError as e:
            self.transport._write(str(e).encode('utf-8'))
        else:
            self.handle(message)

    def handle(self, message):
        out = self.room.command(message)
        if self.room.status() == 'dead':
            out = out + '\n' + 'You died!'
            self.transport.write(str.encode(out))
            self.transport.close()
        elif self.room.status() == 'escaped':
            out = out + '\n' + 'You escaped!'
            self.transport.write(str.encode(out))
            self.transport.close()

        # print("Send: %r" % out)
        self.transport.write(str.encode(out))

        if message == 'quit':
            # print("Close the client socket")
            self.transport.close()


def main(argv):
    port = int(argv[1]) if len(argv) >= 2 else 8888
    loop = asyncio.get_event_loop()

    # coro = loop.create_server(EscapeServer, '', port)
    coro = playground.create_server(EscapeServer, '20191.2.5.2554', port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    main(sys.argv)