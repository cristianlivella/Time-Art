#include <SPI.h>
#include <Ethernet2.h>

byte mac[] = { 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF };
byte ip[] = { 192, 168, 1, 11 };
int ledPin = 5;

EthernetServer server(80);
String httpGet;
bool reading = false;

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
            digitalWrite(ledPin, HIGH);
            Serial.println("Led on");
          }
          else if (httpGet=="ledoff") {
            digitalWrite(ledPin, LOW);
            Serial.println("Led off");
          }
          httpGet = "";
        }
      }
    }
  }
}
