// DEC?
#include "stepper.h"

// DEC?
const int X_STEP_PIN = 54;  // A9
const int X_ENABLE_PIN = 38;
const int X_DIR_PIN = 55;

// RA?
const int Y_STEP_PIN = 60;
const int Y_DIR_PIN = 61;
const int Y_ENABLE_PIN = 56;

Stepper DEC_stepper(X_STEP_PIN, X_DIR_PIN, X_ENABLE_PIN);
Stepper RA_stepper(Y_STEP_PIN, Y_DIR_PIN, Y_ENABLE_PIN);

const int COMMAND_MAX_LENGTH = 20;
const int COMMAND_NAME_LENGTH = 10;
char command_string[COMMAND_MAX_LENGTH];
char command_name[COMMAND_NAME_LENGTH];
char command_trash[COMMAND_MAX_LENGTH];

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
 
  RA_stepper.setup_pins();
  DEC_stepper.setup_pins();
  Serial.begin(115200);
}

void blink_led(){
  delay(50);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(50);
  digitalWrite(LED_BUILTIN, LOW);
}

void handle_serial(){
  memset(command_string, 0, COMMAND_MAX_LENGTH);
  memset(command_name, 0, COMMAND_NAME_LENGTH);
  int command_argument = 0;
  
  Serial.readBytesUntil('\n', command_string, COMMAND_MAX_LENGTH);
  sscanf(command_string, "%s %d", command_name, &command_argument);
  if (0 == strcmp(command_name, "HALT")){
    DEC_stepper.halt();
  }else if (0 == strcmp(command_name, "RA_POSITION")){
    RA_stepper.print_position(Serial);
  }else if (0 == strcmp(command_name, "RA_MOVE_ABS")){
    RA_stepper.set_position_absolute(command_argument);
  }else if (0 == strcmp(command_name, "RA_HALT")){
    RA_stepper.halt();
  }else if (0 == strcmp(command_name, "RA_MOVE_REL")){
    RA_stepper.set_position_relative(command_argument);
  }else if (0 == strcmp(command_name, "POSITION")){
    DEC_stepper.print_position(Serial);
  }else if (0 == strcmp(command_name, "MOVE")){
    DEC_stepper.set_position_relative(command_argument);
  }else{
    Serial.print("UNKNOWN COMMAND: ");
    Serial.print(command_string);
    Serial.println("!");    
  }
}

void loop() {
  if (Serial.available()){
    handle_serial();
  }
  else{
    RA_stepper.move_if_needed();
    DEC_stepper.move_if_needed();
  }
}
