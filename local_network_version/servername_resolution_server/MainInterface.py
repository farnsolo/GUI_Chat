from Backend import Dict
def getIP(name):
    # Return name from given IP
    return Dict[name]
    
def createPair(key, value):
    # set name for ip
    # create new key-value pair
    Dict[key] = value

def getServerNames():
    return list(Dict.keys())

# Time complexity O(1)
def removeServer(key):
    del Dict[key]
