#include "Stepper.h"
#include "AbsoluteEncoder.h"
#include "Arduino.h"
#include "mega_pins.h"

// defines for setting and clearing register bits
#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif

void set_fast_adc(){ 
  // set prescale to 16
  sbi(ADCSRA,ADPS2) ;
  cbi(ADCSRA,ADPS1) ;
  cbi(ADCSRA,ADPS0) ;
}

enum RaStateType{
  TRACKING,
  NOT_TRACKING
};

//enum RaEnkoderStateType{
//  FEEDBACK_OFF,
//  FEEDBACK_ON,
//  FEEDBACK_PAUSED
//};


static uint32_t const ra_calculated_delay_us = 19986;

uint32_t GetTrackingDelayUs(){
  return ra_calculated_delay_us;
}
uint32_t ra_expected_interval_us = GetTrackingDelayUs();
uint32_t ra_last_step_us = 0;
RaStateType ra_state;


const uint8_t COMMAND_MAX_LENGTH = 20;
const uint8_t COMMAND_NAME_LENGTH = 10;
char command_string[COMMAND_MAX_LENGTH];
char command_name[COMMAND_NAME_LENGTH];
char command_trash[COMMAND_MAX_LENGTH];

Stepper stepper_ra(Y_STEP_PIN, Y_DIR_PIN, Y_ENABLE_PIN, "STRA");
Stepper stepper_focuser(X_STEP_PIN, X_DIR_PIN, X_ENABLE_PIN, "FOCU");
Stepper stepper_de(Z_STEP_PIN, Z_DIR_PIN, Z_ENABLE_PIN, "STDE");

void handle_unknown_command(){
  Serial.println("BHS");
  Serial.print("UNKNOWN COMMAND: ");
  Serial.print(command_string);
  Serial.println("!");
}

//RaEnkoderStateType encoder_ra_state = FEEDBACK_ON;
//int32_t ra_encoder_expected_position = 0;
//uint32_t last_ra_feedback_time_us = 0;
//uint32_t expected_ra_feedback_interval_us = RA_Encoder_Step_Period_us;

//void StartEncoderRAFeedback(){
//  enkoder_ra.reset_encoder();
//  ra_encoder_expected_position = 0;
//  encoder_ra_state = FEEDBACK_ON;
//  last_ra_feedback_time_us = micros();
//  expected_ra_feedback_interval_us = RA_Encoder_Step_Period_us;
//}
//
//void PauseEncoderRAFeedback(){
//  encoder_ra_state = FEEDBACK_PAUSED;
//}
//
//void StopEncoderRAFeedback(){
//  encoder_ra_state = FEEDBACK_OFF;
//}


void StartTrackingRA(){
  stepper_ra.change_dir(FORWARD_DIRECTION);
  ra_expected_interval_us = GetTrackingDelayUs();
  ra_state = TRACKING;
  ra_last_step_us = micros();
//  StartEncoderRAFeedback();
}

void StopTrackingRA(){
  ra_state = NOT_TRACKING;
//  StopEncoderRAFeedback();
}

void StartRaStepperMove(int const command_argument){
//  if (encoder_ra_state == FEEDBACK_ON){
//    PauseEncoderRAFeedback();
//  }
  bool const move_forward = (command_argument > 0);
  stepper_ra.change_dir(move_forward);
  stepper_ra.start_moving();
}

