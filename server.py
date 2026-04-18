from socket import *
from constCS import *

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

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

print("Servidor rodando...")

while True:
    conn, addr = s.accept()
    print("Conectado com:", addr)

    while True:
        data = conn.recv(1024)
        if not data:
            break

        msg = data.decode()
        print("Recebido:", msg)

        resposta = process_request(msg)

        conn.send(resposta.encode())

    conn.close()
