from socket import *
from constCS import *
import random
import time

NUM_REQUISICOES = 200
OPERACOES = ["add", "sub", "mul", "div", "pow"]

def gerar_requisicao():
    op = random.choice(OPERACOES)
    v1 = round(random.uniform(1, 1000), 2)
    if op == "div":
        v2 = round(random.uniform(1, 100), 2)
    elif op == "pow":
        v2 = round(random.uniform(1, 5), 2)
    else:
        v2 = round(random.uniform(1, 1000), 2)
    return f"{op};{v1};{v2}"

print(f"Cliente sequencial automático: enviando {NUM_REQUISICOES} requisições...")
inicio = time.time()

resultados = []
for i in range(NUM_REQUISICOES):
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((HOST, PORT))
        msg = gerar_requisicao()
        s.send(msg.encode())
        data = s.recv(1024)
        s.close()
        resultados.append((i, msg, data.decode()))
    except Exception as e:
        resultados.append((i, "ERRO", str(e)))

fim = time.time()
tempo_total = fim - inicio

print(f"\n=== RESULTADO ===")
print(f"Requisições enviadas  : {NUM_REQUISICOES}")
print(f"Requisições concluídas: {len(resultados)}")
print(f"Tempo total           : {tempo_total:.4f} segundos")
print(f"Req/segundo           : {NUM_REQUISICOES / tempo_total:.2f}")

print("\nAmostras dos resultados:")
for req_id, msg, resp in resultados[:5]:
    print(f"  [{req_id}] {msg} => {resp}")