void StopRaStepperMove(){
//  if (encoder_ra_state == FEEDBACK_PAUSED){
//    StartEncoderRAFeedback();
//  }
  stepper_ra.stop_moving();
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
    StartRaStepperMove(command_argument);
  }else if (0 == strcmp(command_name, "RA_STOP")){
    StopRaStepperMove();    
  }else if (0 == strcmp(command_name, "RA_ENCO_ON")){
//    StartEncoderRAFeedback();    
  }else if (0 == strcmp(command_name, "RA_ENCO_OFF")){
//    StopEncoderRAFeedback();    
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
    Serial.println("BHS");
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

//void BoundEncoderRaUpdateRunnable(){
//  enkoder_ra.runnable_update_position();
//}

//int encoder_ra_print_counter = 0;
int step_ra_print_counter = 0;
int step_de_print_counter = 0;


//void BoundEncoderRaPrintRunnable(){
//  if (encoder_ra_print_counter >= 1000){
//    enkoder_ra.print_to(Serial);
//    encoder_ra_print_counter = 0;
//  }
//  encoder_ra_print_counter++;
//}

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

uint32_t SafelySubtractWrappedU32(uint32_t const A, uint32_t const B){
  if (B > A){
    uint32_t const complement = UINT32_MAX - B;
    return A + complement;
  }
  return A - B;
}

struct StepperDirectionSentinel{
  StepperDirectionSentinel(Stepper& guarded) : _guarded(guarded), _dir(guarded.is_forward()) {}
  ~StepperDirectionSentinel(){
    _guarded.change_dir(_dir);
  }
  Stepper& _guarded;
  bool const _dir;
};

//const int32_t RA_Encoder_Direction = -1;

//void PerformRACorrections(){
//  int32_t const current_position = enkoder_ra.get_current_position()*RA_Encoder_Direction;
//  int32_t const position_delta = ra_encoder_expected_position - current_position;
//  bool const should_stepper_be_moved = abs(position_delta) > 0;
//  if (!should_stepper_be_moved){
//    return;
//  }
//  bool const is_stepper_behind_encoder = (position_delta > 0);
//  bool const should_stepper_go_forward = is_stepper_behind_encoder;
//
//  static uint32_t counter=0;
//  counter++;
//  if (counter > 100){
//    // FO_LOW_CUR_ON
//    // RA_ENCO_ON
//    // RA_TRACK_ON
//    
////    Serial.print("Expected position = ");
////    Serial.print(ra_encoder_expected_position);
////    Serial.print(", Current position = ");
////    Serial.println(current_position);
////    counter = 0;
//  }
 
//  StepperDirectionSentinel dir_sentinel(stepper_ra);
//  stepper_ra.change_dir(should_stepper_go_forward);
//  stepper_ra.step_motor();
//}

//void BoundRaFeedback(){
//  if (!encoder_ra_state == FEEDBACK_ON){
//    return;
//  }
//  if (ra_state != TRACKING){
//    return;
//  }
//  uint32_t const current_us = micros();
//  uint32_t current_interval_us = SafelySubtractWrappedU32(current_us, last_ra_feedback_time_us);

//  static uint32_t counter = 0;
//  if (counter == 100){
//    Serial.print("current_interval_us = ");
//    Serial.print(current_interval_us);
//    Serial.print(", expected interval us = ");
//    Serial.println(expected_ra_feedback_interval_us);
//    
//    counter = 0;
//  }
//  counter++;
  
//  if(current_interval_us >= expected_ra_feedback_interval_us){
//    ra_encoder_expected_position++;
//    last_ra_feedback_time_us = current_us;
//    expected_ra_feedback_interval_us = RA_Encoder_Step_Period_us + expected_ra_feedback_interval_us - current_interval_us;
//  }
//  PerformRACorrections();
//}

void BoundStepperRaStepSidereal(){
  if (ra_state != TRACKING){
    return;
  }
  bool const is_forward = stepper_ra.is_forward();
  if (!stepper_ra.is_forward()){
    stepper_ra.change_dir(FORWARD_DIRECTION);
  }
  uint32_t const current_us = micros();
  uint32_t const current_interval_us = current_us - ra_last_step_us;
  if(current_interval_us >= ra_expected_interval_us){
    stepper_ra.step_motor();
    ra_last_step_us = current_us;
    ra_expected_interval_us = GetTrackingDelayUs() + ra_expected_interval_us - current_interval_us;
  }
  stepper_ra.change_dir(is_forward);
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
  BoundStepperRaStepSidereal();
  BoundStepperFocuserSlew();
  BoundStepperRaSlew();
  BoundStepperDecSlew();
//  BoundStepperRaPrintRunnable();
//  BoundStepperDecPrintRunnable();
//  
//  BoundEncoderRaUpdateRunnable();
//  BoundRaFeedback();
  BoundStepperRaMove();
  BoundStepperDecMove();
//  BoundEncoderRaPrintRunnable();
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
  stepper_de.set_delay_us(100);
  set_fast_adc();
}

void loop() {
  if (Serial.available()){
    handle_serial();
  }
  handle_runnables();
  handle_events();
}
