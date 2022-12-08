
Baudrate = Bits/deltat

Na função `_sw_uart_wait_half_T()` temos:
- contMax
- BaudRate (Br)
- Frequência do processador (FP)

A relação entre esses valores é:

    contMax = (FP / Br) * (1/2)

Função necessária para não haver leitura na borda, usada apenas no receptor.


Cuidado: Se o sinal for estéreo, são na verdade dois canais.
