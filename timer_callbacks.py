from threading import Timer 
from Key_Store import keyStore

def expireKey(key):
    if key in keyStore:
        del keyStore[key]
