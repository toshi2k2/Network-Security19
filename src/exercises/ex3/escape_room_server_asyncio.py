import asyncio
from escape_room import EscapeRoom

@asyncio.coroutine
def handle_echo(reader, writer):
    room = EscapeRoom()
    room.start()
    while room.status() == 'locked':
        data = yield from reader.read(1024)
        message = data.decode()
        # addr = writer.get_extra_info('peername')
        # print("Received %r from %r" % (message, addr))

        out = room.command(message)
        if room.status() == 'dead':
            out = out + '\n' + 'You died!'
        elif room.status() == 'escaped':
            out = out + '\n' + 'You escaped!'

        # print("Send: %r" % out)
        writer.write(str.encode(out))
        yield from writer.drain()

        if message == 'quit':
            # print("Close the client socket")
            writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
# print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()