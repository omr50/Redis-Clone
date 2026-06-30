keyStore = {}


def get(key):
    return keyStore[key]

def set(key, value):
    keyStore[key] = value
    return "OK"

