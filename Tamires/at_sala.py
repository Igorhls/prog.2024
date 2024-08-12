import socket

HOST = "10.24.20.174"
PORT = 5000

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
m = "olá"

m = m.encode('utf-8')
print(m)

udp_socket.sendto(m, (HOST, PORT))
udp_socket.close()
