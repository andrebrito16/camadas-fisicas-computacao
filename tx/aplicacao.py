#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2022
# Aplicação
####################################################


# esta é a camada superior, de aplicação do seu software de comunicação serial UART.
# para acompanhar a execução e identificar erros, construa prints ao longo do código!


from struct import pack
import sys
import random
import numpy as np
import time
from enlace import *
from pydoc import describe
from time import sleep

from utils_camadas.generatePackages import GeneratePackages


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
# serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/cu.usbmodem1442301"  # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)

# Carregando imagem em binário
imageR = "./img_p3.png"

txBuffer = open(imageR, 'rb').read()

# Carregando imagem em binário
# imageR ="../img_p3.png"

# txBuffer = open(imageR, 'rb').read()

message = txBuffer

# total_command = b''
# for i in range(N):
#     total_command += commands[random.randint(1, 9)]

# flag = len(total_command).to_bytes(1, byteorder='big')
# total_command = flag + total_command

# print(N)

# Create GenearePackages object
packages = GeneratePackages(message)
fileId = 0
serverId = 7

def main():
    try:
        print("Iniciou o main")

        com1 = enlace(serialName)

        com1.enable()

        time.sleep(.2)

        print("Abriu a comunicação")

        print(f"Vamos enviar {len(message)} bytes")


        # First loop
        inicia = False
        while not inicia:
            print("Iniciando o Message Type 1 (quero falar com você)")
            messageType1 = packages.generateType1(fileId=serverId)
            print(messageType1, len(messageType1))
            com1.sendData(messageType1)
            sleep(5)
            if not com1.rx.getIsEmpty():
                messageType2Response, _ = com1.getData(14)
                
                if (messageType2Response[5] == 1):
                    print("Message type 2 recebido com sucesso (servidor na escuta)")
                    inicia = True

        if inicia:
            while len(packages.packageList ) != 0:
                package = packages.getChunkData()
                print(f"Enviando pacote com id {package[0]}")
     
                com1.sendData(package)
                sleep(.05)
                response, _ = com1.getData(14)
                sleep(.2)

                if (response[6] == 1):
                    print(f"Pacote {package[0]} enviado com sucesso")
                else:
                    print("Pacote não enviado")
                    packages.recoverLastPackage() # Recupera o último pacote para voltar

        # Encerra comunicação
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
