from socket import *
import os
serverPort = int(os.environ.get('SERVER_PORT'))
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)


while True:
    connectionSocket, addr = serverSocket.accept()

    try:
        buffer = ""
        while True:
            sentence = connectionSocket.recv(512).decode()
            print(sentence)
            if not sentence:
                print("connection closed by {}.".format(addr))
                break
            
            buffer += sentence
    finally:
        print(sentence,flush=True)
        connectionSocket.close()