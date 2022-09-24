from datetime import datetime

class GenerateLog():
    
    def __init__(self) -> None:
        self.log = ''
        
    def generateLine(self, msg, msgType, packageSize, sendedPackage, totalPackages, CRC='FFA2') -> str:
        time = datetime.now()
        return f'{time} / {msg} / {msgType} / {packageSize} / {sendedPackage} / {totalPackages} / {CRC}'
    

