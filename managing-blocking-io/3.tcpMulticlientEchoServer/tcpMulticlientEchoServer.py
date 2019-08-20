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

import socket
import os
import select

host = "127.0.0.1"
port = 9999

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((host, port))

tcpsock.listen(4)
print("Listening for incoming connections...")

read_list = [tcpsock]

# global list of total number of messages read,
# regardless of the connection
number_of_messages_read = 0

while True:
    # get "readable" data streams, ones that are waiting
    # to be read because they have data
    readable, writable, errored = select.select(read_list, [], [])
    for s in readable:
        if s is tcpsock:
            # this would block, but it's in the readable list
            (clientsock, (ip, port)) = tcpsock.accept()
            print("Connection initiated from : {0}:{1}".format(ip,str(port)))
            read_list.append(clientsock)
            clientsock.send(("Welcome to the server" + os.linesep).encode())
        else:
            # this would block, but it's in the readable list
            data = s.recv(2048)
            number_of_messages_read += 1
            print("Received Message Number {0}".format(str(number_of_messages_read)))
            print("Client({0}:{1}) sent : {2}".format(ip, str(port), data.decode()))
            s.send(("You sent me : "+data.decode()).encode())
