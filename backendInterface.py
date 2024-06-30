import socket
import pickle

# think about
def getServerNames():
    return commandToDNS("4","0","0")

def getServerIp(serverName):
    return commandToDNS("1",serverName,"0")

def listServer(serverName, ip):
    commandToDNS("2",serverName,ip)

    
def removeServer(serverName):
    commandToDNS("3",serverName,"0")
    
    
def commandToDNS(command, serverName, ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("192.168.1.127",1010))
    
    command_bytes = command.encode()
    # x bytes
    serverName_bytes = serverName.encode()
    # x bytes
    ip_bytes = ip.encode()
    
    # x bytes
    serverNameLength = str(len(serverName_bytes))
    if int(serverNameLength) < 10:
        serverNameLength += "-"
    serverNameLength_bytes = serverNameLength.encode()
    
    byteString = serverNameLength_bytes
    byteString += command_bytes
    byteString += serverName_bytes
    byteString += ip_bytes
    
    try:
        if command == "1":
            sock.sendall(byteString)
            serverIp = sock.recv(1024).decode()
            return serverIp
        
        if command == "4":
            sock.sendall(byteString)
            serverNames = sock.recv(1024)
            # Converts byte stream back into list object
            serverNames = pickle.loads(serverNames)
            return serverNames
        sock.sendall(byteString)
    except Exception as e:
        print("Exception " + e)
    
    sock.close()
