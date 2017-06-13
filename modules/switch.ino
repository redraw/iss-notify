#define PIN 13
byte input;

void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    input = Serial.read();
    if (input == 1) {
      digitalWrite(PIN, HIGH);
    }
    else if (input == 0) {
      digitalWrite(PIN, LOW);
    }
  }
  delay(1000);
}
