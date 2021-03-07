#include "Enkoder.h"
#include "Stepper.h"
#include "Arduino.h"

const uint8_t X_STEP_PIN = 54;  // A9
const uint8_t X_ENABLE_PIN = 38;
const uint8_t X_DIR_PIN = 55;
const uint8_t AUX_A_PIN = A1;// TODO! for mega!
const uint8_t AUX_B_PIN = A2; // TODO!

const uint8_t COMMAND_MAX_LENGTH = 20;
const uint8_t COMMAND_NAME_LENGTH = 10;
char command_string[COMMAND_MAX_LENGTH];
char command_name[COMMAND_NAME_LENGTH];
char command_trash[COMMAND_MAX_LENGTH];

Enkoder enkoder_ra(AUX_A_PIN, AUX_B_PIN, "ENRA");
Stepper stepper_ra(X_STEP_PIN, X_DIR_PIN, X_ENABLE_PIN, "STRA");

void handle_unknown_command(){
  Serial.print("UNKNOWN COMMAND: ");
  Serial.print(command_string);
  Serial.println("!");  
}

void handle_serial(){
  memset(command_string, 0, COMMAND_MAX_LENGTH);
  memset(command_name, 0, COMMAND_NAME_LENGTH);
  int command_argument = 0;
  
  Serial.readBytesUntil('\n', command_string, COMMAND_MAX_LENGTH);
  sscanf(command_string, "%s %d", command_name, &command_argument);
  if (0 == strcmp(command_name, "HALT")){
  }else if (0 == strcmp(command_name, "RA_POSITION")){
  }else if (0 == strcmp(command_name, "RA_MOVE_ABS")){
  }else if (0 == strcmp(command_name, "RA_HALT")){
  }else if (0 == strcmp(command_name, "RA_MOVE_REL")){
  }else if (0 == strcmp(command_name, "POSITION")){
  }else if (0 == strcmp(command_name, "MOVE")){
  }else{
    handle_unknown_command();  
  }
}

int counter = 0;

void handle_runnables(){
    enkoder_ra.runnable_update_position();
  if (counter >= 1000){
    enkoder_ra.print_to(Serial);
    counter = 0;
  }

  counter++;
}

void setup() {
  Serial.begin(115200);
  enkoder_ra.setup_encoder();
  stepper_ra.setup_pins();
}

void loop() {
  if (Serial.available()){
    handle_serial();
  }
  handle_runnables();
}
