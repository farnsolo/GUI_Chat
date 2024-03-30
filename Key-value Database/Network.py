import socket
from MainInterface import getName
from MainInterface import setName
import time

# handle communication to server, use just TCP
# May use dnsPython but want to see if this will surfice

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("192.168.1.107", 1010))
sock.listen()

while(True):
    try:
        conn, addr = sock.accept()
        while True:
            try:
                message = conn.recv(1024).decode()
                # FIND ALTERNATIVE TO 1
                if message == "1":
                    message = conn.recv(1024).decode()
                    conn.sendall(getName(message).encode())
                elif message == "2":
                    i = 0
                    messageBlock = []
                    while (i < 2):
                        # Remove try-catch perhaps
                        try:
                            message = conn.recv(1024).decode()
                            messageBlock.append(message)
                            i+=1
                        except Exception as e:
                            print(e)
                    setName(messageBlock[0],messageBlock[1])               
            except Exception as e:
                print(e)
                break
    except:
        print("Error")
