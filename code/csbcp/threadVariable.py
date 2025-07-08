import threading

_innerVariables = threading.local()

def setUser_id(user_id):
    _innerVariables.user_id = user_id

def getUser_id():
    return int(getattr(_innerVariables, 'user_id', None))