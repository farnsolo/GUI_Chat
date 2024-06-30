import socket
from tkinter import messagebox
import threading
import backendInterface

class serverC:
    def __init__(self, name):
        self.usersIP = []
        self.userNames = {}
        # socket.create_server could come in use
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostName = socket.gethostname()
        self.HOST = socket.gethostbyname(hostName)
        self.PORT = 2525
        self.NAME = name
        backendInterface.listServer(self.NAME,self.HOST)
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen()
        messagebox.showinfo("",f"Server listening on {self.HOST}:{self.PORT}")
        
    def create_server(self):
        self.server_running = True  
        while self.server_running: 
            try:
                # Accept connection
                self.conn, self.addr = self.sock.accept()
                self.usersIP.append(self.conn)
                self.broadcast(f"User {self.addr} has connected")
                self.t1 = threading.Thread(target=self.receive, args=(self.conn,self.addr))
                self.t1.daemon = True
                self.t1.start()
            except OSError as e:
                if not self.server_running and e.errno == 10038:
                    messagebox.showinfo("Server Notification", "Server has Stopped")
                    break
                else:
                    messagebox.showerror(e)
    
    def receive(self, conn, addr):
        # byteString time!
        while self.server_running:
                    try:
                        message = conn.recv(1024)
                        commandRecv = message[:1].decode()
                        messageRecv = message[1:len(message)].decode()
                        if commandRecv == "1":
                            self.broadcast(f"User {self.userNames[addr[0]]} says: " + messageRecv)
                        elif commandRecv == "0":
                            self.userNames[addr[0]] = messageRecv
                        else:
                            self.delete_user(self.conn)
                    except OSError as e:
                        if e.errno == 10056:
                            messagebox.showwarning("Connection Ended", e)
                    except Exception as e:
                        messagebox.showerror("Error Occurred", e)
        
            
    def broadcast(self, message):
        for user in self.usersIP:
            user.sendall(message.encode())
            
    def delete_user(self, conn):
        for user in self.usersIP:
            if user == conn:
                self.usersIP.remove(user)
                self.conn.shutdown(socket.SHUT_RDWR)
                self.conn.close()


    def stop_server(self):
        self.server_running = False
        for user in self.usersIP:
            # fin ack shutdown with each user 
            user.shutdown(socket.SHUT_RDWR)
            user.close()
        self.sock.close()
        del self.sock
