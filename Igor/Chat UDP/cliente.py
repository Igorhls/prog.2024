import socket

# Define o endereço IP e a porta do servidor
host = '10.24.20.174'
port = 5000

# Cria um socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Envia uma mensagem para o servidor
message = input("Digite a mensagem para enviar ao servidor: ")
client_socket.sendto(message.encode(), (host, port))

# Recebe a resposta do servidor
data, server_address = client_socket.recvfrom(1024)
print('Resposta do servidor:', data.decode())

# Fecha o socket do cliente
client_socket.close()
