#include "Enkoder.h"
#include "Arduino.h"

Enkoder enkoder_ra(A1, A2);

void setup() {
  Serial.begin(115200);
  enkoder_ra.setup_encoder();
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
