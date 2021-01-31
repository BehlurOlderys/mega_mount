const int X_STEP_PIN = 54;
const int X_ENABLE_PIN = 38;
//const int X_DIR_PIN = 55;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(X_STEP_PIN, OUTPUT);
  pinMode(X_ENABLE_PIN, OUTPUT);
//  pinMode(X_DIR_PIN, OUTPUT);

  digitalWrite(X_ENABLE_PIN, LOW);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  digitalWrite(X_STEP_PIN, HIGH);
  delay(100);
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(X_STEP_PIN, LOW);
  delay(100);
}
