#include "SoftwareSerial.h" // Inclui a biblioteca SoftwareSerial
SoftwareSerial blackBoardMaster(2, 3); // (RX, TX)
int ledVermelho = 5;
int ledVerde = 6;
int controle = 11;
bool dog;

void setup()
{ // put your setup code here, to run once:
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(10, INPUT);
  Serial.begin(9600);
  blackBoardMaster.begin(9600);
}
int estadoPortao = 0;
unsigned long tempoAbrindo;
unsigned long tempoFechando;
unsigned long tempo;
void loop() {
  byte received = blackBoardMaster.read();
  Serial.println(received);
  
  if (blackBoardMaster.available() > 0)
  {

    if (received == 48) {
      dog = true;
    }
    if ((received == 49)||(received == 255)) {
      dog = false;
    }
  }
  if (estadoPortao == 0)  // Fechado
  {
    digitalWrite(ledVermelho, HIGH);
    digitalWrite(ledVerde, LOW);
    while (dog == true) {
      digitalWrite(ledVermelho, HIGH);
      digitalWrite(ledVerde, LOW);

      while (blackBoardMaster.available() > 0)

      {
        received = blackBoardMaster.read();
        if (received == 48) {
          dog = true;
        }
        if ((received == 49)||(received == 255)) {
          dog = false;
        }
      }
    }
    if (digitalRead(controle) == HIGH)
    {
      while (digitalRead(controle) == HIGH);
      estadoPortao = 1;
    }
  }
  if ((estadoPortao == 1) && (dog == false)) // Abrindo
  {
    tempoAbrindo = millis();
    while ((millis() - tempoAbrindo < 2000) && (estadoPortao == 1))
    {
      digitalWrite(ledVermelho, LOW);
      digitalWrite(ledVerde, HIGH);
      delay(100);
      digitalWrite(ledVerde, LOW);
      delay(100);
      tempo = millis() - tempoAbrindo;
      if (dog == true)
      break;
      while (blackBoardMaster.available() > 0)

      {
        received = blackBoardMaster.read();
        if (received == 48) {
          dog = true;
        }
        if ((received == 49)||(received == 255)) {
          dog = false;
        }
      }
    }
    estadoPortao = 2;
  }
  if ((estadoPortao == 2) && (dog == false)) // Aberto
  {
    digitalWrite(ledVermelho, LOW);
    digitalWrite(ledVerde, HIGH);
    if (digitalRead(controle) == HIGH)
    {
      while (digitalRead(controle) == HIGH);
      estadoPortao = 3;
    }
  }
  if ((estadoPortao == 3)||(dog==true))  // Fechando
  {
    tempoFechando = millis();
    while ((millis() - tempoFechando < tempo))
    {
      digitalWrite(ledVermelho, HIGH);
      digitalWrite(ledVerde, LOW);
      delay(100);
      digitalWrite(ledVermelho, LOW);
      delay(100);
    }
    estadoPortao = 0;
    tempo = millis() - tempoFechando;
  }
  if ((estadoPortao == 4))
  {
   tempoFechando = millis(); 
   while (millis() - tempoFechando < tempo)
   {
      digitalWrite(ledVermelho, HIGH);
      digitalWrite(ledVerde, LOW);
      delay(100);
      digitalWrite(ledVermelho, LOW);
      delay(100);
   }
   estadoPortao = 0;
  }
}
