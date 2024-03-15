import struct
import socket

# Define a função 'read_pcap_file' para ler e analisar um arquivo no formato pcap
def read_pcap_file(file_path):
    # Abre o arquivo pcap no modo de leitura binária ('rb')
    with open(file_path, 'rb') as file:
        # Lê os primeiros 24 bytes do arquivo, que correspondem ao cabeçalho pcap
        pcap_header = file.read(24)

        # Desempacota os dados do cabeçalho pcap usando o formato especificado
        magic_number, maior_version, menor_version, _, _, snap_len, fcs, link_type = struct.unpack('IHHIIIII', pcap_header)

        # Imprime os valores desempacotados do cabeçalho pcap
        print(f'Magic Number: {hex(magic_number)}')
        print(f'Maior Version: {maior_version}')
        print(f'Menor Version: {menor_version}')
        print(f'SnapLen: {snap_len}')
        print(f'FCS: {fcs}')
        print(f'LinkType: {link_type}')

        # Loop para ler e analisar cada pacote no arquivo pcap
        while True:
            # Lê os próximos 16 bytes do arquivo, que correspondem ao cabeçalho do pacote
            packet_header = file.read(16)

            # Verifica se há mais dados no arquivo, se não, sai do loop
            if not packet_header:
                break

            # Desempacota os dados do cabeçalho do pacote
            timestamp_sec, timestamp_usec, captured_len, original_len = struct.unpack('IIII', packet_header)

            # Imprime as informações do cabeçalho do pacote
            print('\nPacket Info:')
            print(f'Timestamp (Segundos): {timestamp_sec}')
            print(f'Timestamp (Microsegundos): {timestamp_usec}')
            print(f'Captura de Pacote Length: {captured_len}')
            print(f'Pacote Original Length: {original_len}')

            # Lê os dados do pacote com base no comprimento de captura
            packet_data = file.read(captured_len)

            # Aqui você pode analisar o conteúdo do pacote de acordo com o tipo de link (Ethernet, IPv4, TCP, UDP, etc.)
            # Este trecho de código pode ficar bastante complexo dependendo do que você deseja extrair dos pacotes

# Função principal que chama 'read_pcap_file' com o caminho do arquivo pcap
def main():
    file_path = 'S:\IFRN\Programação para redes\galileu\Q4.py'  # Caminho do arquivo pcap a ser lido
    read_pcap_file(file_path)

# Verifica se o script está sendo executado diretamente e chama a função 'main'
if __name__ == "__main__":
    main()
