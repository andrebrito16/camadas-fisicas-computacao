from datetime import datetime

class GenerateLog:
    
    def __init__(self) -> None:
        self.log = ''
        
    def generateLine(self, msg, msgType, packageSize, sendedPackage, totalPackages, CRC='FFA2') -> str:
        time = datetime.now()
        self.log += f'{time} / {msg} / {msgType} / {packageSize} / {sendedPackage} / {totalPackages} / {CRC} \n'
    
    def save_log(self):
        with open('Server.txt', 'w') as f:
            f.write(self.log)
    

