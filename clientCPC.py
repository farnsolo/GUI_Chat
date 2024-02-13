import tkinter as tk
import tkinter.scrolledtext as tkk
from tkinter import messagebox
import threading
import socket
import time

class client_GUI:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rcvLoop = True
        self.window = tk.Tk()
        self.window.geometry("500x500")
        self.window.title("Chat")
        
        self.label = tk.Label(self.window, text="Client Handling", font=("Ariel", 18))
        self.label.pack()
        
        self.client_connectBu = tk.Button(self.window, text="Connect to server", font=("Ariel", 18), command=self.connect_server)
        self.client_connectBu.pack()
        
        self.text_area = tkk.ScrolledText(self.window)
        self.text_area.pack()
        self.text_area.config(state='disabled')
        
        self.text_enter = tkk.Text(self.window, height = 2, width = 70)
        self.text_enter.pack()
        
        self.text_enter.bind("<Return>",self.send_message)
        self.text_enter.bind("<Control-Return>", self.enter_line)
        self.window.protocol("WM_DELETE_WINDOW",self.client_close)
        self.window.mainloop()
        
    def connect_server(self):
        self.t3 = threading.Thread(target=self.listen)
        self.t3.daemon = True
        self.t4 = threading.Thread(target=self.receive)
        self.t4.daemon = True
        self.t3.start()
        self.t4.start()
        self.client_connectBu["state"] = "disabled"
        
    def receive(self):
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
                else:
                    messagebox.showinfo("Connection has ended", "Host has destroyed server")
                    self.window.destroy()
                    break
            except ConnectionAbortedError:
                break
            except Exception as e:
                # Possibly more elegant way to implement this?
                if(self.rcvLoop):
                    print("Hello")
                    print(e)
            
    def listen(self):
        self.addr = 'XXXXXXXXXX'
        self.sock.connect((self.addr, 2525))
        print(f"Connected to Server {self.addr}")
        server_connect_message = f"Connected to server {self.addr}. \nPress the Enter key to send message"
        self.enter_message_textbox(server_connect_message)
            
    def send_message(self, event):
        try:
            message = self.text_enter.get("1.0",'end-1c')
            message = self.message_check(message)
            self.sock.sendall(message.encode())
            self.text_enter.delete("1.0", 'end')
            # The return 'break' prevents the return key from moving down a line in the text box
            # I believe this prevents the default behavior from executing by exiting the function
            return 'break'
        except Exception as e:
            self.enter_message_textbox(e)
            
    def enter_line(self,event):
        event.widget.insert("insert", "\n")
        return 'break'
    
    def message_check(self, message):
        return message.strip()
        
    def enter_message_textbox(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert('end', message + "\n")
        self.text_area.yview('end')
        self.text_area.config(state='disabled') 
        
    def client_close(self):
        ans  = messagebox.askyesno(title="Exit", message=f"Do you want to exit server {self.addr}")
        if ans:
            self.rcvLoop = False
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.window.destroy()
