#include "Enkoder.h"
#include "Stepper.h"
#include "Arduino.h"

const int X_STEP_PIN = 54;  // A9
const int X_ENABLE_PIN = 38;
const int X_DIR_PIN = 55;

Enkoder enkoder_ra(A1, A2, "ENRA");
Stepper stepper_ra(X_STEP_PIN, X_DIR_PIN, X_ENABLE_PIN, "STRA");
  
void setup() {
  Serial.begin(115200);
  enkoder_ra.setup_encoder();
  stepper_ra.setup_pins();
}

int counter = 0;

void loop() {
  enkoder_ra.update_position();
  if (counter >= 1000){
    enkoder_ra.print_to(Serial);
    counter = 0;
  }
  counter++;
}
