import socket
import hashlib

class Cliente:
    def __init__(self, endereco='localhost', porta=31471):
        self.endereco = endereco
        self.porta = porta
        self.nome = input('Digite o teu nome: ')

    def conectar(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.endereco, self.porta))
        print(f'Conectado ao servidor com sucesso {self.endereco}:{self.porta}')

    def enviar_pedido(self):
        mensagem = f'G {self.nome}'
        self.socket.sendall(mensagem.encode('utf-8'))

    def receber_transacao(self):
        mensagem = self.socket.recv(1024)
        if mensagem.startswith(b'T'):
            num_transacao = int(mensagem[1:3], 16)
            num_cliente = int(mensagem[3:5], 16)
            tam_janela = int(mensagem[5:13], 16)
            bits_zero = int(mensagem[13:15], 16)
            tam_transacao = int(mensagem[15:23], 16)
            transacao = mensagem[23:].decode('utf-8')
            print(f'Recebeu transação {num_transacao} de {num_cliente} clientes')
            self.procurar_nonce(transacao, num_transacao, tam_janela, bits_zero)
        elif mensagem.startswith(b'W'):
            print('Não há transações disponíveis')
        elif mensagem.startswith(b'A'):
            print('Nonce válido!')
        elif mensagem.startswith(b'R'):
            print('Nonce inválido')
        elif mensagem.startswith(b'I'):
            print('Nonce encontrado em outro cliente')

    def procurar_nonce(self, transacao, num_transacao, tam_janela, bits_zero):
        for nonce in range(tam_janela):
            hash = hashlib.sha256(f'{nonce:08x}{transacao}'.encode('utf-8')).hexdigest()
            if hash.startswith('0' * bits_zero):
                print(f'Nonce encontrado: {nonce:08x}')
                self.enviar_nonce(num_transacao, nonce)
                break

    def enviar_nonce(self, num_transacao, nonce):
        mensagem = f'S {num_transacao:02x} {nonce:08x}'
        self.socket.sendall(mensagem.encode('utf-8'))

if __name__ == '__main__':
    cliente = Cliente()
    cliente.conectar()
    cliente.enviar_pedido()
    while True:
        cliente.receber_transacao()