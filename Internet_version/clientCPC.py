import tkinter as tk
import tkinter.scrolledtext as tkk
from tkinter import messagebox
import threading
import socket
import time

class client_GUI:
    def __init__(self, serverName, username):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rcvLoop = True
        # Is a connection already in place?
        self.socketConnected = False
        
        self.serverName = serverName
        self.window = tk.Tk()
        self.window.geometry("500x500")
        self.window.title("Chat")
        
        self.label = tk.Label(self.window, text="Client Handling", font=("Ariel", 18))
        self.label.pack()
        
        self.text_area = tkk.ScrolledText(self.window)
        self.text_area.pack()
        self.text_area.config(state='disabled')
        
        self.text_enter = tkk.Text(self.window, height = 2, width = 70)
        self.text_enter.pack()
        
        self.username = username
        
        # Send message
        self.text_enter.bind("<Return>",self.send_message)
        # New line command
        self.text_enter.bind("<Control-Return>", self.enter_line)
        self.window.protocol("WM_DELETE_WINDOW",self.client_close)
        self.connect_server()
        self.window.mainloop()
        
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
        
    def connect_server(self):
        self.socketConnected = True
        self.t3 = threading.Thread(target=self.listen)
        self.t3.daemon = True
        self.t4 = threading.Thread(target=self.receive)
        self.t4.daemon = True
        self.t3.start()
        self.t4.start()
        

# -----------------------------------------------------------------------------------------------------------------------------------------------------------

    def receive(self):
        self.serverSq = ""
        # Potential need of a fix
        time.sleep(0.1)
        while self.rcvLoop:
            try:
                self.message = self.sock.recv(1024).decode()
                if self.message:
                    self.text_area.config(state='normal')
                    self.text_area.insert('end', self.message + "\n")
                    self.text_area.yview('end')
                    self.text_area.config(state='disabled') 
                elif self.message == 0:
                    messagebox.showinfo("Connection has ended", "Host has destroyed server")
                    self.window.destroy()
                    break
            except ConnectionAbortedError:
                break
            except Exception as e:
                # Possibly more elegant way to implement this?
                if(self.rcvLoop):
                    messagebox.showerror("ERROR",e)
                    #print("Hello")
                    #print(e)
            
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
            
    def listen(self):
        try:
            self.sock.connect(("44.222.65.104",1099))
            self.socketConnected = True
            byteString = self.buildMessage("1",self.serverName)
            self.sock.sendall(byteString)
            server_connect_message = f"Connected to server {self.serverName}. \nPress the Enter key to send message"
            self.enter_message_textbox(server_connect_message)
        except Exception as e:
            messagebox.showerror("ERROR",e)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
            
    def send_message(self, event):
        try:
            message = self.text_enter.get("1.0",'end-1c')
            message = self.message_check(message)
            message = f"{self.username} says: {message}"
            byteString = self.buildMessage("2",message)
            self.sock.sendall(byteString)
            self.text_enter.delete("1.0", 'end')
            # The return 'break' prevents the return key from moving down a line in the text box
            # I believe this prevents the default behavior from executing by exiting the function
            return 'break'
        except Exception as e:
            self.enter_message_textbox("",str(e))
            
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
            
    def enter_line(self,event):
        event.widget.insert("insert", "\n")
        return 'break'
    
    # Removes trailing whitespace 
    def message_check(self, message):
        return message.strip()
        
    def enter_message_textbox(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert('end', message + "\n")
        self.text_area.yview('end')
        self.text_area.config(state='disabled') 
        
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
        
    def client_close(self):
        ans  = messagebox.askyesno(title="Exit", message=f"Do you want to exit window?")
        if ans and self.socketConnected:
            self.sock.sendall(self.buildMessage("8",""))
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        if ans:
            self.rcvLoop = False
            self.window.destroy()
            
    
    def buildMessage(self, command,msg):
        command_bytes = command.encode()
        # x bytes
        msg_bytes = msg.encode()
        
        byteString = command_bytes
        byteString += msg_bytes
        return byteString