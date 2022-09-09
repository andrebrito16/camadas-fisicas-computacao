
from struct import pack
from collections import deque
import numpy as np


class GeneratePackages:

    def __init__(self, allBytes) -> None:
        self.numberOfPackages = (len(allBytes) // 114) + 1
        self.packageList = deque() # Create a queue
        self.bytes = allBytes
        self.lastSendedPackage = None

        self.generateAllPackages()

    def generateHead(self, id: int, payloadSize: int, packageType: int = 1, handshakeFlag: int = 0, verificationFlag: int = 0) -> bytes:
        byteId = id.to_bytes(1, byteorder='big')
        byteNumberOfPackages = self.numberOfPackages.to_bytes(
            2, byteorder='big')
        bytePayloadSize = payloadSize.to_bytes(1, byteorder='big')
        byteHandshakeFlag = handshakeFlag.to_bytes(1, byteorder='big')
        bytePackageType = packageType.to_bytes(1, byteorder='big')
        byteVerificationFlag = verificationFlag.to_bytes(1, byteorder='big')

        head = byteId + byteNumberOfPackages + bytePackageType + \
            bytePayloadSize + byteHandshakeFlag + \
            byteVerificationFlag + b'\x00'*3

        return head

    def generatePayload(self, payload: bytes) -> bytes:
        return payload

    def generateEop(self) -> bytes:
        return b'\xFF\xFF\xFF\xFF'

    def generatePackage(self, id: int, packagePayload: bytes) -> bytes:
        head = self.generateHead(id, len(packagePayload))
        payload = self.generatePayload(packagePayload)
        eop = self.generateEop()

        package = head + payload + eop

        return package

    def generateAllPackages(self) -> list:

        for i in range(self.numberOfPackages):
            packagePayload = self.bytes[i*114:min((i+1)*114, len(self.bytes))]
            package = self.generatePackage(i+1, packagePayload)
            self.packageList.append(package)

        self.packageList = deque(np.array(self.packageList))

    def generateHandshake(self) -> bytes:
        head = self.generateHead(id=0, payloadSize=0, packageType=0)
        payload = b''
        eop = self.generateEop()

        handshake = head + payload + eop

        return handshake

    def itIsOk(self) -> bytes:
        head = self.generateHead(id=0, payloadSize=0, packageType=0, handshakeFlag=1)
        payload = b''
        eop = self.generateEop()

        handshake = head + payload + eop

        return handshake

    def packageVerficationFlag(self, flag) -> bytes:
        head = self.generateHead(0, packageType=2, verificationFlag=flag)
        payload = b''
        eop = self.generateEop()

        verificationPackage = head + payload + eop

        return verificationPackage
    
    def getChunkData(self):
        self.lastSendedPackage = self.packageList.popleft()
        return self.lastSendedPackage
    
    def recoverLastPackage(self):
        if self.lastSendedPackage is not None:
            self.packageList.appendleft(self.lastSendedPackage)
            self.lastSendedPackage = None