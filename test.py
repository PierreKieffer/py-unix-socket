#!/usr/bin/env python3

from unix_socket.unix_socket import UnixSocket

def worker(payload) : 
    print("payload : {} :)".format(payload))

if __name__=="__main__":
    with UnixSocket(with_ack=True) as ipc : 
        ipc.run()
