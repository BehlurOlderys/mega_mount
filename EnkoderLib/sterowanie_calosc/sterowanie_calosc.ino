#include "Stepper.h"
#include "Enkoder.h"
#include "Arduino.h"
#include "Config.h"

enum RaStateType{
  TRACKING,
  NOT_TRACKING
};


static uint32_t const ra_calculated_delay_us = 19986;
uint32_t ra_expected_interval_us = ra_calculated_delay_us;

uint32_t ra_last_step_us = 0;

RaStateType ra_state;

const uint8_t X_STEP_PIN = 54;  // A9
const uint8_t X_ENABLE_PIN = 38;
const uint8_t X_DIR_PIN = 55;

const uint8_t Y_STEP_PIN = 60;
const uint8_t Y_DIR_PIN = 61;
const uint8_t Y_ENABLE_PIN = 56;

const uint8_t Z_STEP_PIN = 46;
const uint8_t Z_DIR_PIN = 48;
const uint8_t Z_ENABLE_PIN = 62;

const uint8_t AUX_A_PIN = A1;// TODO! for mega!
const uint8_t AUX_B_PIN = A2; // TODO!

const uint8_t COMMAND_MAX_LENGTH = 20;
const uint8_t COMMAND_NAME_LENGTH = 10;
char command_string[COMMAND_MAX_LENGTH];
char command_name[COMMAND_NAME_LENGTH];
char command_trash[COMMAND_MAX_LENGTH];

Enkoder enkoder_ra(AUX_A_PIN, AUX_B_PIN, "ENRA");
Stepper stepper_ra(Y_STEP_PIN, Y_DIR_PIN, Y_ENABLE_PIN, "STRA");
Stepper stepper_focuser(X_STEP_PIN, X_DIR_PIN, X_ENABLE_PIN, "FOCU");
Stepper stepper_de(Z_STEP_PIN, Z_DIR_PIN, Z_ENABLE_PIN, "STDE");

void handle_unknown_command(){
  Serial.print("UNKNOWN COMMAND: ");
  Serial.print(command_string);
  Serial.println("!");  
}

void StartTrackingRA(){
  ra_expected_interval_us = ra_calculated_delay_us;
  ra_state = TRACKING;
  ra_last_step_us = micros();
}

void StopTrackingRA(){
  ra_state = NOT_TRACKING;
}

void handle_serial(){
  memset(command_string, 0, COMMAND_MAX_LENGTH);
  memset(command_name, 0, COMMAND_NAME_LENGTH);
  int command_argument = 0;
  
  Serial.readBytesUntil('\n', command_string, COMMAND_MAX_LENGTH);
  sscanf(command_string, "%s %d", command_name, &command_argument);
  // RIGHT ASCENSION AXIS:
  if       (0 == strcmp(command_name, "RA_HALT")){
    stepper_ra.halt();
  }else if (0 == strcmp(command_name, "RA_POSITION")){
    stepper_ra.print_to(Serial);
  }else if (0 == strcmp(command_name, "RA_MOVE")){
    bool const move_forward = (command_argument > 0);
    stepper_ra.change_dir(move_forward);
    stepper_ra.start_moving();
  }else if (0 == strcmp(command_name, "RA_STOP")){
    stepper_ra.stop_moving();
  }else if (0 == strcmp(command_name, "RA_SLEW_ABS")){
    // todo
  }else if (0 == strcmp(command_name, "RA_SLEW_REL")){
    stepper_ra.set_position_relative(command_argument);
  }else if (0 == strcmp(command_name, "RA_TRACK_ON")){
    StartTrackingRA();
  }else if (0 == strcmp(command_name, "RA_TRACK_OFF")){
    StopTrackingRA();
  }else if (0 == strcmp(command_name, "IS_TRACKING")){
    bool const is_tracking = (TRACKING == ra_state);
    Serial.println(is_tracking);
  } // DECLINATION AXIS:
   else if (0 == strcmp(command_name, "DE_HALT")){
    stepper_de.halt();
  }else if (0 == strcmp(command_name, "DE_MOVE")){
    bool const move_forward = (command_argument > 0);
    stepper_de.change_dir(move_forward);
    stepper_de.start_moving();
  }else if (0 == strcmp(command_name, "DE_STOP")){
    stepper_de.stop_moving();
  }else if (0 == strcmp(command_name, "DE_POSITION")){
    stepper_de.print_to(Serial);
  }else if (0 == strcmp(command_name, "DE_MOVE_ABS")){
    // todo
  }else if (0 == strcmp(command_name, "DE_MOVE_REL")){
    stepper_de.set_position_relative(command_argument);
  } // FOCUSER:
   else if (0 == strcmp(command_name, "FO_POSITION")){
    stepper_focuser.print_to(Serial);
  }else if (0 == strcmp(command_name, "FO_HALT")){
    stepper_focuser.halt();
  }else if (0 == strcmp(command_name, "FO_MOVE_REL")){
    stepper_focuser.set_position_relative(command_argument);
  }else if (0 == strcmp(command_name, "FO_LOW_CUR_ON")){
    stepper_focuser.go_to_low_current_halt();
  }else if (0 == strcmp(command_name, "FO_LOW_CUR_OFF")){
    stepper_focuser.go_to_normal_operation();
  }else{
    handle_unknown_command();  
  }
}

