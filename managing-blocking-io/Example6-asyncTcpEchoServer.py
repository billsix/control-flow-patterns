# Copyright (c) 2019 William Emerison Six
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import asyncio
import os

# global list of total number of messages read,
# regardless of the connection
number_of_messages_read = 0


async def handle_echo(reader, writer):
    global number_of_messages_read

    ipaddress, port = writer.get_extra_info('peername')
    print("Connection initiated from : "+ipaddress+":"+str(port))
    # this call does not block
    writer.write(("Welcome to the server" + os.linesep).encode())
    # force the writing to block
    await writer.drain()


    while True:
        # await will block this async function,
        # it does not block the CPU, as the event
        # loop defined below can still proceed.  Other connections
        # can still proceed without needing threads,
        # and no mutexes are required
        data = await reader.read(2048)
        # once the client sends data, the event loop
        # will allow the rest of this procedure to proceed

        # no mutexs needed
        number_of_messages_read += 1
        print("Received Message Number %s" % str(number_of_messages_read))

        print("Client({0}:{1}) sent : {2}".format(ipaddress,
                                                  port,
                                                  data.decode()))
        # this call does not block
        writer.write(("You sent me : " + data.decode()).encode())
        # force the writing to block
        await writer.drain()


loop = asyncio.get_event_loop()
server = loop.run_until_complete(
    asyncio.start_server(handle_echo,
                         '127.0.0.1',
                         9999,
                         loop=loop))

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))


try:
    print("Listening for incoming connections...")
    loop.run_forever()
except KeyboardInterrupt:
    pass
