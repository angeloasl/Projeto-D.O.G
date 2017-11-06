int ledVermelho=4;
int ledVerde=2;
int controle=10;

void setup() 
{  // put your setup code here, to run once:
pinMode(4,OUTPUT);
pinMode(2,OUTPUT);
pinMode(10,INPUT);
}
int estadoPortao = 0;
unsigned long tempoAbrindo;
unsigned long tempoFechando;
unsigned long tempo;

void loop() {
if (estadoPortao == 0)  // Fechado
{
  digitalWrite(ledVermelho, HIGH);
  digitalWrite(ledVerde, LOW);
  if (digitalRead(controle) == HIGH)
  {
    while (digitalRead(controle) == HIGH);
    estadoPortao = 1;
  }
}
if (estadoPortao == 1)  // Abrindo
{ 
  tempoAbrindo = millis();
  while((millis() - tempoAbrindo < 2000) && (estadoPortao == 1))
  {
   digitalWrite(ledVermelho, LOW);
   digitalWrite(ledVerde, HIGH);
   delay(100);
   digitalWrite(ledVerde, LOW);
   delay(100);
   tempo = millis() - tempoAbrindo;
   if (digitalRead(controle) == HIGH)
   estadoPortao = 2;
  }
  estadoPortao = 2;
}
if (estadoPortao == 2)  // Aberto
{
   digitalWrite(ledVermelho, LOW);
   digitalWrite(ledVerde, HIGH);
   if (digitalRead(controle) == HIGH)
   {
     while (digitalRead(controle) == HIGH);
     estadoPortao = 3;
   }
}
if (estadoPortao == 3)  // Fechando
{
  tempoFechando = millis();
  while((millis() - tempoFechando < tempo) && (digitalRead(controle)== LOW))
  {
    digitalWrite(ledVermelho, HIGH);
    digitalWrite(ledVerde, LOW);
    delay(100);
    digitalWrite(ledVermelho, LOW);
    delay(100);
  }
  tempo = millis() - tempoFechando;
  if(digitalRead(controle) == LOW)
  {
  estadoPortao = 0;
  }
}
}
