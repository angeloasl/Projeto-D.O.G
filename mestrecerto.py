#include <Ultrasonic.h>
#include "SoftwareSerial.h" // Inclui a biblioteca SoftwareSerial
Ultrasonic ultrassomPortaCasa(7, 6); // define o nome do sensor(ultrassom)
Ultrasonic ultrassomPortaGaragem(5, 4);
SoftwareSerial blackBoardSlave(2,3); // (RX, TX)
bool dog = false;
const int ledVerde = 11;
const int botao_sistema = 13;
const int botao_garagem = 13;
const int ledVermelho = 9;
const int ledAmarelo = 10;
bool sinal_botao_garagem;
bool sinal_botao_sistema;
bool led_State = HIGH;
void setup() 
{
  Serial.begin(9600);
  pinMode(ledAmarelo, OUTPUT);
  pinMode(botao_sistema, INPUT);
  pinMode(ledVerde, OUTPUT);
  pinMode(ledVermelho, OUTPUT);
  sinal_botao_sistema = true;
  blackBoardSlave.begin(9600);
  
}

void loop() {

  float distancia_PortaCasa = ultrassomPortaCasa.Ranging(CM);
  float distancia_PortaGaragem = ultrassomPortaGaragem.Ranging(CM);
  
  if (sinal_botao_sistema == false)
  {
  digitalWrite(ledAmarelo, HIGH);
  digitalWrite(ledVermelho, LOW);
  digitalWrite(ledVerde, LOW);   
  dog = false;
  }
  if (digitalRead(botao_sistema) == HIGH)
  {
    while (digitalRead(botao_sistema) == HIGH);
    sinal_botao_sistema = !sinal_botao_sistema;
  }

  if (sinal_botao_sistema == true) {    
    digitalWrite(ledAmarelo, LOW);
    if ((distancia_PortaCasa >= 11) && (distancia_PortaCasa <= 15))
    {
      dog = false;
    }
    if ((distancia_PortaGaragem >= 11) && (distancia_PortaGaragem <= 15))
    {
      dog = true;
    }
    if (dog==false)
    {
      digitalWrite(ledVerde, HIGH);
      digitalWrite(ledVermelho, LOW);
    }
     if (dog==true)
    {
      digitalWrite(ledVermelho,HIGH);
      digitalWrite(ledVerde, LOW);
    }
    if (dog == false){
      blackBoardSlave.print(1);
    }
    if (dog == true){
      blackBoardSlave.print(0);
    }
  }
}
