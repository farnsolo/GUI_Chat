import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import serverListOption
import backendInterface
import serverCPC
import threading
import queue

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.label = tk.Label(self.root, text="Welcome to GUI chat", font=("Ariel", 18))
        self.label.pack()        
        self.server_createBu = tk.Button(self.root, text="Create server", font=("Ariel",16), command=self.create_server)
        self.server_createBu.pack()
        self.server_destroyBu = tk.Button(self.root, text="Destroy server", font=("Ariel", 16), command=self.stop_server)
        self.server_destroyBu.pack()
        self.client = tk.Button(self.root, text="Client", font=("Ariel", 18), command=self.create_client)
        self.client.pack()
        
        self.serverHeader = tk.Label(self.root, text="Your Server name:", font=("Ariel", 18))
        self.serverHeader.pack()
        
        self.serverLabel = tk.Label(self.root, text=":", font=("Ariel", 11))
        self.serverLabel.pack()
        
        self.usernameHeader = tk.Label(self.root, text="Your Username:", font=("Ariel", 18))
        self.usernameHeader.pack()
        self.usernameLabel = tk.Label(self.root, text=":", font=("Ariel", 11))
        self.usernameLabel.pack()
        
        self.username = self.input_Name("Enter username")
        self.usernameLabel.config(text=self.username)
        self.server_destroyBu["state"] = "disabled"
        self.server_createBu["state"] = "normal"
        self.root.protocol("WM_DELETE_WINDOW",self.close_main)
        self.message_queue = queue.Queue()
        self.root.mainloop()
        
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
    # Name must be more than 5 characters but less than 31
    def input_Name(self, stringa):
        name = simpledialog.askstring("", stringa)
        while(name == None or len(name) < 5 or len(name) > 30):
            name = simpledialog.askstring("", stringa)
        return name
    
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
        
    def create_server(self):
        name = self.input_Name("Enter server name")
        if(name == None):
            messagebox.showinfo("Server Creation Aborted", "Invalid server name")
        else:
            try:
                self.server = serverCPC.serverC(name)
                self.t1 = threading.Thread(target=self.server.create_server)
                self.t1.daemon = True
                self.t1.start()
                self.server_createBu["state"] = "disabled"
                self.server_destroyBu["state"] = "normal"
                self.serverLabel.config(text = name)
            except OSError as e:
                if e.errno == 10061:
                    messagebox.showerror("Error","Resolution server is offline, can not create server")
            
# -----------------------------------------------------------------------------------------------------------------------------------------------------------
        
    def create_client(self):
        # Multiple client_GUI objects created and none destroyed need to fix
        try:
            serverListOption.Main(self.username)
        except OSError as e:
                if e.errno == 10061:
                    messagebox.showerror("Error","Resolution server is offline, can not view servers")
        except Exception as e:
            messagebox.showerror("Error", e)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------

    def stop_server(self):
        self.server_destroyBu["state"] = "disabled"
        self.server_createBu["state"] = "normal"
        backendInterface.removeServer(self.server.NAME)
        self.serverLabel.config(text="")
        self.server.stop_server()
        del self.server
        
    
    def close_main(self):
        ans  = messagebox.askyesno(title="Exit", message=f"Do you want to exit app?")
        if ans and self.server_createBu["state"] == "disabled":
            self.stop_server()
        if ans:
            self.root.destroy()
            
GUI()
