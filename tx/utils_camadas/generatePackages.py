
from email import header
from struct import pack
from collections import deque
import numpy as np


class GeneratePackages:

    def __init__(self, allBytes) -> None:
        self.numberOfPackages = (len(allBytes) // 114) + 1
        self.packageList = deque() # Create a queue
        self.bytes = allBytes
        self.lastSendedPackage = None
        self.CRC = b'\x00' * 2
        self.generateAllPackages()

    def generateHead(self, id: int = 0, payloadSize: int = 0, fileId: int = 0, messsageType: int = 1, handshakeFlag: int = 0, verificationFlag: int = 0, restartFromPackage: int = 0, lastSuccessReceivedPackage:int = 0) -> bytes:
        byteId = id.to_bytes(1, byteorder='big')
        byteNumberOfPackages = self.numberOfPackages.to_bytes(
            1, byteorder='big')
        bytePayloadSize = payloadSize.to_bytes(1, byteorder='big')
        byteHandshakeFlag = handshakeFlag.to_bytes(1, byteorder='big')
        byteMesssageType = messsageType.to_bytes(1, byteorder='big')
        byteFileId = fileId.to_bytes(1, byteorder='big') if handshakeFlag == 1 else bytePayloadSize
        byteVerificationFlag = verificationFlag.to_bytes(1, byteorder='big')
        byteRestartFromPackage = restartFromPackage.to_bytes(1, byteorder='big')
        byteLastSuccessReceivedPackage = lastSuccessReceivedPackage.to_bytes(1, byteorder='big')

        head = byteMesssageType + b'\x00' * 2 + byteNumberOfPackages + \
            byteId + byteFileId + byteRestartFromPackage + byteLastSuccessReceivedPackage + self.CRC
        return head

    def generatePayload(self, payload: bytes) -> bytes:
        return payload

    def generateEop(self) -> bytes:
        return b'\xAA\xBB\xCC\xDD'

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

    def generateHandshake(self, fileId) -> bytes:
        head = self.generateHead(0, fileId=fileId, packageType=0)
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

    def itIsPackageOk(self) -> bytes:
        head = self.generateHead(id=0, payloadSize=0, packageType=0, handshakeFlag=0, verificationFlag=1)
        payload = b''
        eop = self.generateEop()

        handshake = head + payload + eop

        return handshake

    def itIsPackageNotOk(self) -> bytes:
        head = self.generateHead(id=0, payloadSize=0, packageType=0, handshakeFlag=0, verificationFlag=0)
        payload = b''
        eop = self.generateEop()

        handshake = head + payload + eop

        return handshake

    def generateType1(self, fileId: int) -> bytes:
        head = self.generateHead(messsageType=1, fileId=fileId, handshakeFlag=1)
        eop = self.generateEop()
        package = head + eop
        return package
    
    def generateType2(self):
        head = self.generateHead(messsageType=2, fileId=1)
        eop = self.generateEop()
        package = head + eop
        return package

    def generateType3(self, id):
        payload = self.getChunkData()
        head = self.generateHead(messsageType=3, id=id, payloadSize=payload[5])
        package = head + payload[10:]
        return package

    def generateType4(self, lastSuccessReceivedPackage):
        head = self.generateHead(messsageType=4, lastSuccessReceivedPackage=lastSuccessReceivedPackage)
        eop = self.generateEop()
        package = head + eop
        return package
        
    def generateType5(self):
        head = self.generateHead(messsageType=5)
        eop = self.generateEop()
        package = head + eop
        return package
        
    def generateType6(self):
        head = self.generateHead(messsageType=6, lastSuccessReceivedPackage=self.lastSendedPackage[4])
        eop = self.generateEop()
        package = head + eop
        return package
