from hashlib import sha256
from time import time
from struct import pack

# Definindo a função findnounce que realiza a mineração de nonce
def findnounce(data_To_Hash, bitsToBeZero, start_nonce=0):
    # Mensagem de início da busca por um hash com o número de zeros especificado
    print(f"Iniciando a busca por um hash de '{data_To_Hash}' que inicia com {bitsToBeZero} zeros ")

    # Registrando o tempo de início
    timestart = time()

    # Loop infinito para encontrar o nonce adequado
    while True:
        # Inicializando um objeto de hash SHA-256
        hashbinario = sha256()

        # Atualizando o hash com o nonce atual e a string data_To_Hash
        hashbinario.update(pack("<i", start_nonce) + data_To_Hash.encode("utf-8"))

        # Obtendo o valor hash binário
        hashbinario = hashbinario.digest()

        # Convertendo o hash binário para uma representação hexadecimal
        hashhexa = ''.join([f'{i:02x}' for i in hashbinario])

        # Convertendo o hash binário para uma representação de texto binário
        hashtextobinario = ''.join([f'{i:08b}' for i in hashbinario])

        # Verificando se o texto binário do hash começa com o número especificado de zeros
        if hashtextobinario.startswith("0"*bitsToBeZero):
            # Se a condição for atendida, o loop é interrompido
            break
        
        # Se não, incrementa o nonce e continua o loop
        start_nonce += 1

    # Calculando e exibindo o tempo decorrido, nonce e hash encontrado
    print(f"Minerando '{data_To_Hash}', bits em zero: {bitsToBeZero}, Nonce: {start_nonce}, demorou {time()-timestart:.2f} segundos.")
    print(f"Hash: {hashhexa}\n{'-'*40}")

# Chamando a função findnounce com diferentes entradas para observar o comportamento
findnounce("Esse é fácil", 8)
findnounce("Esse é fácil", 10)
findnounce("Esse é fácil", 15)
findnounce("Texto maior muda o tempo?", 8)
findnounce("Texto maior muda o tempo?", 10)
findnounce("Texto maior muda o tempo?", 15)
findnounce("É possível calcular esse?", 18)
findnounce("É possível calcular esse?", 19)
findnounce("É possível calcular esse?", 20)

# Abrindo o arquivo em modo de escrita
with open('tabela.txt', 'w') as file:
    # Escrevendo os resultados no arquivo
    file.write(f"{'-'*40}\n")
    file.write(f"{'Data To Hash': <30}{'Bits em Zero': <15}{'Nonce': <10}{'Tempo (s)': <15}{'Hash': <64}\n")
    file.write(f"{'-'*40}\n")
    
    # Chamando a função findnounce com diferentes entradas para observar o comportamento
    findnounce("Esse é fácil", 8)
    findnounce("Esse é fácil", 10)
    findnounce("Esse é fácil", 15)
    findnounce("Texto maior muda o tempo?", 8)
    findnounce("Texto maior muda o tempo?", 10)
    findnounce("Texto maior muda o tempo?", 15)
    findnounce("É possível calcular esse?", 18)
    findnounce("É possível calcular esse?", 19)
    findnounce("É possível calcular esse?", 20)
    
    # Escrevendo uma linha de separação no final do arquivo
    file.write(f"{'-'*40}\n")