void BoundEncoderRaUpdateRunnable(){
  enkoder_ra.runnable_update_position();
}

int encoder_ra_print_counter = 0;
int step_ra_print_counter = 0;
int step_de_print_counter = 0;


void BoundEncoderRaPrintRunnable(){
  if (encoder_ra_print_counter >= 1000){
    enkoder_ra.print_to(Serial);
    encoder_ra_print_counter = 0;
  }
  encoder_ra_print_counter++;
}

void BoundStepperRaPrintRunnable(){
  if (step_ra_print_counter >= 1000){
    stepper_ra.print_to(Serial);
    step_ra_print_counter = 0;
  }
  step_ra_print_counter++;
}

void BoundStepperDecPrintRunnable(){
  if (step_de_print_counter >= 1000){
    stepper_de.print_to(Serial);
    step_de_print_counter = 0;
  }
  step_de_print_counter++;
}

void BoundStepperRaStepSidereal(){
  if (ra_state != TRACKING){
    return;
  }
  uint32_t const current_us = micros();
  uint32_t const current_interval_us = current_us - ra_last_step_us;
  if(current_interval_us >= ra_expected_interval_us){
    stepper_ra.step_motor();
    ra_last_step_us = current_us;
    ra_expected_interval_us = ra_calculated_delay_us + ra_expected_interval_us - current_interval_us;
  }
}

void BoundStepperRaSlew(){
  if (!stepper_ra.is_slewing()){
    return;
  }
  stepper_ra.runnable_slew_to_desired();
}

void BoundStepperRaMove(){
  if (!stepper_ra.is_moving()){
    return;
  }
  stepper_ra.runnable_move();
}

void BoundStepperDecMove(){
  if (!stepper_de.is_moving()){
    return;
  }
  stepper_de.runnable_move();
}

void BoundStepperFocuserSlew(){
  if (!stepper_focuser.is_slewing()){
    return;
  }
  stepper_focuser.runnable_slew_to_desired();
}

void BoundStepperDecSlew(){
  if (!stepper_de.is_slewing()){
    return;
  }
  stepper_de.runnable_slew_to_desired();
}

void handle_runnables(){
  BoundStepperFocuserSlew();
  BoundStepperRaSlew();
  BoundStepperDecSlew();
//  BoundStepperRaPrintRunnable();
//  BoundStepperDecPrintRunnable();
//  
//  BoundEncoderRaPrintRunnable();
//  BoundEncoderRaUpdateRunnable();
  BoundStepperRaStepSidereal();
  BoundStepperRaMove();
  BoundStepperDecMove();
}

void handle_events(){
  
}

void setup() {
  Serial.begin(115200);
//  enkoder_ra.setup_encoder();
  stepper_ra.setup_pins();
  stepper_de.setup_pins();
  stepper_focuser.setup_pins();
  ra_last_step_us = micros();
  ra_state = NOT_TRACKING;
  stepper_ra.set_delay_us(100);
  stepper_de.set_delay_us(1000);
}

void loop() {
  if (Serial.available()){
    handle_serial();
  }
  handle_runnables();
  handle_events();
}
