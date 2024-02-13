import socket
from tkinter import messagebox
import threading

class serverC:
    def __init__(self):
        self.users = []
        # socket.create_server could come in use
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = 'xxxxxxxxxx'
        self.PORT = 2525
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen()
        print(f"Server listening on {self.HOST}:{self.PORT}")
        
    def create_server(self):
        self.server_running = True  
        while self.server_running: 
            try:
                # Accept connection
                self.conn, self.addr = self.sock.accept()
                self.users.append(self.conn)
                self.broadcast(f"User {self.addr} has connected")
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
                        if message:
                            self.broadcast(f"User {addr} says: " + message)
                        else:
                            self.delete_user(self.conn)
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
                self.conn.shutdown(socket.SHUT_RDWR)
                self.conn.close()


    def stop_server(self):
        self.server_running = False
        for user in self.users:
            # fin ack shutdown with each user 
            user.shutdown(socket.SHUT_RDWR)
            user.close()
        self.sock.close()
