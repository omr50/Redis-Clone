from Key_Store import get, set, keyStore
from timer_callbacks import expireKey
from threading import Timer
import time
from RESP import encode
import json
import os

def handlePing(command):
    return "PONG"

def handleEcho(command):
    if command[1][0] == '"' and command[1][-1] == '"':
        return command[1][1:-1] 
    return command[1]

def executeCommand(command):
    if command[0] in commands:
        return commands[command[0]](command)

def handleSet(command):
    conflict = 0
    argConflict = ["EX", "PX", "EXAT", "PXAT"]
    for arg in command:
        if arg in argConflict:
            conflict += 1
        if conflict > 1:
            return "Contains conflicting arguments"
    if len(command) < 3:
        return "Invalid command: try set <key> <val> <options>"
    if len(command) == 3:
        set(command[1], command[2])
        return "OK"
    elif len(command) > 3:
        args = command[3:]
        if "EX" in args:
            if len(command) >= 5:
                for i in range(len(args)):
                    if i == len(args) - 1:
                        return "Incorrectly formatted: missing arguments"
                    if args[i] == "EX":
                        key, value = command[1], command[2]
                        expiryTime = int(args[i + 1])
                        set(key, value)
                        Timer(expiryTime, expireKey, args=[key]).start()
                        return "OK"
        elif "PX" in args:
            if len(command) >= 5:
                for i in range(len(args)):
                    if i == len(args) - 1:
                        return "Incorrectly formatted: missing arguments"
                    if args[i] == "PX":
                        key, value = command[1], command[2]
                        expiryTime = int(args[i + 1])
                        set(key, value)
                        Timer(expiryTime / 1000, expireKey, args=[key]).start()
                        return "OK"
        elif "EXAT" in args:
            if len(command) >= 5:
                for i in range(len(args)):
                    if i == len(args) - 1:
                        return "Incorrectly formatted: missing arguments"
                    if args[i] == "EXAT":
                        key, value = command[1], command[2]
                        expiryTime =  int(args[i + 1]) - int(time.time())
                        if expiryTime < 0:
                            return "Cannot set expire time in past"
                        set(key, value)
                        Timer(expiryTime, expireKey, args=[key]).start()
                        return "OK"
        elif "PXAT" in args:
            if len(command) >= 5:
                for i in range(len(args)):
                    if i == len(args) - 1:
                        return "Incorrectly formatted: missing arguments"
                    if args[i] == "PXAT":
                        key, value = command[1], command[2]
                        expiryTime =  int(args[i + 1]) / 1000 - int(time.time())
                        print(expiryTime)
                        if expiryTime < 0:
                            return "Cannot set expire time in past"
                        set(key, value)
                        Timer(expiryTime, expireKey, args=[key]).start()
                        return "OK"

            else: 
                return "Incorrectly formatted: missing arguments"


def handleGet(command):
    if len(command) != 2:
        return "Invalid command: try get <key>"

    val = get(command[1])
    if val:
        return val
    return "Value not found"

def handleExists(command):
    if len(command) == 1:
        return "No keys provided: try EXISTS <keys....>"
    count = 0
    for key in command[1:]:
        if key in keyStore:
            count += 1
    return "(integer) " + str(count)

def handleDel(command):
    if len(command) == 1:
        return "No keys provided: try DEL <keys....>"
    count = 0
    for key in command[1:]:
        if key in keyStore:
            if key in keyStore:
                del keyStore[key]
                count += 1
    return "(integer)" + str(count)

def handleIncr(command):
    if len(command) != 2:
        return "Incorrect args: try INCR <key>"
    key = command[1]
    if key in keyStore:
        val = keyStore[key]
        try:
            num = int(val)
            num += 1
            keyStore[key] = str(num)
            return '"' + str(num) + '"'
        except ValueError:
            return "Value is not an integer"
    return "Key not found"
 
def handleDecr(command):
    if len(command) != 2:
        return "Incorrect args: try INCR <key>"
    key = command[1]
    if key in keyStore:
        val = keyStore[key]
        try:
            num = int(val)
            num -= 1
            keyStore[key] = str(num)
            return '"' + str(num) + '"'
        except ValueError:
            return "Value is not an integer"
    return "Key not found"

def handleLpush(command):
    if len(command) < 3:
        return "malformed command: try LPUSH <key> [element ...]"
    
    key = command[1]
    elements = command[2:]
    if key not in keyStore:
        keyStore[key] = []
    arr = keyStore[key]
    for elem in elements:
        arr = [elem] + arr
    keyStore[key] = arr
    return "(integer) " + str(len(elements))

def handleRpush(command):
    if len(command) < 3:
        return "malformed command: try RPUSH <key> [element ...]"
    
    key = command[1]
    elements = command[2:]
    if key not in keyStore:
        keyStore[key] = []
    arr = keyStore[key]
    for elem in elements:
        arr.append(elem)
    keyStore[key] = arr
    return "(integer) " + str(len(elements))

def handleSave(command):
    if len(command) != 1:
        return "incorrect command: try SAVE"

    # timestamp = time.time()
    # saveFileName = "snapshot_" + str(timestamp)
    saveFileName = "./snapshots/snapshot"
    with open(saveFileName, 'w') as snapshot:
        json.dump(keyStore, snapshot)
    return "Saved to file: " + saveFileName

def handleLoad():
    if not os.path.isfile("./snapshots/snapshot"):
        print("no snapshot, empty keyStore initialized")
        return
    with open("./snapshots/snapshot", 'r') as snapshot:
        data = json.load(snapshot)
        keyStore.clear()
        keyStore.update(data)
        print("fully seeded keyStore")
        print(keyStore)



    return "seeded keystore"
commands = {
    'PING': handlePing,
    'ECHO': handleEcho,
    'SET': handleSet,
    'GET': handleGet,
    'EXISTS': handleExists,
    'DEL': handleDel,
    'INCR': handleIncr,
    'DECR': handleDecr,
    'LPUSH': handleLpush,
    'RPUSH': handleRpush,
    'SAVE': handleSave
}