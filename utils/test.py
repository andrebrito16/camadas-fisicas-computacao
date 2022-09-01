from generatePackages import GeneratePackages

# Random message on bytes
message = b'Hello World!'

numberOfBytes = len(message)

numberOfPackages = (numberOfBytes // 114) + 1

packages = GeneratePackages(numberOfPackages)
