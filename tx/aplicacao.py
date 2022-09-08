#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2022
# Aplicação
####################################################


# esta é a camada superior, de aplicação do seu software de comunicação serial UART.
# para acompanhar a execução e identificar erros, construa prints ao longo do código!


from pydoc import describe
from enlace import *
import time
import numpy as np
import random
from generatePackages import GeneratePackages

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
# serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)

N = random.randint(10, 30)

commands = {
    1: b'\x00\xFA\x00\x00\xCC',
    2: b'\x00\x00\xFA\x00\xCC',
    3: b'\xFA\x00\x00\xCC',
    4: b'\x00\xFA\x00\xCC',
    5: b'\x00\x00\xFA\xCC',
    6: b'\x00\xFA\xCC',
    7: b'\xFA\x00\xCC',
    8: b'\x00\xCC',
    9: b'\xFA\xCC'
}

# Carregando imagem em binário
imageR ="../img_p3.png"

txBuffer = open(imageR, 'rb').read()

message = txBuffer

# total_command = b''
# for i in range(N):
#     total_command += commands[random.randint(1, 9)]

# flag = len(total_command).to_bytes(1, byteorder='big')
# total_command = flag + total_command

# print(N)

# Create GenearePackages object
packages = GeneratePackages(message)


def main():
    try:
        print("Iniciou o main")

        com1 = enlace(serialName)

        com1.enable()

        time.sleep(.2)

        print("Abriu a comunicação")

        # message = b"\xAA"*189

        print(f"Vamos enviar {len(message)} bytes")

        # as array apenas como boa pratica para casos de ter uma outra forma de dados

        print("Iniciando transmissão...")
        

        com1.sendData(np.asarray(txBuffer))

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
