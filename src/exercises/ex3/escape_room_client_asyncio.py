import asyncio
import sys
# from aioconsole import ainput

@asyncio.coroutine
def tcp_echo_client(loop):
    reader, writer = yield from asyncio.open_connection('127.0.0.1', 8888, loop=loop)

    while True:
        message = input(">> ")
        # message = await ainput(">> ")
        # print('Send: %r' % message)
        writer.write(message.encode())

        data = yield from reader.read(1024)

        decoded_data = data.decode('utf-8')
        if decoded_data[-5:] == 'died!' or decoded_data[-8:] == 'escaped!':
            print(decoded_data)
            # print('Close the socket')
            writer.close()
            sys.exit()
        print(decoded_data)
        if message == 'quit':
            writer.close()
            sys.exit()


loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(loop))
loop.close()