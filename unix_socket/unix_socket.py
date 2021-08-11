#!/usr/bin/env python3
import os
import socket
import threading
import sys 
import logging


class UnixSocket(): 
    def __init__(self, cust_add_namespace = None, with_ack = False, ack_message = "__ACK__\n", with_broadcast = False, custom_handler = None): 
        if cust_add_namespace != None : 
            self._add_namespace = cust_add_namespace
        else : 
            self._add_namespace = "/tmp/unix_socket.sock"

        self._clients = []
        self.with_ack = with_ack
        self.ack_message = ack_message
        self.with_broadcast = with_broadcast
        self.custom_handler = custom_handler

        self.logger = logging.getLogger("unix_socket.logger")

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

        if os.path.exists(self._add_namespace): 
            os.remove(self._add_namespace)
        self.logger.info("unix socket is closed")

    def start_ipc_server(self) : 
        """start_ipc_server
        Init inter process communication server
        """
        if os.path.exists(self._add_namespace): 
            os.remove(self._add_namespace)

        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server.bind(self._add_namespace)
        self.server.listen()
        self.logger.info("unix socket is opened")

    def shutdown(self) : 
        """shutdown
        Close all active client sockets
        Close server
        """
        for client in self._clients : 
            self._clients.remove(client)
            client.close()

        self.server.close()

    def close_client_socket(self, client_socket) : 
        client_socket.close()
        self._clients.remove(client_socket)


    def handler(self, client_socket): 
        """handler
        Handle client socket 
        """
        while True :
            pckt = client_socket.recv(4096)
            if pckt: 
                decode = pckt.decode().split("\n")[0].split("\r")[0]
                if decode == "exit" : 
                    self.logger.info("Close client socket {}".format(client_socket))
                    self.close_client_socket(client_socket)
                    sys.exit()
                else : 
                    if self.custom_handler is None : 
                        self.logger.info("Event received : {}".format(decode))
                        if self.with_ack : 
                            client_socket.send(str.encode(self.ack_message))

                        if self.with_broadcast : 
                            self.logger.info("Event broadcast : {}".format(decode))
                            self.broadcast(client_socket, decode)

                    else : 
                        self.custom_handler(decode)
                        if self.with_ack : 
                            client_socket.send(str.encode(self.ack_message))

                        if self.with_broadcast : 
                            self.logger.info("Event broadcast : {}".format(decode))
                            self.broadcast(client_socket, decode)

    def broadcast(self, sender_socket, payload) : 
        """broadcast
        If broadcast is availabled in handler, the payload is sent to all active client sockets
        """
        for target_client in self._clients : 
            if target_client != sender_socket : 
                target_client.send(str.encode("{}\n".format(payload)))

    def run(self): 
        """run 
        Accept client connections, open and handle client sockets in independant threads
        """
        while True : 
            try :
                self.client_socket, _ = self.server.accept()
                self.logger.info("New client connection {}".format(self.client_socket))
                self._clients.append(self.client_socket)

                self.client_thread = threading.Thread(
                        target=self.handler,
                        args=(self.client_socket,)
                        )

                self.client_thread.setDaemon(True)
                self.client_thread.start()
            except : 
                return

if __name__=="__main__":
    with UnixSocket() as ipc : 
        ipc.run(with_ack = True, broadcast = True)

