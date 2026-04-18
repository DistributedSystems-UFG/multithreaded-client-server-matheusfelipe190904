from socket import *
from constCS import *

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))

print("Conectado ao servidor!")

while True:
    print("\nOperações disponíveis:")
    print("add, sub, mul, div, pow")
    print("Digite 'sair' para encerrar")

    op = input("Operação: ")

    if op == "sair":
        break

    v1 = input("Valor 1: ")
    v2 = input("Valor 2: ")

    msg = f"{op};{v1};{v2}"
    s.send(msg.encode())

    data = s.recv(1024)
    print("Resultado:", data.decode())

s.close()
