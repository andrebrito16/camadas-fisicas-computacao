from generatePackages import GeneratePackages
import numpy as np

# # Random message on bytes
# message = b'\xAA'*300*3

imageR ="./img_p3.png"

txBuffer = open(imageR, 'rb').read()

message = txBuffer

packages = GeneratePackages(message)
packages.itIsOk()

print(packages.generateHandshake()[2])
# print(packages.packageList[0][1] + packages.packageList[0][2])
# print(packages.getChunkData())
# print(packages.lastSendedPackage)
