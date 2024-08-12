import threading
import time
import random

def piloto(nome):
    distancia = 0
    while distancia < 100:
        velocidade = random.randint(1, 10)
        distancia += velocidade
        print(f"{nome} percorreu {distancia} metros.")
        time.sleep(0.1)
    print(f"{nome} terminou a corrida!")

pilotos = ["Piloto 1", "Piloto 2", "Piloto 3"]

threads = []
for piloto_nome in pilotos:
    t = threading.Thread(target=piloto, args=(piloto_nome,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Corrida terminada!")
