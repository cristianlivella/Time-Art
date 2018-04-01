#include <SPI.h>
#include <Ethernet2.h>

byte mac[] = { 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF };
byte ip[] = { 192, 168, 1, 11 };

int ledB = 3;
int ledG = 5;
int ledR = 6;
int led1 = 7;
int led2 = 8;

EthernetServer server(80);
String par, val;
int reading = 0, intVal, ledBv = 0, ledGv = 0, ledRv = 0, led1v = 0, led2v = 0;

void elaborateRequest();

void setup() {
  pinMode(ledB, OUTPUT);
  pinMode(ledG, OUTPUT);
  pinMode(ledR, OUTPUT);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  Ethernet.begin(mac, ip);
  server.begin();
  Serial.begin(9600);
  Serial.println("Arduino here!");
  Serial.print("IP: ");
  Serial.println(Ethernet.localIP());
  Serial.println();
}

void loop() {
  EthernetClient client = server.available();
  if (client) {
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        if (c==' ') {
          reading = 0;
        }
        else if (c=='=') {
          reading = 2;
        }
        else if (c=='&') {
          elaborateRequest();
        }
        if (reading==1 && c!='&' && c!='=') {
          par += c;
        }
        else if (reading==2 && c!='&' && c!='=') {
          val += c;
        }
        if (c=='?') {
          reading = 1;
        }
        if (c == '\n') {
          elaborateRequest();
          reading = 0;
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/html");
          client.println();
          client.print("Arduino here!");
          client.print("-LedR:");
          client.print(ledRv);
          client.print("-LedG:");
          client.print(ledGv);
          client.print("-LedB:");
          client.print(ledBv);
          client.print("-Led1:");
          client.print(led1v);
          client.print("-Led2:");
          client.print(led2v);
          delay(1);
          client.stop();
        }
      }
    }
  }
}

void elaborateRequest() {
  if (par!="" && val!="") {
    Serial.println();
    Serial.print("PAR: ");
    Serial.println(par);
    Serial.print("VAL: ");
    Serial.println(val);
    intVal = val.toInt();
    if (par=="ledB") {
      analogWrite(ledB, intVal);
      ledBv = intVal;
    }
    else if (par=="ledG") {
      analogWrite(ledG, intVal);
      ledGv = intVal;
    }
    else if (par=="ledR") {
      analogWrite(ledR, intVal);
      ledRv = intVal;
    }
    else if (par=="led1") {
      digitalWrite(led1, intVal);
      led1v = intVal;
    }
    else if (par=="led2") {
      digitalWrite(led2, intVal);
      led2v = intVal;
    }
  }
  par = "";
  val = "";
  reading = 1;
}
