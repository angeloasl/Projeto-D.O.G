/* O programa a seguir é parte de um sistema de garagem que busca reduzir as chances de ocorrer acidentes com cahorros/crianças
, como atropelamento ou fugas, na área da garagem.
  O sistema é formado por dois arduinos. Esse primeiro é responsável por detectar se a criança/cachorro se encontra na 
  garagem ou não.
  Para isso utiliza-se de um par de sensores ultrassônicos localizados acima da porta de passagem da garagem.*/

// PROJETO GRUPO 1 DE INTRODUÇÃO À ENGENHARIA DE CONTROLE E AUTOMAÇÃO
// ALUNOS: ÂNGELO ANTONIO, BIANCA VITORIA, ERIK LISBOA, FELIPE DE LIMA E GABRIEL MARTINS

#include <SoftwareSerial.h>
#include <Ultrasonic.h>

Ultrasonic ultrassomPortaCasa(7, 6); // Sensor localizado na porta da garagem pelo lado do corredor, ou seja, do lado 
de fora da garagem
Ultrasonic ultrassomPortaGaragem(5, 4); // // Sensor localizado na porta da garagem pelo lado da garagem, ou seja, 
do lado de dentro da garagem
SoftwareSerial blackBoardSlave(2, 3); // (RX, TX)

bool dog = false;
const int ledVerde = 11;
const int botao_sistema = 13; 
// Botão responsável pelo desligamento do sistema, caso o dono não deseje que ele esteja em funcionamento em determinada situação
const int ledVermelho = 9;
const int ledAmarelo = 10;
const int alarme = 8;
bool sinal_botao_sistema = true; // Variável que carrega o estado do sistema (ligado ou desligado), iniciando ligado (true)

void setup()
{

  pinMode(ledAmarelo, OUTPUT);
  pinMode(botao_sistema, INPUT);
  pinMode(ledVerde, OUTPUT);
  pinMode(ledVermelho, OUTPUT);
  blackBoardSlave.begin(9600);

}

void loop() {

  float distancia_PortaCasa = ultrassomPortaCasa.Ranging(CM); // Mede a distância do sensor em relação ao chão
  float distancia_PortaGaragem = ultrassomPortaGaragem.Ranging(CM); // Mede a distância do sensor em relação ao chão

  if (sinal_botao_sistema == false) // Se essa condição for satisfeita, o sistema encontra-se desligado
  , acenderá um led amarelo próximo à porta de acesso para informar ao usuário
  {
    digitalWrite(ledAmarelo, HIGH);
    digitalWrite(ledVermelho, LOW);
    digitalWrite(ledVerde, LOW);
    dog = false;
  }
  if (digitalRead(botao_sistema) == HIGH) // Botão que altera o estado do sistema apertado
  {
    while (digitalRead(botao_sistema) == HIGH);
    sinal_botao_sistema = !sinal_botao_sistema;
  }

  if (sinal_botao_sistema == true) /* Se essa condição for satisfeita, o sistema encontra-se ligado, 
  acenderá um led verde próximo à porta de acesso para informar ao usuário que o cachorro não se encontra na garagem,
  caso o cachorro seja detectado, 
  apagará o led verde e acenderá o vermelho */
  {
    digitalWrite(ledAmarelo, LOW);
    if ((distancia_PortaCasa >= 11) && (distancia_PortaCasa <= 15))
    {
      dog = false;
    }
    if ((distancia_PortaGaragem >= 11) && (distancia_PortaGaragem <= 15))
    {
      dog = true;
    }
  }
  if (dog == false) // Se essa variável é falsa, então o cachorro não se encontra na garagem
  {
    digitalWrite(ledVerde, HIGH);
    digitalWrite(ledVermelho, LOW);
    blackBoardSlave.print(1); // Informa ao outro arduino que o cachorro não se encontra na garagem
    noTone(alarme);
  }
  if (dog == true) // Se essa variável é verdadeira, então o cachorro encontra-se na garagem
  {
    digitalWrite(ledVermelho, HIGH);
    digitalWrite(ledVerde, LOW);
    blackBoardSlave.print(0); // Informa ao outro arduino que o cachorro encontra-se na garagem
    tone(alarme, 1000);
  }
}
