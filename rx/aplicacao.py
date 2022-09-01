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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
# serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/cu.usbmodem1442401"  # Mac    (variacao de)
# serialName = "COM11"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        # declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        com1.enable()
        print("Esperando um byte de sacrifício")
        com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(1)
        print("Abriu a comunicação")

        time.sleep(.2)

        # Receeiving the commands
        rxBufferSize, nRxSize = com1.getData(1)
        rxBufferSize, nRxSize = com1.getData(
            int.from_bytes(rxBufferSize, byteorder='big'))

        # Split on \xcc
        commandsList = rxBufferSize.split(b'\xcc')
        commandsList.pop()  # Remove delimiter on the end
        print("Recebido {} comandos".format(len(commandsList)))

        time.sleep(0.5)
        returnFlag = len(commandsList)
        returnFlagBytes = returnFlag.to_bytes(1, byteorder='big')

        com1.sendData(returnFlagBytes)
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
