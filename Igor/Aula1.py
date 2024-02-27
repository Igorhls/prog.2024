from datetime import datetime

fd = open ("cap1.dump", "rb")
header = fd.read(24)

recHeader = fd.read(16)
while len(recHeader) == 16:
    recLen = int.from_bytes(recHeader[8:12], 'little')
    recTime = datetime.fromtimestamp(int.from_bytes(recHeader[0:4], 'little'))
    print (recTime)

    recPacket = fd.read(recLen)
    recHeader = fd.read(16)
fd.close()