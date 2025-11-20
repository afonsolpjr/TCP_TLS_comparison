from socket import *
import os
serverName = 'tcp-server'
serverPort = int(os.environ.get('SERVER_PORT'))
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))


buffer = b''
for i in range(0,100):
    buffer += str.encode("Esta é a {}ª mensagem teste\n".format(i))

clientSocket.send(buffer)

clientSocket.close()