from socket import *
from constCS import *
import threading
import random
import time

NUM_REQUISICOES = 200
OPERACOES = ["add", "sub", "mul", "div", "pow"]

resultados = []
lock = threading.Lock()

def gerar_requisicao():
    op = random.choice(OPERACOES)
    v1 = round(random.uniform(1, 1000), 2)
    # Para div e pow, evitar valores problemáticos
    if op == "div":
        v2 = round(random.uniform(1, 100), 2)
    elif op == "pow":
        v2 = round(random.uniform(1, 5), 2)
    else:
        v2 = round(random.uniform(1, 1000), 2)
    return f"{op};{v1};{v2}"

def enviar_requisicao(req_id):
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((HOST, PORT))
        msg = gerar_requisicao()
        s.send(msg.encode())
        data = s.recv(1024)
        s.close()
        with lock:
            resultados.append((req_id, msg, data.decode()))
    except Exception as e:
        with lock:
            resultados.append((req_id, "ERRO", str(e)))

print(f"Cliente multithread: enviando {NUM_REQUISICOES} requisições em paralelo...")
inicio = time.time()

threads = []
for i in range(NUM_REQUISICOES):
    t = threading.Thread(target=enviar_requisicao, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

fim = time.time()
tempo_total = fim - inicio

print(f"\n=== RESULTADO ===")
print(f"Requisições enviadas : {NUM_REQUISICOES}")
print(f"Requisições concluídas: {len(resultados)}")
print(f"Tempo total          : {tempo_total:.4f} segundos")
print(f"Req/segundo          : {NUM_REQUISICOES / tempo_total:.2f}")

# Mostrar algumas amostras
print("\nAmostras dos resultados:")
for req_id, msg, resp in sorted(resultados)[:5]:
    print(f"  [{req_id}] {msg} => {resp}")
