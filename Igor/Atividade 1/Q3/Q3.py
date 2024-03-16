import os
import statistics
import socket
import struct
import time

def read_pcap(file_path):
    # Lê um arquivo pcap e retorna uma lista de pacotes.
    packets = []
    with open(file_path, 'rb') as f:
        pcap_header = f.read(24)
        while True:
            timestamp_bytes = f.read(4)
            if not timestamp_bytes:
                break
            timestamp = struct.unpack('<I', timestamp_bytes)[0]
            f.read(4)  # Ignorar a precisão do timestamp
            captured_len = struct.unpack('<I', f.read(4))[0]
            packet_len = struct.unpack('<I', f.read(4))[0]
            packet_data = f.read(captured_len)
            packets.append((timestamp, packet_data))
            # Ignorar qualquer padding
            if captured_len < packet_len:
                f.read(packet_len - captured_len)
    return packets

def analyze_packets(packets):
    # Analisa os pacotes e extrai as informações necessárias.
    ip_packets = []
    for timestamp, packet_data in packets:
        ethertype = struct.unpack('>H', packet_data[12:14])[0]
        if ethertype == 0x0800:  # IPv4
            ip_packets.append(packet_data[14:])
    
    tcp_packets = [p for p in ip_packets if p[9] == 6]  # Protocolo TCP
    udp_packets = [p for p in ip_packets if p[9] == 17]  # Protocolo UDP

    ip_sizes = [len(p) for p in ip_packets]
    tcp_sizes = [len(p) for p in tcp_packets]
    udp_sizes = [len(p) for p in udp_packets]

    max_tcp_size = max(tcp_sizes) if tcp_sizes else 0
    incomplete_packets = sum(1 for p in ip_packets if len(p) != len(p[8:]))

    avg_udp_size = statistics.mean(udp_sizes) if udp_sizes else 0

    ip_counts = {}
    for p in ip_packets:
        src_ip = socket.inet_ntoa(p[12:16])
        if src_ip not in ip_counts:
            ip_counts[src_ip] = 0
        ip_counts[src_ip] += 1

    max_traffic_ip = max(ip_counts, key=ip_counts.get)
    max_traffic_count = ip_counts[max_traffic_ip]

    return {
        'ip_headers': [socket.inet_ntoa(p[12:16]) for p in ip_packets],
        'capture_time': (packets[0][0], packets[-1][0]),
        'max_tcp_size': max_tcp_size,
        'incomplete_packets': incomplete_packets,
        'avg_udp_size': avg_udp_size,
        'max_traffic_ip': max_traffic_ip,
        'max_traffic_count': max_traffic_count
    }

def print_results(results):
    # Imprime resultados num formato legível.
    print("\nResultados:")
    print("a) Cabeçalhos IP:")
    for header in results['ip_headers']:
        print(header)

    print("\nb) Tempo de captura:")
    print(f"Início: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(results['capture_time'][0]))}s")
    print(f"Fim: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(results['capture_time'][1]))}s")

    print(f"\nc) Maior tamanho do pacote TCP: {results['max_tcp_size']} bytes")
    print(f"d) Quantidade de pacotes incompletos: {results['incomplete_packets']}")
    print(f"e) Média do tamanho dos pacotes UDP: {results['avg_udp_size']} bytes")
    print(f"f) IPs com maior tráfego: {results['max_traffic_ip']} ({results['max_traffic_count']} pacotes)")
    print(f"g) Número de IPs com os quais a interface capturada interagiu: {len(set(results['ip_headers']))}")

"""Substitua 'path/to/your/pcap/file' abaixo pelo caminho do arquivo pcap"""

file_path = 'path/to/your/pcap/file'
packets = read_pcap(file_path)
results = analyze_packets(packets)
print_results(results)
