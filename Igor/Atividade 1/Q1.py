import os

def xor_encrypt(source_file, password, dest_file):
    try:
        # Verifica se o arquivo de destino já existe
        if os.path.exists(dest_file):
            raise FileExistsError("O arquivo de destino já existe")

        # Abre o arquivo de origem em modo binário
        with open(source_file, 'rb') as src_file:
            # Abre o arquivo de destino em modo binário
            with open(dest_file, 'wb') as dest_file:
                # Inicializa o índice da senha
                password_index = 0

                # Lê o arquivo de origem byte a byte
                byte = src_file.read(1)
                while byte:
                    # Obtém o valor ASCII do caractere atual da senha
                    password_byte = ord(password[password_index])

                    # Realiza a operação XOR no byte
                    encrypted_byte = bytes([byte[0] ^ password_byte])

                    # Escreve o byte criptografado no arquivo de destino
                    dest_file.write(encrypted_byte)

                    # Atualiza o índice da senha
                    password_index = (password_index + 1) % len(password)

                    # Lê o próximo byte do arquivo de origem
                    byte = src_file.read(1)

        print("Criptografia concluída com sucesso")

    except FileNotFoundError:
        print("Arquivo de origem não encontrado")
    except FileExistsError:
        print("O arquivo de destino já existe")

# Exemplo de uso
source_file = input("Digite o nome do arquivo de origem: ")
password = input("Digite a senha: ")
dest_file = input("Digite o nome do arquivo de destino: ")

xor_encrypt(source_file, password, dest_file)
