# py-unix-socket

Stupid Python implementation of a Unix domain socket server. 



* [Unix domain socket](#unix-domain-socket)
* [Install](#install)
* [Quickstart](#quickstart)
* [Features](#features)
	* [Custom address namespace](#custom-address-namespace)
	* [Acknowledgment](#acknowledgment)
	* [Custom handler](#custom-handler)
	* [Broadcast](#broadcast)
* [Client](#client)
	* [Connect](#connect)
	* [Send and receive](#send-and-receive)
	* [Exit request](#exit-request)


## Unix domain socket
A Unix domain socket or IPC socket (inter-process communication socket) is a data communications endpoint for exchanging data between processes executing on the same host operating system.

The Unix domain socket facility is a standard component of POSIX operating systems.

The API for Unix domain sockets is similar to that of an Internet socket, but rather than using an underlying network protocol, all communication occurs entirely within the operating system kernel.

Unix domain sockets may use the file system as their address name space. 


## Install 
```bash 
pip install -U . 
```

## Quickstart 
- Default address namespace : `/tmp/unix_socket.sock`

```python
from unix_socket.unix_socket import UnixSocket

if __name__=="__main__":
    with UnixSocket() as ipc : 
        ipc.run()
```

## Features  
### Custom address namespace 
```python 
if __name__=="__main__":
    with UnixSocket(cust_add_namespace = "/path/to/file") as ipc : 
        ipc.run()
```

### Acknowledgment 
By default, the server does not send an acknowledgment back to the client process after processing a payload.
It is possible to activate the feature  when starting the server : 
```python 
if __name__=="__main__":
    with UnixSocket(with_ack = True, ack_message = "ack_event") as ipc : 
        ipc.run()
```

The default acknowledgment event sent to the client process is: `"__ACK__\n"`

### Custom handler
By default, the server will log incoming payload. 
It's possible to add a custom handler method to process incoming payload. 
```python 
def custom_worker(payload) : 
	... 

if __name__=="__main__":
    with UnixSocket(custom_handler = worker) as ipc : 
        ipc.run()
```

### Broadcast 
By default, broadcasting payload to active clients is disabled. 
To activate the broadcast to all active clients : 

```python 

if __name__=="__main__":
    with UnixSocket(with_broadcast = True) as ipc : 
        ipc.run()
```

## Client 
### Connect 
```python
client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.connect("/tmp/unix_socket.sock")
```
### Send and receive
```python
message = "foobar\n"
client.send(message.encode())

r = client.recv(1024)
print ( 'Received :', r.decode())
```

### Exit request
```python
message = "exit\n"
client.send(message.encode())
```










