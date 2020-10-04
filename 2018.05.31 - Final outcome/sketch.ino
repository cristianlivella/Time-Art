sketch.ino#include <SPI.h>
#include <Ethernet2.h>
#include <IRremote.h>
#include <HashMap.h>

CreateHashMap(commands, char *, int, 24);

commands["on"] = 16236607;
commands["off"] = 16203967;
commands["su"] = 16187647;
commands["giu"] = 16220287;
commands["flash"] = 16240687;
commands["strobe"] = 16248847;
commands["fade"] = 16238647;
commands["smooth"] = 16246807;
commands["white"] = 16244767;
commands["red"] = 16195807;
commands["red2"] = 16191727;
commands["green"] = 16228447;
commands["green2"] = 16224367;
commands["blue"] = 16212127;
commands["blue2"] = 16208047;
commands["blue3"] = 16230487;
commands["orange"] = 16199887;
commands["orange2"] = 16189687;
commands["purple"] = 16216207;
commands["purple2"] = 16206007;
commands["ciano"] = 16232527;
commands["ciano2"] = 16222327;
commands["yellow"] = 16197847;
commands["fuchsia"] = 16214167;

//IR
IRsend irsend;
decode_results results;
unsigned long value;

int codeType = 3;
unsigned long codeValue;
int codeLen=32;

//ETHERNET
byte mac[] = { 0xAA, 0xBB , 0xCC, 0xDD, 0xEE, 0xFF };
byte ip[] = { 192, 168, 1, 11 };
int ledPin = 3;

EthernetServer server(80);
String httpGet;
bool reading = false;

void sendCode(unsigned int command) {//MANDARE COSE
  codeValue = command;
  int repeat = 0;
  if (codeType == NEC) {
    if (repeat) {
      irsend.sendNEC(REPEAT, codeLen);
      Serial.println("Sent NEC repeat");
    } else {
      irsend.sendNEC(codeValue, codeLen);
      Serial.print("Sent NEC ");
      Serial.println(codeValue, HEX);
    }
  delay(15);
  }

}

void setup() {
  pinMode(ledPin, OUTPUT);
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
          reading = false;
        }
        if (reading==true) {
          httpGet += c;
        }
        else if (c=='?') {
          reading = true;
        }
        if (c == '\n') {
          Serial.println(httpGet);
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/html");
          client.println();
          client.print("<html><body>");
          client.print("<h1>Arduino here!</h1>");
          client.print("<h2>IP: ");
          client.print(Ethernet.localIP());
          client.print("</h2>");
          client.print("</body></html>");
          delay(1);
          client.stop();
          sendCode(commands[httpGet]);
          serial.printLn("Command " + httpGet + " sent");
          httpGet = "";
        }
      }
    }
  }
}
