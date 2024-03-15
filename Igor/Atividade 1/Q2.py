import time
import hashlib

def findNonce(dataToHash, bitsToBeZero):
    nonce = 0
    start_time = time.time()
    
    while True:
        # Converter nonce em 4 bytes
        nonce_bytes = nonce.to_bytes(4, 'big')
        
        # Concatenar nonce com dataToHash
        data = nonce_bytes + dataToHash
        
        # Calcular o hash
        hash_result = hashlib.sha256(data).hexdigest()
        
        # Verificar se o hash possui o número necessário de zeros iniciais
        if hash_result.startswith('0' * bitsToBeZero):
            end_time = time.time()
            elapsed_time = end_time - start_time
            return nonce, elapsed_time
        
        nonce += 1

# Definir os dados e bitsToBeZero para cada linha na tabela
table_data = [
    (b"Esse e facil", 8),
    (b"Esse e facil", 10),
    (b"Esse e facil", 15),
    (b"Texto maior muda o tempo?", 8),
    (b"Texto maior muda o tempo?", 10),
    (b"Texto maior muda o tempo?", 15),
    (b"E possivel calcular esse?", 18),
    (b"E possivel calcular esse?", 19),
    (b"E possivel calcular esse?", 20)
]

# Preencher a tabela
table = []
for data, bits in table_data:
    nonce, elapsed_time = findNonce(data, bits)
    table.append((data.decode(), bits, nonce, elapsed_time))

# Escrever a tabela em um arquivo
with open('/home/igorhls/code/prog.2024/Igor/Atividade 1/tabela.txt', 'w') as file:
    file.write("Texto a validar\t\tBits em zero\tNonce\tTempo (em s)\n")
    for row in table:
        file.write(f"{row[0]}\t\t{row[1]}\t\t{row[2]}\t{row[3]}\n")

print("Tabela gerada com sucesso!")
