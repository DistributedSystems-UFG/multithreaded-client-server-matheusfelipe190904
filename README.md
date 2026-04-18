# Cliente-Servidor Multithread (ASR 05)

Sistema cliente-servidor em Python com suporte a múltiplas threads, baseado na implementação da ASR 04.

## Autor
Matheus Felipe de Borba Machado Vieira

---

## Descrição do sistema

O sistema implementa uma calculadora remota via sockets TCP, onde o cliente envia operações matemáticas e o servidor processa e retorna os resultados. Esta versão estende a ASR 04 com suporte a multithreading tanto no servidor quanto no cliente, além de geração automática de requisições para fins de experimento de desempenho.

---

## Arquivos

| Arquivo | Descrição |
|---|---|
| `constCS.py` | Configurações compartilhadas (HOST e PORT) |
| `server.py` | Servidor single-thread original (ASR 04) |
| `server_mt.py` | Servidor multithread — cria uma thread por cliente conectado |
| `client.py` | Cliente interativo original (ASR 04) |
| `client_auto.py` | Cliente sequencial com geração automática de requisições |
| `client_mt.py` | Cliente multithread com geração automática de requisições |

---

## Operações disponíveis

- `add` — soma
- `sub` — subtração
- `mul` — multiplicação
- `div` — divisão (com tratamento de divisão por zero)
- `pow` — potência

### Formato das requisições

```
operacao;valor1;valor2
```

Exemplo: `add;10;5` → resposta: `15.0`

---

## Como executar

### Configuração

No arquivo `constCS.py`, defina o IP do servidor:

```python
HOST = '172.31.95.98'  # IP privado da instância servidora na AWS
PORT = 5678
```

### Versão single-thread (original)

```bash
# Terminal 1 — servidor
python3 server.py

# Terminal 2 — cliente interativo
python3 client.py
```

### Versão servidor multithread + cliente sequencial automático

```bash
# Terminal 1 — servidor
python3 server_mt.py

# Terminal 2 — cliente
python3 client_auto.py
```

### Versão totalmente multithread

```bash
# Terminal 1 — servidor
python3 server_mt.py

# Terminal 2 — cliente
python3 client_mt.py
```

---

## Detalhes de implementação

### Servidor multithread (`server_mt.py`)

Para cada cliente que conecta, o servidor cria uma nova `threading.Thread` que executa a função `handle_client`. O loop principal continua aceitando novas conexões enquanto as threads ativas processam as requisições em paralelo. Threads são marcadas como `daemon=True` para encerrar junto com o processo principal.

### Cliente multithread (`client_mt.py`)

Cada requisição é enviada por uma thread independente, com uma conexão TCP própria. Um `threading.Semaphore(20)` limita a concorrência máxima em 20 threads simultâneas, evitando sobrecarga nas instâncias. Um `threading.Lock` protege a lista de resultados contra condições de corrida.

### Geração automática de requisições

Ambos os clientes automáticos (`client_auto.py` e `client_mt.py`) utilizam `random.choice` e `random.uniform` para gerar operações e valores aleatórios. O número de requisições é configurável pela variável `NUM_REQUISICOES`.

---

## Ambiente de execução

- **Plataforma:** AWS Academy — instâncias EC2
- **Servidor:** instância `Server` (t2.small) — IP privado `172.31.95.98`
- **Cliente:** instância `pear1` (t3.micro) — IP público `98.81.255.152`
- **Região:** us-east-1d
- **Linguagem:** Python 3
