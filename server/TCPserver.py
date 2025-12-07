from socket import *
import os
import ssl
import threading

# Configurações de Porta
PORT_TCP = int(os.environ.get('SERVER_PORT', 12000))
PORT_TLS = PORT_TCP + 1  # 12001


# Estratégia: abrir dois servidores em threads diferentes, um para conexões tcp e outro para conexões não-tcp

def start_tcp_server():

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', PORT_TCP))
    serverSocket.listen(1)

    print(f"[TCP] Ouvindo na porta {PORT_TCP} (Texto Claro)...")

    while True:
        conn, addr = serverSocket.accept()
        print(f"[TCP] Conexão de {addr}")
        try:
            while True:
                data = conn.recv(1024)
                if not data: break
                print(f"[TCP Recebido]: {data.decode(errors='ignore')}")
        finally:
            conn.close()

def start_tls_server():
    
    # Configura SSL
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
    
    # Criando sockets
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', PORT_TLS))
    serverSocket.listen(1)
    print(f"[TLS] Ouvindo na porta {PORT_TLS} (Criptografado)...")

    while True:
        conn, addr = serverSocket.accept()
        try:
            # Embrulha o socket em TLS
            conn_ssl = context.wrap_socket(conn, server_side=True)
            print(f"[TLS] Conexão Segura de {addr}")
            
            while True:
                data = conn_ssl.recv(1024)
                if not data: break
                print(f"[TLS Recebido]: {data.decode(errors='ignore')}")
        except Exception as e:
            print(f"[TLS Erro]: {e}")
        finally:
            try:
                conn_ssl.close()
            except:
                pass

# Inicia as duas threads
if __name__ == "__main__":
    t1 = threading.Thread(target=start_tcp_server)
    t2 = threading.Thread(target=start_tls_server)
    
    t1.start()
    t2.start()