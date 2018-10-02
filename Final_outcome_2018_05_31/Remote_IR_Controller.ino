#include <SPI.h>
#include <Ethernet2.h>
#include <IRremote.h>

struct Command {
  unsigned int on = 16236607;
  unsigned int off = 16203967;
  unsigned int su = 16187647;
  unsigned int giu = 16220287;
  unsigned int flash = 16240687;
  unsigned int strobe = 16248847;
  unsigned int fade = 16238647;
  unsigned int smooth = 16246807;
};

struct Color {
  unsigned int white = 16244767;
  unsigned int red = 16195807;
  unsigned int red2 = 16191727;
  unsigned int green = 16228447;
  unsigned int green2 = 16224367;
  unsigned int blue = 16212127;
  unsigned int blue2 = 16208047;
  unsigned int blue3 = 16230487;
  unsigned int orange = 16199887;
  unsigned int orange2 = 16189687;
  unsigned int purple = 16216207;
  unsigned int purple2 = 16206007;
  unsigned int ciano = 16232527;
  unsigned int ciano2 = 16222327;
  unsigned int yellow = 16197847;
  unsigned int fuchsia = 16214167;
};

Color color;
Command command;

//IR
IRsend irsend;
decode_results results;
unsigned long value;

int codeType = 3;
unsigned long codeValue;
int codeLen=32;

//ETHERNET
byte mac[] = { 0x90, 0xA2 , 0xDA, 0x11, 0x17, 0x31 };
byte ip[] = { 10, 205, 0, 18 };
int ledPin = 5;

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
          if (httpGet=="ledon") {
            sendCode(command.on);
            Serial.println("Led on");
          }
          else if (httpGet=="ledoff") {
            sendCode(command.off);
            Serial.println("Led off");
          }
          else if (httpGet=="su") {
            sendCode(command.su);
            Serial.println("Command su sended");
          }
          else if (httpGet=="giu") {
            sendCode(command.giu);
            Serial.println("Command giu sended");
          }
          else if (httpGet=="flash") {
            sendCode(command.flash);
            Serial.println("Command flash sended");
          }
          else if (httpGet=="strobe") {
            sendCode(command.strobe);
            Serial.println("Command strobe sended");
          }
          else if (httpGet=="fade") {
            sendCode(command.fade);
            Serial.println("Command fade sended");
          }
          else if (httpGet=="smooth") {
            sendCode(command.smooth);
            Serial.println("Command smooth sended");
          }
          else if (httpGet=="white") {
            sendCode(color.white);
            Serial.println("Color swithced to white");
          }
          else if (httpGet=="red") {
            sendCode(color.red);
            Serial.println("Color swithced to red");
          }
          else if (httpGet=="red2") {
            sendCode(color.red2);
            Serial.println("Color swithced to red2");
          }
          else if (httpGet=="green") {
            sendCode(color.green);
            Serial.println("Color swithced to green");
          }
          else if (httpGet=="green2") {
            sendCode(color.green2);
            Serial.println("Color swithced to green2");
          }
          else if (httpGet=="blue") {
            sendCode(color.blue);
            Serial.println("Color swithced to blue");
          }
          else if (httpGet=="blue2") {
            sendCode(color.blue2);
            Serial.println("Color swithced to blue2");
          }
          else if (httpGet=="blue3") {
            sendCode(color.blue3);
            Serial.println("Color swithced to blue3");
          }
          else if (httpGet=="orange") {
            sendCode(color.orange);
            Serial.println("Color swithced to orange");
          }
          else if (httpGet=="orange2") {
            sendCode(color.orange2);
            Serial.println("Color swithced to orange2");
          }
          else if (httpGet=="purple") {
            sendCode(color.purple);
            Serial.println("Color swithced to purple");
          }
          else if (httpGet=="purple2") {
            sendCode(color.purple2);
            Serial.println("Color swithced to purple2");
          }
          else if (httpGet=="ciano") {
            sendCode(color.ciano);
            Serial.println("Color swithced to ciano");
          }
          else if (httpGet=="ciano2") {
            sendCode(color.ciano2);
            Serial.println("Color swithced to ciano2");
          }
          else if (httpGet=="yellow") {
            sendCode(color.yellow);
            Serial.println("Color swithced to yellow");
          }
          else if (httpGet=="fuchsia") {
            sendCode(color.fuchsia);
            Serial.println("Color swithced to fuchsia");
          }
          httpGet = "";
        }
      }
    }
  }
}
