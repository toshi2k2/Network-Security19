import asyncio
import sys
import time
import os
import mimetypes
# from escape_room import EscapeRoom

class ExampleHttpServer(asyncio.Protocol):
    def __init__(self, document_root):
        self.document_root = document_root
        # initialization

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        # print('Connection from {}'.format(peername))
        self.transport = transport
        self.buffer = ''
        # self.room = EscapeRoom()
        # self.room.start()

    def data_received(self, raw_data):
        try:
            message = raw_data.decode('utf-8')
            self.buffer += message
        except UnicodeDecodeError as e:
            self.transport._write(str(e).encode('utf-8'))
        else:
            while '\r\n\r\n' in self.buffer:
                # print("AWOOOO")
                head, x = self.buffer.split('\r\n\r\n', 1)
                self.buffer = x
                # print("head:\r\n", head,'\r\n\r\n', "buffer:\r\n", self.buffer)
                self.mixresque(head)

    def mixresque(self, message):
        t = time.asctime(time.localtime(time.time()))

        error_file = '<html><head><title>404 Not Found</title></head><body bgcolor="red"><center>' \
                     '<h1>404 Not Found</h1></center><hr><center>nginx</center></body></html>'
        error = 'HTTP/1.1 404 Not Found\r\nDate: '+ t +'\r\nServer: NetSec Prototype Server 1.0\r\n' \
                                                       'Content-Length: '+str(len(error_file))+'\r\n\r\n'
        command, vals = message.split('\r\n', 1)

        method, uri, version = command.split(' ')
        if method != 'GET':
            self.transport.write(str.encode(error+error_file))
            self.transport.close()
        if version[-3:] not in ['1.1', '1.0']:
            self.transport.write(str.encode(error+error_file))
            self.transport.close()

        if self.document_root[-1:] == '/':
            if len(self.document_root) > 1:
                self.document_root = self.document_root[:-1]
            else:
                self.document_root = ''

        address = self.document_root + '/' + uri
        if os.path.isdir(address):
            address += '/index.html'

        con_type = mimetypes.MimeTypes().guess_type(address)[0]
        # print("con_type: ", con_type)
        try:
            last_modified = time.asctime(time.localtime(os.stat(address).st_mtime))
        except Exception:
            last_modified = t
        try:
            file = open(address, 'rb')  # open file , r => read , b => byte format
            response = file.read()
            file.close()
            con_length = len(response)
        except Exception as e:
            self.transport.write(str.encode(error+error_file))
            self.transport.close()
        else:
            out = 'HTTP/1.1 200 OK\r\nDate: '+t+'\r\nServer: NetSec Prototype Server 1.0\r\n' \
                  'Last-Modified: '+last_modified+'\r\nContent-Length: '+str(con_length)+'\r\nConnection:' \
                  ' close\r\nContent-Type: '+con_type+'\r\n\r\n'
            # print(out)

            self.transport.write(str.encode(out)+response)
            self.transport.close()
        # print("COMMAND: ", command)

def main(argv):
    # port = int(argv[1]) if len(argv) >= 2 else 8888
    doc_root = sys.argv[1] if len(argv) >= 2 else './'
    port = 80
    loop = asyncio.get_event_loop()

    coro = loop.create_server(lambda: ExampleHttpServer(doc_root), '', port)
    server = loop.run_until_complete(coro)

    # print("server created")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    main(sys.argv)