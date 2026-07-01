from Key_Store import keyStore

def expireKey(key):
    if key in keyStore:
        print("found and removed key")
        del keyStore[key]
    print("DELETED")
