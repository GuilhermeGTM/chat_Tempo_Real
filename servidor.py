import socket
import threading

# Endereço IP e porta onde o servidor vai escutar conexões
HOST = '127.0.0.1'  # Localhost (apenas conexões locais)
PORT = 55555        # Porta escolhida para o servidor

# Cria o socket do servidor usando IPv4 (AF_INET) e TCP (SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associa o socket ao endereço e porta definidos
server.bind((HOST, PORT))

# Coloca o servidor em modo de escuta, pronto para aceitar conexões
server.listen()

# Dicionário que armazena as salas e os clientes conectados em cada uma
salas = {}

# Função que envia uma mensagem para todos os clientes de uma sala
def broadcast(sala, mensagem):
    for i in salas[sala]:  # Itera sobre todos os clientes da sala
        if isinstance(mensagem, str):  # Se a mensagem for string, codifica para bytes
            mensagem = mensagem.encode()
        i.send(mensagem)  # Envia a mensagem para o cliente

# Função que escuta mensagens de um cliente e retransmite para a sala
def enviarMensagem(nome, sala, client):
    while True:
        mensagem = client.recv(1024)  # Recebe até 1024 bytes do cliente
        mensagem = f"{nome}: {mensagem.decode()}\n"  # Formata a mensagem com o nome do remetente
        broadcast(sala, mensagem)  # Envia a mensagem para todos da sala

# Loop principal do servidor: aceita conexões de clientes
while True:
    client, addr = server.accept()  # Aceita uma nova conexão
    client.send(b'SALA')            # Solicita ao cliente que envie o nome da sala
    sala = client.recv(1024).decode()  # Recebe o nome da sala
    nome = client.recv(1024).decode()  # Recebe o nome do usuário

    # Se a sala ainda não existe, cria uma nova lista para ela
    if sala not in salas.keys():
        salas[sala] = []

    # Adiciona o cliente à sala correspondente
    salas[sala].append(client)

    # Exibe no terminal que o cliente se conectou
    print(f'{nome} se conectou na sala {sala}! INFO {addr}')

    # Notifica os outros participantes da sala que o novo cliente entrou
    broadcast(sala, f'{nome}: Entrou na sala!\n')

    # Cria uma nova thread para escutar as mensagens desse cliente
    thread = threading.Thread(target=enviarMensagem, args=(nome, sala, client))
    thread.start()
