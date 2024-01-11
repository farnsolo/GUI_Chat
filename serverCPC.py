import socket
from tkinter import messagebox
import random

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
        self.HOST = 'xx.x.xx.xxx'
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
                self.conn, addr = self.sock.accept()
                self.users.append(self.conn)
                self.broadcast(f"User {addr} has connected")
                #self.conn.sendall(self.serverSeq.encode())
                while self.server_running:
                    try:
                        message = self.conn.recv(1024).decode()
                        # if message == "2":
                        #   self.broadcast(f"User {addr} has disconnected")
                        #  self.delete_user(self.conn)
                        # print(f"User {addr} has left")
                        #else:
                        self.broadcast(f"User {addr} says: " + message)
                    except OSError as e:
                        if e.errno == 10056:
                            messagebox.showwarning("Connection Ended", e)
                    except Exception as e:
                        messagebox.showerror("Error Occurred", e)
            except OSError as e:
                if not self.server_running and e.errno == 10038:
                    messagebox.showinfo("Server Notification", "Server has Stopped")
                    break
                else:
                    raise e
        
            
    def broadcast(self, message):
        for user in self.users:
            user.sendall(message.encode())
            
    # def delete_user(self, conn):
    #    for user in self.users:
    #       if user == conn:
    #          self.users.remove(user)
    def stop_server(self):
        self.server_running = False
        self.broadcast("1")
        for user in self.users:
            user.close()
        self.sock.close()