import socket
stopServerSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
with open("srv.cfg","r") as srvFile: connectivityTuple=eval(srvFile.read().strip()) 
stopServerSocket.connect(connectivityTuple)
stopServerSocket.sendall(bytes("11".ljust(1024),"utf-8"))
stopServerSocket.sendall(bytes("stop server","utf-8"))
stopServerSocket.close()
