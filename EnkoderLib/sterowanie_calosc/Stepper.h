#ifndef BHS_STEPPER_H
#define BHS_STEPPER_H

#include <stdint.h>
#include "Serializer.h"

uint16_t const MINIMAL_STATIC_VALUE_OF_STEPPING_DELAY_US = 1000; // 1ms is safe for starting from 0
uint16_t const MINIMAL_DYNAMIC_VALUE_OF_STEPPING_DELAY_US = 50; // 50us is safe to drive
bool const DESIRED_POSITION_REACHED = true;
bool const DESIRED_POSITION_NOT_REACHED = false;
uint8_t const STEPPER_NAME_SIZE = 4u;
static int8_t const STEPPER_TYPE_ID = 2u;


struct StepperDebugData{
  StepperDebugData(const char* stepper_four_letter_name);
  int32_t _motor_position;
  int32_t _desired_position;
  uint16_t _delay_us;
  bool    _dir_forward;
  bool    _is_enabled;  
  bool    _is_slewing;  
  char    _name[STEPPER_NAME_SIZE];
};


struct Stepper{
       Stepper(uint8_t const step_pin, uint8_t const dir_pin, uint8_t const en_pin, const char* name_short);
  void halt();
  bool is_enabled() const;
  bool is_slewing() const;
  bool is_moving() const;
  void setup_pins();
  void set_delay_us(uint32_t const delay_us);
  void set_position_absolute(int32_t const new_position);  
  void set_position_relative(int32_t const position_delta);
  const char* get_name() const;

  void go_to_low_current_halt();
  void go_to_normal_operation();
  void change_dir(bool const forward);
  void start_moving();
  void stop_moving();
  void runnable_move();
  bool runnable_slew_to_desired();
  void step_motor();
  template <typename Printer>
  void print_to(Printer& printer) const{
    StepperDebugData data_to_serialize(_only_four_letters_name);
    data_to_serialize._delay_us = _delay_us;
    data_to_serialize._dir_forward = _dir_forward;
    data_to_serialize._motor_position = _motor_position;
    data_to_serialize._desired_position = _desired_position;
    data_to_serialize._is_enabled = _is_enabled;
    data_to_serialize._is_slewing = _is_slewing;  
    Serialize(printer, data_to_serialize);
  }
private:
  void enable_motor();
  void disable_motor();
  
  uint8_t const _step_pin;
  uint8_t const _dir_pin;
  uint8_t const _en_pin;

  uint16_t _delay_us;
  bool    _dir_forward;
  int32_t _motor_position;
  int32_t _desired_position;
  bool    _is_enabled;  
  bool    _is_slewing;
  bool    _is_moving;
  char    _only_four_letters_name[STEPPER_NAME_SIZE+1];
};

#endif  // BHS_STEPPER_H
