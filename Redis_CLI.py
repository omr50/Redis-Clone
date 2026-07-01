# TCP Client
import socket
from RESP import encodeArray, parse, encode

HOST = "127.0.0.1"
PORT = 6379

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST,PORT))
    while True:
        message = input("> ")

        if message.lower() == "quit":
            break
        
        messageArray = message.split()
        respArray = encode(messageArray)
        sock.sendall(respArray.encode())
        response = sock.recv(4096)
        
        print(parse(response.decode()))