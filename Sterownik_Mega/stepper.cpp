#include "stepper.h"
#include <Arduino.h>

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

void Stepper::move_if_needed(){
  if (_desired_position != _motor_position){
    if (!_is_enabled){
      enable_motor();
    }
    step_motor();
  }
  else{
    if (_is_enabled){
      disable_motor();
    }
    delay(100);
  }
}

void Stepper::step_motor(uint16_t delay_ms/* =50*/){
  delay(delay_ms);
  digitalWrite(_step_pin, HIGH);
  delay(delay_ms);
  digitalWrite(_step_pin, LOW);
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

