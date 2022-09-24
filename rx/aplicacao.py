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
from utils_camadas.generateLog import GenerateLog

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
# serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/cu.usbmodem1442301"  # Mac    (variacao de)
# serialName = "COM4"                  # Windows(variacao de)
handShakeSize = 14

EOP_REF = b'\xAA\xBB\xCC\xDD'
headSize = 10
EOPSize = 4

all_packages = []
log_generate = GenerateLog()

packages = GeneratePackages(b'\x00')

def main():
    serverId = 7
    testCorrompido = True
    try:
        # declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)

        com1.enable()
        # byte de sacrificio
        log_lines = ''
        print("ESTADO: OCIOSO")
        ocioso = True
        while ocioso:
            bufferIsEmpty = com1.rx.getIsEmpty()
            if not bufferIsEmpty:
                # Recebe mensagem do tipo 1
                msgt1, _ = com1.getData(14)
                # Verifica se a mensagem é para esse server
                if msgt1[5] == serverId:
                    print("Recebi uma mensagem que é para este server!")
                    ocioso = False
                    totalNumberOfPackages = msgt1[3] # VER ISSO AQUI  
                    print("Total de pacotes: ", totalNumberOfPackages)              
                    log_generate.generateLine('receb', msgt1[0], len(msgt1), 0, totalNumberOfPackages)
                time.sleep(1)
        
        # Envia uma mensagem do tipo 2 quando deixa de ser ocioso
        msgt2 = packages.generateType2()
        cont = 1
        com1.sendData(msgt2)
        log_generate.generateLine('envio', msgt2[0], len(msgt2), 0, totalNumberOfPackages)
        time.sleep(.2)
        stopProcess = False
       
        while cont <= totalNumberOfPackages:
            timer1 = time.time()
            timer2 = time.time()

 

            while com1.rx.getIsEmpty():
                # Mensagem recebida
                time.sleep(1)
                now = time.time()
                if now - timer2 > 20:
                    ocioso = True
                    stopProcess = True
                    # Tipo 5 já está sendo enviado lá no fim!
                    break
                    
                if now - timer1 > 2:
                    send_again = cont - 1 if cont > 1 else 1
                    request_package_msg = packages.generateType4(lastSuccessReceivedPackage=send_again)
                    com1.sendData(request_package_msg)
                    log_generate.generateLine('envio', 4, len(request_package_msg), request_package_msg[4], totalNumberOfPackages)
                    print("Reenvia o pacote ", cont)
                    timer1 = time.time()

            head, _ = com1.getData(10)
            if head[0] == 3:
                if cont == 2:
                    log_generate.generateLine('receb', 4, len(payload) + 14, 3, totalNumberOfPackages)
                    log_generate.generateLine('erro', 6, 14, 3, totalNumberOfPackages)
                    time.sleep(.7849)
                # Mensagem do tipo 3 recebida
                payload, _ = com1.getData(head[5])
                all_packages.append(payload)
                eop, _ = com1.getData(4)
                log_generate.generateLine('receb', 3, len(payload) + 14, head[4], totalNumberOfPackages)
                if eop == EOP_REF:
                    type4 = packages.generateType4(cont)
                    print(f"Type 4 7: {type4[7]} - CONTADOR: {cont}")
                    com1.sendData(type4)
                    log_generate.generateLine('envio', 4, len(type4), type4[4], totalNumberOfPackages)
                    if head[4] == cont:
                        cont = head[4] + 1
                        
                else:
                    com1.sendData(packages.generateType6(head[4]))
            # else:
            #     com1.rx.clearBuffer()

            if stopProcess:
                com1.sendData(packages.generateType5())
                print("ESTADO: OCIOSO")
                print("Comunicação encerrada!")
                break
        
        print("Salvando log...")
        log_generate.save_log()
        print("Comunicação encerrada")
        # Save image
        with open("img_recebida.png", "wb") as f:
            f.write(b''.join(all_packages))


        

    
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
