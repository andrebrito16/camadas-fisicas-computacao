#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2022
# Aplicação
####################################################


# esta é a camada superior, de aplicação do seu software de comunicação serial UART.
# para acompanhar a execução e identificar erros, construa prints ao longo do código!


from mimetypes import common_types
from enlace import *
import time
import numpy as np
from utils_camadas.generatePackages import GeneratePackages

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
# serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/cu.usbmodem1442401"  # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)
handShakeSize = 14

EOP_REF = b'\xAA\xBB\xCC\xDD'
headSize = 10
EOPSize = 4

package = GeneratePackages(b'\x00')

all_packages = []



def main():
    testCorrompido = True
    try:
        print("Iniciou o main")
        # declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        com1.enable()
        # byte de sacrificio
        print("Esperando um handShake")

        initData, nRx = com1.getData(14)
        print("Recebeu um handShake")


        # Get total packs
        total_packs = int.from_bytes(initData[1:3], byteorder='big')
        time.sleep(0.2)

        # Send its ok
        com1.sendData(package.itIsOk())
        print("Enviou um handShake itItsOk")
        time.sleep(0.2)

        current_id = 1
        while current_id <= total_packs:
            
            # Get head package
            initData, nRx = com1.getData(headSize)
            time.sleep(0.2)

            # Get payload package
            current_payload_size = initData[4] 
            current_payload_data, nRx = com1.getData(current_payload_size)
            print(current_payload_size)
            time.sleep(0.2)

            # Get EOP package
            EOP_test, nRx = com1.getData(EOPSize)
            print(EOP_REF, EOP_test)
            if EOP_test != EOP_REF or testCorrompido:
                testCorrompido = False
                print("----PAYLOAD CORROMPIDO----")
                com1.sendData(package.itIsPackageNotOk())
            else:
                print("----PAYLOAD OK----")
                com1.sendData(package.itIsPackageOk())
                all_packages.append(current_payload_data)
                current_id += 1

            time.sleep(0.2)
        print(all_packages)

        # Transform list of bytes in png img

        with open('img_result.png', 'wb') as f:
            f.write(bytes(b''.join(all_packages)))
        

        com1.rx.clearBuffer()
        time.sleep(1)
        print("Abriu a comunicação")

        time.sleep(.2)

    
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
