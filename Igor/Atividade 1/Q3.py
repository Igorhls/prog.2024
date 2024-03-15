import dpkt
import datetime

def processar_captura(arquivo):
    with open(arquivo, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        inicia = None
        termina = None
        maior_pacote = 0
        incompleto_pacote = 0
        tamanho_pacotes = 0
        total_pacotes = 0

        for timestamp, buf in pcap:
            if inicia is None:
                inicia = datetime.datetime.fromtimestamp(timestamp)
            fim_pacote = datetime.datetime.fromtimestamp(timestamp)

            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data

            if len(buf) < ip.len:
                incompleto_pacote += 1

            if ip.len > maior_pacote:
                maior_pacote = ip.len

            tamanho_pacotes += ip.len
            total_pacotes += 1

        media_pacotes = tamanho_pacotes / total_pacotes

        return inicia, fim_pacote, maior_pacote, incompleto_pacote, media_pacotes


if __name__ == '__main__':
    nome_arquivo = "cap1.dump"
    inicia, fim, maior, incompleto, media = processar_captura(nome_arquivo)


    print(f"A captura de pacotes inicia em {inicia} e termina em {fim}.")
    print(f"O maior pacote capturado tem tamanho: {maior}.")
    print(f"O número de pacotes incompletos é: {incompleto}.")
    print(f"A média dos tamanhos de pacotes é: {media}.")