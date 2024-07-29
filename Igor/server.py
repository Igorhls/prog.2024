import socket

# Define o endereço IP e a porta do servidor
IP = '10.25.3.154'
PORT = 5000

# Cria um socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associa o socket ao endereço IP e porta do servidor
sock.bind((IP, PORT))

print(f"Servidor UDP iniciado em {IP}:{PORT}")

# Dicionário para armazenar os clientes conectados
clientes = {}

while True:
    # Recebe os dados e o endereço do cliente
    data, address = sock.recvfrom(1024)
    
    # Registra o cliente no dicionário
    clientes[address] = data.decode()
    
    # Propaga a mensagem recebida a todos os outros clientes
    for client_address in clientes:
        if client_address != address:
            sock.sendto(data, client_address)

    # Envia uma resposta ao cliente
    response = "Olá, cliente!"
    sock.sendto(response.encode(), address)
