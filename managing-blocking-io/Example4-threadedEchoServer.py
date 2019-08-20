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
import threading
import os

# global list of total number of messages read,
# regardless of the connection
number_of_messages_read = 0


class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] New thread started for "+ip+":"+str(port))

    def run(self):
        print("Connection from : "+ip+":"+str(port))

        clientsock.send(("Welcome to the server" + os.linesep).encode())

        # data = "ignore" because Python doesn't have a do while loop
        # give data a garbage value so that the first evaluation
        # of the loop will proceed
        data = "ignore"

        while len(data):
            # this blocks, but who cares?  It's only blocking
            # in it's own thread, all other threads will
            # continue executing
            data = self.clientsocket.recv(2048)
            # not thread safe, as this is a global variable
            # if two threads both read the value of "number_of_messages_read"
            # as "5" before the first thread updates the value to "6",
            # both threads will update the value to be "6", and
            # thus it won't be the correct value of "7"
            number_of_messages_read += 1
            print("Received Message Number %s" % str(number_of_messages_read))
            print("Client(%s:%s) sent : %s" %
                  (self.ip, str(self.port), data.decode()))
            self.clientsocket.send(("You sent me : "+data.decode()).encode())

        print("Client at "+self.ip+" disconnected...")


host = "127.0.0.1"
port = 9999

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcpsock.bind((host, port))

while True:
    tcpsock.listen(4)
    print("Listening for incoming connections...")

    # this blocks, but who cares?  It's only blocking
    # in it's own thread, all other threads will
    # continue executing (because of the newthread.start below
    (clientsock, (ip, port)) = tcpsock.accept()

    # pass clientsock to the ClientThread thread object being created
    newthread = ClientThread(ip, port, clientsock)
    newthread.start()
