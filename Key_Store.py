keyStore = {}


def get(key):
    if key in keyStore:
        return keyStore[key]
    return None

def set(key, value):
    keyStore[key] = value
    return "OK"

