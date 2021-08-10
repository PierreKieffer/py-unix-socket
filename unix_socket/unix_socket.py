#!/usr/bin/env python3
import os
import socket
import threading
import sys 

class UnixSocket(): 
    def __init__(self, cust_file_socket = None): 
        if cust_file_socket != None : 
            self._file_socket = cust_file_socket
        else : 
            self._file_socket = "/tmp/unix_socket.sock"

        self._clients = []

    def __enter__(self) : 
        """context manager
        Enter
        """
        self.start_ipc_server()
        return self

    def __exit__(self, type, value, traceback): 
        """context manager
        Exit
        """
        self.shutdown()

        if os.path.exists(self._file_socket): 
            os.remove(self._file_socket)
        print("unix socket is closed")

    def start_ipc_server(self) : 
        """start_ipc_server
        Init inter process communication server
        """
        if os.path.exists(self._file_socket): 
            os.remove(self._file_socket)

        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server.bind(self._file_socket)
        self.server.listen()
        print("unix socket is opened")

    def shutdown(self) : 
        """shutdown
        Close all active client sockets
        Close server
        """
        for client in self._clients : 
            self._clients.remove(client)
            client.close()

        self.server.close()

    def handler(self, client_socket, custom_handler = None, with_ack = False, broadcast = False): 
        """handler
        Handle client socket 
        """
        while True :
            pckt = client_socket.recv(4096)
            if pckt: 
                decode = pckt.decode().split("\n")[0].split("\r")[0]
                if decode == "exit" : 
                    client_socket.close()
                    sys.exit()
                else : 
                    if custom_handler is None : 
                        print("Event received : {}".format(decode))
                        if with_ack : 
                            client_socket.send(str.encode("__ACK__\n"))

                        if broadcast : 
                            print("Event broadcast : {}".format(decode))
                            self.broadcast(client_socket, decode)

                    else : 
                        custom_handler(decode)
                        if with_ack : 
                            client_socket.send(str.encode("__ACK__\n"))

                        if broadcast : 
                            print("Event broadcast : {}".format(decode))
                            self.broadcast(client_socket, decode)

    def broadcast(self, sender_socket, payload) : 
        """broadcast
        If broadcast is availabled in handler, the payload is sent to all active client sockets
        """
        for target_client in self._clients : 
            if target_client != sender_socket : 
                target_client.send(str.encode("{}\n".format(payload)))

    def run(self, custom_handler = None, with_ack = False, broadcast = False): 
        """run 
        Accept client connections, open and handle client sockets in independant threads
        """
        while True : 
            try :
                self.client_socket, _ = self.server.accept()
                self._clients.append(self.client_socket)

                self.client_thread = threading.Thread(
                        target=self.handler,
                        args=(self.client_socket,),
                        kwargs={"custom_handler" : custom_handler, "with_ack" : with_ack, "broadcast" : broadcast}
                        )

                self.client_thread.setDaemon(True)
                self.client_thread.start()
            except : 
                return

if __name__=="__main__":
    with UnixSocket() as ipc : 
        ipc.run(with_ack = True, broadcast = True)

