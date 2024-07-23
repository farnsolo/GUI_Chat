import socket
import time
from tkinter import messagebox
import threading

class serverC:
    def __init__(self, name):
        # socket.create_server could come in use
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.NAME = name
        messagebox.showinfo("",f"Server {self.NAME} Online")
        
    def create_server(self):
        self.server_running = True  
        try:
            self.sock.connect(("44.222.65.104",1099))
            self.sock.sendall(self.buildMessage("3",self.NAME))
            # Accept connection
            self.t1 = threading.Thread(target=self.receive)
            self.t1.daemon = True
            self.t1.start()
        except OSError as e:
            messagebox.showerror("Connection failed",e)
    
    def receive(self):
        # byteString time!
        while self.server_running:
            try:
                message = self.sock.recv(1024)
                if not message:
                    continue
                msg = self.buildMessage("4",message.decode())
                self.sock.sendall(msg)
            except OSError as e:
                if not self.server_running and e.errno == 10038:
                    messagebox.showinfo("Server Notification", "Server has Stopped")
                if e.errno == 10056:
                    messagebox.showinfo("Connection Ended", e)
            except Exception as e:
                messagebox.showerror("Error", e)
        
    def broadcast(self, message):
        try:
            msg = self.buildMessage("4",message.decode())
            self.sock.sendall(msg)
        except Exception as e:
            print("ERROR Here" + str(e))

    def stop_server(self):
        self.server_running = False
        try:
            self.sock.send(self.buildMessage("7",""))
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except OSError as e:
            if e.errno == 10054:
                messagebox.showinfo("Connection Ended", e)
        del self.sock
    
    def buildMessage(self, command,msg):
        command_bytes = command.encode()
        # x bytes
        msg_bytes = msg.encode()
        # # x bytes
        byteString = command_bytes
        byteString += msg_bytes
        return byteString