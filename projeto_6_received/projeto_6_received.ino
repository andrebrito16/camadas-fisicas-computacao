int pinReceive = 4;
float T0 = 0;

void setup() {
  pinMode(pinReceive, INPUT);
  Serial.begin(9600);

}

// 21Mhz
float waitT(float qtdeTs=1, float speedClock=9600, float T0=0){
  /*
   * Como sabemos, 1 clock dura 1/9600 segundos
   * Além disso, 1 clock de 20Mhz dura 1/(20*10^6)
   */
  double oneClock = 1 / (21 * pow(10, 6));
  double oneT = 1 / speedClock;
  int qtdeClocks = floor(oneT / oneClock) + 1;
  for (int i = 0; i < int(qtdeClocks * qtdeTs); i++){
    __asm__("nop");
  }
  return T0 + qtdeClocks * qtdeTs;
}

int receiveData(int initMask=1, int pinReceive=4){
  int T0 = 0;
  int myInformation = 0; // 0000 0000; My information
  int qtde1s = 0;

  for (int i = 0; i < 8; i++){
    int bitNow = digitalRead(pinReceive);
    if (bitNow == 1){
      qtde1s++;
    }
    myInformation = myInformation |= (bitNow << i);
    waitT(1, 9600, 0);
  }

  // bit parity
  int bitNow = digitalRead(pinReceive);
  Serial.print("Bit de paridade coletado:  ");
  Serial.print(bitNow);
  Serial.print(" || ");
  Serial.print("Bit de paridade calculado:  ");
  Serial.print(qtde1s % 2);
  Serial.print(" || ");
  return myInformation;
}

void loop() {
  // Inicia recebimento de dados
  if (digitalRead(pinReceive) == 0){
    waitT(1.5, 9600, 0);
    int information = receiveData();
    Serial.print("Recebi: ");
    Serial.print(information, HEX);
    Serial.println(" ");
    delay(1000);
  }
  
}
