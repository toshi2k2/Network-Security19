import asyncio
import sys

def asyn_inputs(q):
    asyncio.async(q.put(sys.stdin.readline()))

class EscapeClient(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        self.transport = transport
        asyn_in = asyncio.async(q.get())
        asyn_in.add_done_callback(self.send)

    def data_received(self, data):
        decoded_data = data.decode('utf-8')
        print(decoded_data)
        if decoded_data[-5:] != 'died!' and decoded_data[-8:] != 'escaped!':
            asyn_in = asyncio.async(q.get())
            asyn_in.add_done_callback(self.send)

    def connection_lost(self, eee):
        # print(self.transport.is_closing())
        self.loop.stop()

    def send(self, in2):
        out = in2.result()
        self.transport.write(out.encode())

port = 8888
host = '127.0.0.1'

if len(sys.argv) > 1:
    if ':' in sys.argv[1]:
        s_in = sys.argv[1].split(':')
        host = s_in[0]
        port = int(s_in[1])
        # print("port: ", host, port)
    else:
        port = int(sys.argv[1])

q = asyncio.Queue()
loop = asyncio.get_event_loop()
loop.add_reader(sys.stdin, asyn_inputs, q)
coro = loop.create_connection(lambda: EscapeClient(loop), host, port)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
