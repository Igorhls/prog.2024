import socket
import hashlib
import threading

class Servidor:
    def __init__(self, porta=31471):
        self.porta = porta
        self.transacoes = []
        self.clientes = []
        self.janela_validacao = 1000000

    def iniciar(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', self.porta))
        self.socket.listen(5)
        print(f'Servidor iniciado {self.porta}')

        threading.Thread(target=self.atender_clientes).start()

    def atender_clientes(self):
        while True:
            cliente, endereco = self.socket.accept()
            print(f'Cliente conectado com sucesso: {endereco}')
            self.clientes.append(cliente)
            threading.Thread(target=self.atender_cliente, args=(cliente,)).start()

    def atender_cliente(self, cliente):
        while True:
            mensagem = cliente.recv(1024)
            if not mensagem:
                break
            comando = mensagem.decode('utf-8')[0]
            if comando == 'G':
                self.enviar_transacao(cliente)
            elif comando == 'S':
                self.validar_nonce(cliente, mensagem)
        cliente.close()

    def enviar_transacao(self, cliente):
        if not self.transacoes:
            cliente.sendall(b'W')
            return
        transacao = self.transacoes.pop(0)
        num_transacao = len(self.transacoes)
        num_cliente = len(self.clientes)
        tam_janela = self.janela_validacao
        bits_zero = 4
        tam_transacao = len(transacao)
        mensagem = f'T {num_transacao:02x} {num_cliente:02x} {tam_janela:08x} {bits_zero:02x} {tam_transacao:08x} {transacao}'
        cliente.sendall(mensagem.encode('utf-8'))

    def validar_nonce(self, cliente, mensagem):
        num_transacao = int(mensagem[1:3], 16)
        nonce = mensagem[3:7]
        transacao = self.transacoes[num_transacao]
        hash = hashlib.sha256(nonce + transacao).hexdigest()
        if hash.startswith('0' * 4):
            self.enviar_validacao(cliente, num_transacao)
            self.notificar_clientes(num_transacao)
        else:
            cliente.sendall(f'R {num_transacao:02x}'.encode('utf-8'))

    def enviar_validacao(self, cliente, num_transacao):
        cliente.sendall(f'A {num_transacao:02x}'.encode('utf-8'))

    def notificar_clientes(self, num_transacao):
        for cliente in self.clientes:
            if cliente != self.clientes[0]:
                cliente.sendall(f'I {num_transacao:02x}'.encode('utf-8'))

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

if __name__ == '__main__':
    servidor = Servidor()
    servidor.iniciar()
    while True:
        transacao = input('Digite aqui uma transação: ')
        servidor.adicionar_transacao(transacao.encode('utf-8'))