import socket
from tkinter import messagebox
import random
import threading

def randomSeq(self):
        characters = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','j','k','l','z','x','c','v','b','n','m','1','2','3','4','5','6','7','8','9']
        sq = ""
        for x in range(15):
            i = random.randint(0,35)
            sq += characters[i]
        return sq

class serverC:
    def __init__(self):
        self.users = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = 'xxx.xxx.xxx.xxx'
        self.PORT = 2525
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen()
        print(f"Server listening on {self.HOST}:{self.PORT}")
        self.serverSeq = randomSeq(self)
        print(self.sock)
        
    def create_server(self):
        self.server_running = True  
        while self.server_running: 
            try:
                # Accept connection
                self.conn, self.addr = self.sock.accept()
                self.users.append(self.conn)
                self.broadcast(f"User {self.addr} has connected")
                print(self.conn)
                #self.conn.sendall(self.serverSeq.encode())
                self.t1 = threading.Thread(target=self.receive, args=(self.conn,self.addr))
                self.t1.daemon = True
                self.t1.start()
            except OSError as e:
                if not self.server_running and e.errno == 10038:
                    messagebox.showinfo("Server Notification", "Server has Stopped")
                    break
                else:
                    raise e
    
    def receive(self, conn, addr):
        while self.server_running:
                    try:
                        message = conn.recv(1024).decode()
                        # CHANGE 'CODE'
                        if message == "123":
                            self.delete_user(self.conn)
                        else:
                            self.broadcast(f"User {addr} says: " + message)
                    except OSError as e:
                        if e.errno == 10056:
                            messagebox.showwarning("Connection Ended", e)
                    except Exception as e:
                        messagebox.showerror("Error Occurred", e)
        
            
    def broadcast(self, message):
        for user in self.users:
            user.sendall(message.encode())
            
    def delete_user(self, conn):
        for user in self.users:
            if user == conn:
                self.users.remove(user)
                self.conn.close()


    def stop_server(self):
        self.server_running = False
        self.broadcast("1")
        for user in self.users:
            user.close()
        self.sock.close()
