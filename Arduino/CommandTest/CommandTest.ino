/*
  Command protocol test A
*/

const int handshake_pin = 12;
int x;
bool finished = false;
String message_in = "";
String serial_no_in = "";
String command_in = "";

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ;  // wait for serial port to connect. Needed for native USB port only
  }
  pinMode(handshake_pin, OUTPUT);   // handshake is on digital pin 2
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (finished) {
    digitalWrite(handshake_pin, LOW);
  } else {
    digitalWrite(handshake_pin, HIGH);
    if(Serial.available() > 0)
    {
      digitalWrite(handshake_pin, LOW);
      message_in = Serial.readStringUntil('\n');
      if (message_in.length() < 8) {
        Serial.println("BADM");
      }
      serial_no_in = message_in.substring(0,4);
      command_in = message_in.substring(4,8);
      if (command_in == "WHOU") {
        Serial.println(serial_no_in + "OKOK" + "Arduino");
      } else if (command_in == "DUMY") {
        Serial.println(serial_no_in + "OKOK" + "Dummy");
      } else if (command_in == "EXIT") {
        Serial.println(serial_no_in + "OKOK" + "Exiting");
        finished = true;
      } else if (command_in == "LED+") {
        Serial.println(serial_no_in + "OKOK" + "LED ON");
        digitalWrite(LED_BUILTIN, HIGH);
      } else if (command_in == "LED-") {
        Serial.println(serial_no_in + "OKOK" + "LED OFF");
        digitalWrite(LED_BUILTIN, LOW);
      } else {
        Serial.println(serial_no_in + "BADC");
      }
    }
  }
}
