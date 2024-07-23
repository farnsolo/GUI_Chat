import pickle
import socket
from _thread import start_new_thread
import serverCard

serverList = {}

def connectionHandling(c):
    global serverName
    while True:
        try:
            message = c.recv(1024)
            if not message:
                break
            commandRecv = message[:1].decode()
            messageRecv = message[1:len(message)]
            match(commandRecv):
                case "1":
                    serverName = messageRecv.decode()
                    serverList[serverName].appendConn(c)
                case "2":
                    serverList[serverName].getServerConn().sendall(messageRecv)
                case "3":
                    serverName = messageRecv.decode()
                    serverList[serverName] = serverCard.serverCard(c)
                case "4":
                    listConn = serverList[serverName].getConnList()
                    for conn in listConn:
                        conn.sendall(messageRecv)
                case "6":
                    c.sendall(pickle.dumps(list(serverList.keys())))
                case "7":
                    listConn = serverList[serverName].getConnList()
                    if len(listConn) > 0:
                        for conn in listConn:
                            conn.close()
                    serverList.pop(serverName)
                    break
                case "8":
                    serverList[serverName].removeConn(c)
        except Exception as e:
            print(e)
    c.close()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("44.222.65.104", 1099))
    sock.listen()
    
    while True:
        conn, addr = sock.accept()
        try:
            start_new_thread(connectionHandling,(conn,))
        except Exception as e:
            print(e)
if __name__ == '__main__':
    main()