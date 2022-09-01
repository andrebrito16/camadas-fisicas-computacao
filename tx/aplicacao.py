#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from pydoc import describe
from enlace import *
import time
import numpy as np
import random

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
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

# N = 20
# num_commands = hex(N)
# print(len(num_commands), str(num_commands).split('b')[1].split('x')[1].replace('\'',''))

# flagBytes = str(num_commands).split('b')[1].split('x')[1].replace('\'','').upper()

# if len(flagBytes) == 3:
#     flagBytes = '0' + flagBytes
# print(flagBytes)
total_command = b''
for i in range(N):
    total_command += commands[random.randint(1, 9)]
# print(total_command.encode())
# print(type(len(total_command).to_bytes(1, byteorder='big')))
# print(len(total_command))
flag = len(total_command).to_bytes(1, byteorder='big')
total_command = flag + total_command
print(N)

def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")

        # time.sleep(.2)
        # # com1.sendData(len(num_commands).to_bytes('1', byteorder='big'))
        # time.sleep(1)

           
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        #txBuffer = imagem em bytes!
        # txBuffer = b'\x12\x13\xAA'  #isso é um array de bytes

        txBuffer = total_command
    
        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
    
            
        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
            
        
        com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
        
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        txSize = com1.tx.getStatus()
        while txSize == 0:
            txSize = com1.tx.getStatus()
        print('enviou = {}' .format(txSize))
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
    
        #acesso aos bytes recebidos
        txLen = 1 #len(txBuffer)
        # time.sleep(.2)
        flagIsEmpty = com1.rx.getIsEmpty()
        endtimeStamp = time.time() + 5
        
        while flagIsEmpty:
            flagIsEmpty = com1.rx.getIsEmpty()
            if time.time() > endtimeStamp:
                break

        if not flagIsEmpty:
            time.sleep(1)
            rxBuffer, nRx = com1.getData(txLen)
            print("recebeu {} bytes" .format(len(rxBuffer)))
            for i in range(len(rxBuffer)):
                print("recebeu {}" .format(rxBuffer[i]))
        else:
            print("Não recebeu nada")

            
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
