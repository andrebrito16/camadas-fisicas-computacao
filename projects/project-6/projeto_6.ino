int pinSend = 3;
float T0 = 0;
byte msg = 0x0B;

int initMask = 1;      // 0000 0001; Init mask
int myInformation = int(msg); // 0000 0101; My information

void setup() {
  pinMode(pinSend, OUTPUT);
  Serial.begin(9600);
  digitalWrite(pinSend, 1);
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


void sendData(int myInformation=5, int initMask=1, int pinSend=3){
  int T0 = 0;
  int qtde1s = 0;

  //Serial.print(0);
  //Serial.print("    ");
  //Serial.println(T0);

  // Start bit
  digitalWrite(pinSend, 0);
  T0 = waitT(1, 9600, T0);
  
  
  for (int i = 0; i < 8; i++){
    int bitNow = initMask & (myInformation >> i);
    if (bitNow == 1){
      qtde1s++;
    }
    //Serial.print(bitNow);
    //Serial.print("    ");
    //Serial.println(T0);
    digitalWrite(pinSend, bitNow);
    T0 = waitT(1, 9600, T0);
  }

  // bit Parity
  // Se for par => 0;
  // Se for impar => 1;
  int bitParity = qtde1s % 2;
  digitalWrite(pinSend, bitParity);
  T0 = waitT(1, 9600, T0);
  //Serial.print(bitParity);
  //Serial.print("    ");
  //Serial.println(T0);

  // Stop bit;
  digitalWrite(pinSend, 1);
  T0 = waitT(1, 9600, T0);
  //Serial.print(1);
  //Serial.print("    ");
  //Serial.println(T0);
  
}


void loop() {
  sendData(myInformation, initMask, pinSend);
  Serial.print("Enviei: ");
  Serial.print(msg, HEX);
  Serial.println(" ");
  delay(4000);
}
