import socket
import os

# Define o diretório onde os arquivos estão localizados
diretorio_arquivos = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'arquivos')

def listar_arquivos():
    return os.listdir(diretorio_arquivos)

def enviar_arquivo(sock, cliente, caminho, posicao_inicial):
    with open(caminho, 'rb') as f:
        f.seek(posicao_inicial)
        while True:
            dados = f.read(1024)
            if not dados:
                break
            sock.sendall(dados)

def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('127.0.0.1', 1234))
    servidor.listen(5)
    print("Servidor esperando conexões...")

    while True:
        cliente, endereco = servidor.accept()
        print(f"Conexão estabelecida com {endereco}")

        try:
            mensagem = cliente.recv(1024).decode()
            comando, *args = mensagem.split()

            if comando == 'LIST':
                arquivos = listar_arquivos()
                resposta = 'LIST_OK ' + ','.join(arquivos)
                cliente.sendall(resposta.encode())

            elif comando == 'GET':
                nome_arquivo = args[0]
                posicao_inicial = int(args[1]) if len(args) > 1 else 0
                caminho_arquivo = os.path.join(diretorio_arquivos, nome_arquivo)

                if not os.path.isfile(caminho_arquivo):
                    cliente.sendall('ERROR 1'.encode())
                elif posicao_inicial < 0 or posicao_inicial > os.path.getsize(caminho_arquivo):
                    cliente.sendall('ERROR 2'.encode())
                else:
                    tamanho_arquivo = os.path.getsize(caminho_arquivo) - posicao_inicial
                    cliente.sendall(f'FILE_OK {tamanho_arquivo}'.encode())
                    enviar_arquivo(cliente, caminho_arquivo, posicao_inicial)

            else:
                cliente.sendall('ERROR 3'.encode())
        except Exception as e:
            print(f"Erro: {e}")
            cliente.sendall('ERROR 3'.encode())

        cliente.close()

if __name__ == "__main__":
    main()
