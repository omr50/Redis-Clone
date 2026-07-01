from Key_Store import get, set, keyStore
from threading import timer
from timer_callbacks import expireKey
from threading import Timer

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
                        expiryTime = int(command[i + 1])
                        set(command[1], command[2])
                        Timer(expiryTime, expireKey, args=[expiryTime])
                        return "OK"
            else: 
                return "Incorrectly formatted: missing arguments"
        if "EX" == command[3]:

    set(command[1], command[2])
    return "OK" 

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