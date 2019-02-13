import asyncio
import sys

stdin_queue = []
stdout_queue = []

class EscapeClient(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop

    def connection_made(self, transport):
        self.transport = transport
        # asyn_in = asyncio.async(q.get())
        # asyn_in.add_done_callback(self.send)

    def data_received(self, data):
        decoded_data = data.decode('utf-8')
        # print(decoded_data)
        stdout_queue.append(decoded_data)
        # print(decoded_data)
        # if decoded_data[-5:] != 'died!' and decoded_data[-8:] != 'escaped!':
        #     asyn_in = asyncio.async(q.get())
        #     asyn_in.add_done_callback(self.send)

    def connection_lost(self, eee):
        # print(self.transport.is_closing())
        self.loop.stop()

    # def send(self, in2):
    #     out = in2.result()
    #     self.transport.write(out.encode())

async def async_input(prompt):
    print(prompt, end="")
    sys.stdout.flush()
    while len(stdin_queue) == 0:
        await asyncio.sleep(.1)
    return stdin_queue.pop(0)

async def game_runner(protocol):
    while True:
        command = await async_input(">> ")
        # print(command)
        # print(protocol.transport.get_write_buffer_limits(), protocol.transport.get_write_buffer_size())
        # protocol.transport.write('yoo'.encode('utf-8'))
        protocol.transport.write(command.encode())
        while len(stdout_queue) == 0:
            await asyncio.sleep(0)
        output = stdout_queue.pop(0)
        print(output)
        if output[-5:] == 'died!' or output[-8:] == 'escaped!':
            break

port = 8888
host = '127.0.0.1'

# def asyn_inputs(q):
#     asyncio.async(q.put(sys.stdin.readline()))

def handle_stdin():
    line_in = sys.stdin.readline()
    # line_in = line_in[:-1] # remove \n
    stdin_queue.append(line_in)
    # handle line_in

if len(sys.argv) > 1:
    if ':' in sys.argv[1]:
        s_in = sys.argv[1].split(':')
        host = s_in[0]
        port = int(s_in[1])
        # print("port: ", host, port)
    else:
        port = int(sys.argv[1])

# q = asyncio.Queue()
loop = asyncio.get_event_loop()
# loop.add_reader(sys.stdin, asyn_inputs, q)
# loop.add_reader(sys.stdin, handle_stdin)
coro = loop.create_connection(lambda: EscapeClient(loop), host, port)
_,protocol = loop.run_until_complete(coro)

loop.add_reader(sys.stdin, handle_stdin)
asyncio.ensure_future(game_runner(protocol))

loop.run_forever()
loop.close()
