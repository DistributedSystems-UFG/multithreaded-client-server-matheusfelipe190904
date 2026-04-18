from socket import *
from constCS import *
import threading

def process_request(msg):
    try:
        parts = msg.split(";")
        op = parts[0]
        if op == "add":
            return str(float(parts[1]) + float(parts[2]))
        elif op == "sub":
            return str(float(parts[1]) - float(parts[2]))
        elif op == "mul":
            return str(float(parts[1]) * float(parts[2]))
        elif op == "div":
            if float(parts[2]) == 0:
                return "Erro: divisão por zero"
            return str(float(parts[1]) / float(parts[2]))
        elif op == "pow":
            return str(float(parts[1]) ** float(parts[2]))
        else:
            return "Erro: operação inválida"
    except:
        return "Erro no processamento"

def handle_client(conn, addr):
    print(f"[Thread {threading.current_thread().name}] Conectado com: {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        msg = data.decode()
        print(f"[Thread {threading.current_thread().name}] Recebido: {msg}")
        resposta = process_request(msg)
        conn.send(resposta.encode())
    conn.close()
    print(f"[Thread {threading.current_thread().name}] Conexão encerrada: {addr}")

s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(10)
print("Servidor multithread rodando...")

while True:
    conn, addr = s.accept()
    t = threading.Thread(target=handle_client, args=(conn, addr))
    t.daemon = True
    t.start()
    print(f"Thread iniciada: {t.name} | Threads ativas: {threading.active_count() - 1}")
