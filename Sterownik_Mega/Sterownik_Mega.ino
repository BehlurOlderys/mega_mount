// DEC?
#include "stepper.h"


const int X_STEP_PIN = 54;  // A9
const int X_ENABLE_PIN = 38;
const int X_DIR_PIN = 55;

Stepper DEC_stepper(X_STEP_PIN, X_DIR_PIN, X_ENABLE_PIN);


// RA?
const int Y_STEP_PIN = 60;
const int Y_DIR_PIN = 61;
const int Y_ENABLE_PIN = 56;

Stepper RA_stepper(Y_STEP_PIN, Y_DIR_PIN, Y_ENABLE_PIN);

const int COMMAND_MAX_LENGTH = 20;
const int COMMAND_NAME_LENGTH = 10;
char command_string[COMMAND_MAX_LENGTH];
char command_name[COMMAND_NAME_LENGTH];
char command_trash[COMMAND_MAX_LENGTH];

bool dir_forward = true;
int motor_position = 0;
int desired_position = 0;
bool is_enabled = false;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(X_STEP_PIN, OUTPUT);
  pinMode(X_ENABLE_PIN, OUTPUT);
  pinMode(X_DIR_PIN, OUTPUT);
  digitalWrite(X_ENABLE_PIN, LOW);

  RA_stepper.setup_pins();
  
  dir_forward = true;
  motor_position = 0;
  desired_position = 0;
  
  Serial.begin(115200);
}

void step_motor(){
  delay(50);
  digitalWrite(X_STEP_PIN, HIGH);
  delay(50);
  digitalWrite(X_STEP_PIN, LOW);
}

void enable_motor(){
  digitalWrite(X_ENABLE_PIN, LOW);
}

void disable_motor(){
  digitalWrite(X_ENABLE_PIN, HIGH);
}

void change_dir(bool const forward){
  bool const tmp_dir = dir_forward;
  dir_forward = forward;
  if (tmp_dir != dir_forward){ 
    digitalWrite(X_DIR_PIN, (dir_forward ? HIGH : LOW));
  }
}

void blink_led(){
  delay(50);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(50);
  digitalWrite(LED_BUILTIN, LOW);
}

void set_position(int const new_position){
  int const delta = new_position - desired_position;
  desired_position = new_position;
  bool const is_forward = (delta > 0);
  change_dir(is_forward);
}

void handle_serial(){
  memset(command_string, 0, COMMAND_MAX_LENGTH);
  memset(command_name, 0, COMMAND_NAME_LENGTH);
  int command_argument = 0;
  
  Serial.readBytesUntil('\n', command_string, COMMAND_MAX_LENGTH);
  sscanf(command_string, "%s %d", command_name, &command_argument);
  if (0 == strcmp(command_name, "HALT")){
    set_position(motor_position);
  }else if (0 == strcmp(command_name, "RA_POSITION")){
    RA_stepper.print_position(Serial);
  }else if (0 == strcmp(command_name, "RA_MOVE_ABS")){
    RA_stepper.set_position_absolute(command_argument);
  }else if (0 == strcmp(command_name, "RA_MOVE_REL")){
    RA_stepper.set_position_relative(command_argument);
  }else if (0 == strcmp(command_name, "POSITION")){
    Serial.print("CURRENT ");
    Serial.print(motor_position);
    Serial.print(" DESIRED ");
    Serial.println(desired_position);
  }else if (0 == strcmp(command_name, "MOVE")){
    int const new_position = motor_position + command_argument;
    set_position(new_position);
  }else{
    Serial.print("UNKNOWN COMMAND: ");
    Serial.print(command_string);
    Serial.println("!");    
  }
}

void move_if_needed(){
  int const increment = (dir_forward ? 1 : -1);
  
  if (desired_position != motor_position){
    if (!is_enabled){
      enable_motor();
      is_enabled = true;
    }
    step_motor();
    motor_position += increment;
  }
  else{
    if (is_enabled){
      disable_motor();
      is_enabled = false;
    }
    delay(100);
  }
}

void loop() {
  if (Serial.available()){
    handle_serial();
  }
  else{
    move_if_needed();
  }
}
