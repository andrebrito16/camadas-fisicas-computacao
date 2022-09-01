
class GeneratePackages:

    def __init__(self, numberOfPackages) -> None:
        self.numberOfPackages = numberOfPackages
        self.packageList = []

    def generateHead(self, id: int, payloadSize: int, handshakeFlag: int) -> bytes:

        # Handshake with 10 bytes
        byteId = id.to_bytes(1, byteorder='big')
        byteNumberOfPackages = self.numberOfPackages.to_bytes(
            1, byteorder='big')
        bytePackageType = b"\x01"
        bytePayloadSize = payloadSize.to_bytes(1, byteorder='big')
        byteHandshakeFlag = handshakeFlag.to_bytes(1, byteorder='big')

        head = byteId + byteNumberOfPackages + bytePackageType + \
            bytePayloadSize + byteHandshakeFlag + b'\x00'*5

        return head

    def generatePayload(self, payload: bytes) -> bytes:
        return payload

    def generateEop(self) -> bytes:
        return b'\xFF\xFF\xFF\xFF'

    def generatePackage(self, id: int, packageType: int, payload: bytes, handshakeFlag: int) -> bytes:
        head = self.generateHead(
            id, self.numberOfPackages, packageType, len(payload), handshakeFlag)
        payload = self.generatePayload(payload)
        package = head + payload + self.generateEop()

        return package
