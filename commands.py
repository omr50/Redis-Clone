from Key_Store import get, set

def handlePing(command):
    return "PONG"

def handleEcho(command):
    return command[1:-1] 

def executeCommand(command):
    if command[0] in commands:
        return commands[command[0]](command)

def handleSet(command):
    set(command[1], command[2])

def handleGet(command):
    return get(command[1])

commands = {
    'PING': handlePing,
    'ECHO': handleEcho,
    'set': handleSet,
    'get': handleGet
}