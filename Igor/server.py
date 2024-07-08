import socket

# Define o endereço IP e a porta do servidor
IP = '10.25.3.154'
PORT = 5000

# Cria um socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associa o socket ao endereço IP e porta do servidor
sock.bind((IP, PORT))

print(f"Servidor UDP iniciado em {IP}:{PORT}")

# Remove o loop while True e o recvfrom
# Recebe os dados e o endereço do cliente
data, address = sock.recvfrom(1024)

# Processa os dados recebidos
# ...

# Envia uma resposta ao cliente
response = "Olá, cliente!"
sock.sendto(response.encode(), address)
