import sys, hashlib

if len(sys.argv) < 2:
    print(f"uso:{sys.argv[0]} nomearq")
    print("Exemplo: python3 hash.py arquivo.txt")
    sys.exit(1)

fd = open(sys.argv[1], "rb")
h = hashlib.sha256()
h.update
fd.close
print(h.hexdigest())
