#define LED 13
byte input;

void setup() {
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    input = Serial.read();
    if (input == 1) {
      digitalWrite(LED, HIGH);
    }
    else if (input == 0) {
      digitalWrite(LED, LOW);
    }
  }
  delay(1000);
}
