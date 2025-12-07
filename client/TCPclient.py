from socket import *
import os
import ssl
import time

serverName = 'tcp-server'
PORT_TCP = int(os.environ.get('SERVER_PORT', 12000))
PORT_TLS = PORT_TCP + 1 
## Truncar sslkeylogfile
f = open('/captures/tls.log', 'w')
f.close()

#####################################################################
mensagem = "No one begins as a pro. Pay the beginner tax with pride."
#####################################################################

def normal_tcp():
    print(f"\n--- Iniciando Envio TCP NORMAL (Porta {PORT_TCP}) ---")

    clientSocket = socket(AF_INET, SOCK_STREAM)

    try:
        clientSocket.connect((serverName, PORT_TCP))
        
        # Envia várias vezes 
        for i in range(5):
            payload = f"{mensagem}\n"
            clientSocket.send(payload.encode())
            print(f"Enviado: {payload.strip()}")
            
    except Exception as e:
        print(f"Erro TCP: {e}")
    finally:
        clientSocket.close()
        
    print("--- Fim TCP Normal ---\n")



def tls_tcp():
    print(f"--- Iniciando Envio TLS (Porta {PORT_TLS}) ---")
    
    context = ssl.create_default_context()
    # Carrega certificado como confiável
    context.load_verify_locations('/opt/server.crt')

    raw_socket = socket(AF_INET, SOCK_STREAM)
    
    try:
        # Cria a conexão segura
        tls_conn = context.wrap_socket(raw_socket, server_hostname=serverName)
        tls_conn.connect((serverName, PORT_TLS))
        print(f"Handshake TLS concluído. Cifra: {tls_conn.cipher()}")

        # Envia várias vezes 
        for i in range(5):
            payload = f"{mensagem}\n"
            tls_conn.sendall(payload.encode())
            print(f"Enviado (Criptografado): {payload.strip()}")
            
    except Exception as e:
        print(f"Erro TLS: {e}")
    finally:
        # Fechar o socket TLS corretamente
        try:
            tls_conn.close()
        except:
            pass
    print("--- Fim TLS ---")



# Execução Principal
if __name__ == "__main__":
    # Pausa para garantir que o servidor subiu
    time.sleep(2) 
    
    
    normal_tcp()

    # Pausa para melhor separação dos fluxos no Wireshark
    time.sleep(2) 
    
    tls_tcp()