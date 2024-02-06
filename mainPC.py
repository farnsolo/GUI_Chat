import tkinter as tk
import clientCPC
import serverCPC
import threading
import queue

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
        self.client = tk.Button(self.root, text="Client", font=("Ariel", 18), command=self.create_client)
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
        
    def create_client(self):
        # Multiple client_GUI objects created and none destroyed need to fix
        self.client = clientCPC.client_GUI()
        
    def stop_server(self):
        self.server_destroyBu["state"] = "disabled"
        self.server_createBu["state"] = "normal"
        self.server.stop_server()
        self.server = None
GUI()
