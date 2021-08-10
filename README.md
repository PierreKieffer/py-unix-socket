# py-unix-socket

Python implementation of a Unix domain socket server. 

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
from unix_socket import unix_socket

if __name__=="__main__":
    with UnixSocket() as ipc : 
        ipc.run()
```

## Custom address namespace 
```python 
if __name__=="__main__":
    with UnixSocket(cust_add_namespace = "/path/to/file") as ipc : 
        ipc.run()
```

## Acknowledgment 
By default, the server does not send an acknowledgment back to the client process after processing a payload.
It is possible to activate the feature  when starting the server : 
```python 
if __name__=="__main__":
    with UnixSocket() as ipc : 
        ipc.run()
```

The acknowledgment event sent to the client process is: `"__ACK__\n"`

## Acknowledgments  
```python 
if __name__=="__main__":
    with UnixSocket() as ipc : 
        ipc.run()
```












