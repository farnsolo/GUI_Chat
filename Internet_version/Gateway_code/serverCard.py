class serverCard():
    def __init__(self, conn):
        self.CONN = conn
        self.userDir = []
        
    def appendConn(self,conn):
        self.userDir.append(conn)
        
    def getServerConn(self):
        return self.CONN
    
    def getConnList(self):
        return self.userDir
    
    def removeConn(self, conn):
        self.userDir.remove(conn)