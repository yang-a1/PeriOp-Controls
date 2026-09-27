
const int SSR_PIN = 4;

void setup() {
  // put your setup code here, to run once:
  pinMode(SSR_PIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("Type 'on' or 'off' to control the relay.");
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim(); // remove spaces or newline

    if (cmd == "on") {
      digitalWrite(SSR_PIN, HIGH);
      Serial.println("Relay turned ON");
    }
    else if (cmd == "off") {
      digitalWrite(SSR_PIN, LOW);
      
      Serial.println("Relay turned OFF");
    }
    else {
      Serial.println("Unknown command. Use 'on' or 'off'.");
    }
  }
}
