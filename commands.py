from Key_Store import get, set, keyStore
from timer_callbacks import expireKey
from threading import Timer
import time

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

commands = {
    'PING': handlePing,
    'ECHO': handleEcho,
    'SET': handleSet,
    'GET': handleGet
}