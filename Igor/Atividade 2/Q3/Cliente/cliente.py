import socket
import os

def listar_arquivos(sock):
    sock.sendall('LIST'.encode())
    resposta = sock.recv(4096).decode()
    if resposta.startswith('LIST_OK'):
        arquivos = resposta[8:].split(',')
        print("Arquivos disponíveis:")
        for arquivo in arquivos:
            print(f" - {arquivo}")
    else:
        print("Erro ao listar arquivos.")

def baixar_arquivo(sock, nome_arquivo, posicao_inicial=0):
    sock.sendall(f'GET {nome_arquivo} {posicao_inicial}'.encode())
    resposta = sock.recv(1024).decode()
    if resposta.startswith('FILE_OK'):
        tamanho_arquivo = int(resposta.split()[1])
        caminho = os.path.join('download', nome_arquivo)

        with open(caminho, 'wb') as f:
            recebido = 0
            while recebido < tamanho_arquivo:
                dados = sock.recv(1024)
                if not dados:
                    break
                f.write(dados)
                recebido += len(dados)
        
        print(f"Download concluído: {nome_arquivo}")
    elif resposta.startswith('ERROR 1'):
        print("Erro: Arquivo não encontrado.")
    elif resposta.startswith('ERROR 2'):
        print("Erro: Posição inicial inválida.")
    else:
        print("Erro desconhecido.")

def main():
    while True:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(('127.0.0.1', 1234))

        comando = input("Digite o comando (LIST, GET <arquivo>, SAIR): ").strip().split()
        if not comando:
            continue

        if comando[0] == 'LIST':
            listar_arquivos(cliente)
        elif comando[0] == 'GET':
            if len(comando) < 2:
                print("Uso: GET <nome_arquivo>")
                cliente.close()
                continue
            nome_arquivo = comando[1]
            posicao_inicial = int(comando[2]) if len(comando) > 2 else 0
            baixar_arquivo(cliente, nome_arquivo, posicao_inicial)
        elif comando[0] == 'SAIR':
            cliente.close()
            break
        else:
            print("Comando desconhecido.")
            cliente.close()

if __name__ == "__main__":
    main()
