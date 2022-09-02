from generatePackages import GeneratePackages
import numpy as np

# Random message on bytes
message = b'\xAA'*300*3

packages = GeneratePackages(message)

print(packages.packageList[0][1] + packages.packageList[0][2])
