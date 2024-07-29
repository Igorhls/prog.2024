import socket

# Define o endereço IP e a porta do servidor
server_ip = '10.25.3.154'
server_port = 50000

# Cria um socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Envia uma mensagem para o servidor
message = input("Digite a mensagem para enviar ao servidor: ")
client_socket.sendto(message.encode(), (server_ip, server_port))

# Recebe a resposta do servidor
data, server_address = client_socket.recvfrom(1024)
print('Resposta do servidor:', data.decode())

# Fecha o socket do cliente
client_socket.close()
