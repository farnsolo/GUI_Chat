import socket
import pickle
from MainInterface import getIP, createPair, removeServer, getServerNames

# handle communication to server, use just TCP
# May use dnsPython but want to see if this will suffice

# Make own DNS thing
# Binary encoded
# First three bits for operation + message encoded in ASCII

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("192.168.1.127", 1010))
sock.listen()

while(True):
        conn, addr = sock.accept()
        try:
            print(addr)
            message = conn.recv(1024)
            length = 0
            length = message[:1].decode() if message[1:2].decode() == "-" else message[:2].decode()
            length  = int(length)
            length += 3
            commandRecv = message[2:3].decode()
            serverNameRecv = message[3:length]
            ipRecv = message[length:len(message)]
            
            if commandRecv == "1":
                ip = getIP(serverNameRecv)
                conn.sendall(ip)
            elif  commandRecv == "4":
                data = pickle.dumps(getServerNames())                     
                conn.sendall(data)
            elif commandRecv == "2":
                createPair(serverNameRecv,ipRecv)
            else:
                removeServer(serverNameRecv)
        except IOError as exception:
            print(exception)
