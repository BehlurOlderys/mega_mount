#include "Stepper.h"
#include <Arduino.h>

Stepper::Stepper(uint8_t const step_pin, uint8_t const dir_pin, uint8_t const en_pin, const char* name_short):
   _step_pin(step_pin),
   _dir_pin(dir_pin),
   _en_pin(en_pin),
   _delay_us(MINIMAL_STATIC_VALUE_OF_STEPPING_DELAY_US),
   _dir_forward(true),
   _motor_position(0),
   _desired_position(0),
   _is_enabled(false),
   _only_four_letters_name()
{  
  memset(_only_four_letters_name, 0, sizeof(_only_four_letters_name));
  strncpy(_only_four_letters_name, name_short, STEPPER_NAME_SIZE);
}

void Stepper::halt(){
  set_position_absolute(_motor_position);
  disable_motor();
}

bool Stepper::is_enabled() const {
  return _is_enabled;
}
void Stepper::setup_pins(){
  pinMode(_step_pin, OUTPUT);
  pinMode(_dir_pin, OUTPUT);
  pinMode(_en_pin, OUTPUT);
  digitalWrite(_en_pin, LOW);
}

void Stepper::set_position_absolute(int32_t const new_position){
  int32_t const delta = new_position - _desired_position;
  _desired_position = new_position;
  bool const is_forward = (delta > 0);
  change_dir(is_forward);
}

void Stepper::set_position_relative(int32_t const position_delta){
  int32_t const new_position = _motor_position + position_delta;
  set_position_absolute(new_position);
}

const char* Stepper::get_name() const {
  return _only_four_letters_name;
}  

bool Stepper::runnable_slew_to_desired(){
  if (_desired_position != _motor_position){
    step_motor();
    return DESIRED_POSITION_NOT_REACHED;
  }
  return DESIRED_POSITION_REACHED;
}

void Stepper::step_motor(){
  digitalWrite(_step_pin, HIGH);
  delayMicroseconds(_delay_us);
  digitalWrite(_step_pin, LOW);
  delayMicroseconds(_delay_us);
  int32_t const increment = (_dir_forward ? 1 : -1);
  _motor_position += increment;
}

void Stepper::enable_motor(){
  digitalWrite(_en_pin, LOW);
  _is_enabled = true;
}

void Stepper::disable_motor(){
  digitalWrite(_en_pin, HIGH);
  _is_enabled = false;
}

void Stepper::change_dir(bool const forward){
  if (forward == _dir_forward){
    return;
  }
  _dir_forward = forward;
  digitalWrite(_dir_pin, (_dir_forward ? HIGH : LOW));
}

