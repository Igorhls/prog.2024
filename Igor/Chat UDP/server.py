import socket

# Define o endereço IP e a porta do servidor
IP = '10.24.20.174'
PORT = 5000

# Cria um socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associa o socket ao endereço IP e porta do servidor
sock.bind((IP, PORT))

print(f"Servidor UDP iniciado em {IP}:{PORT}")

while True:
    # Recebe os dados e o endereço do cliente
    data, address = sock.recvfrom(1024)

    # Exibe a mensagem recebida
    print(f"Mensagem recebida do cliente {address}: {data.decode()}")

    # Processa os dados recebidos
    # ...

    # Envia uma resposta ao cliente
    response = "Olá, cliente!"
    sock.sendto(response.encode(), address)
