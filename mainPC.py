import tkinter as tk
import tkinter.scrolledtext as tkk
from tkinter import messagebox
import serverCPC
import threading
import queue
import socket
import time

class client_GUI:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        self.serverSq = ""
        time.sleep(0.1)
        while True:
            try:
                self.message = self.sock.recv(1024).decode()
                # FIND ALTERNATIVE TO 1
                if self.message == "1": 
                    messagebox.showinfo("Connection has ended", "Host has destroyed server")
                    self.window.destroy()
                    break
                else:
                    self.text_area.config(state='normal')
                    self.text_area.insert('end', self.message + "\n")
                    self.text_area.yview('end')
                    self.text_area.config(state='disabled') 
            except ConnectionAbortedError:
                break
            except Exception as e:
                print("Hello")
                print(e)
                #self.sock.close()
                #break
            
    def listen(self):
        self.addr = 'xx.x.xx.xxx'
        self.sock.connect((self.addr, 2525))
        print(f"Connected to Server {self.addr}")
        server_connect_message = f"Connected to server {self.addr}. \nPress the Enter key to send message"
        self.enter_message_textbox(server_connect_message)
            
    def send_message(self, event):
        try:
            message = self.text_enter.get("1.0",'end-1c')
            self.sock.sendall(message.encode())
            self.text_enter.delete("1.0", 'end')
        except Exception as e:
            self.enter_message_textbox(e)
            
    def enter_message_textbox(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert('end', message + "\n")
        self.text_area.yview('end')
        self.text_area.config(state='disabled') 
    
    # def on_close(self):
    #     code = "2"
    #    self.sock.sendall(code.encode())
    #   self.sock.close()
        
class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.label = tk.Label(self.root, text="Server Handling", font=("Ariel", 18))
        self.label.pack()        
        self.server_createBu = tk.Button(self.root, text="Create server", font=("Ariel",16), command=self.create_server)
        self.server_createBu.pack()
        self.server_destroyBu = tk.Button(self.root, text="Destroy server", font=("Ariel", 16), command=self.stop_server)
        self.server_destroyBu.pack()
        self.client = tk.Button(self.root, text="Client", font=("Ariel", 18), command=client_GUI)
        self.client.pack()
        
        self.message_queue = queue.Queue()
        self.root.mainloop()
        
    def create_server(self):
        self.server = serverCPC.serverC()
        self.t1 = threading.Thread(target=self.server.create_server)
        self.t1.daemon = True
        self.t1.start()
        self.server_createBu["state"] = "disabled"
        self.server_destroyBu["state"] = "normal"
        
    def stop_server(self):
        self.server_destroyBu["state"] = "disabled"
        self.server_createBu["state"] = "normal"
        self.server.stop_server()
        self.server = None
GUI()
