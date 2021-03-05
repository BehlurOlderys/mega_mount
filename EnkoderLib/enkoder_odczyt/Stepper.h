#ifndef BHS_STEPPER_H
#define BHS_STEPPER_H

#include <stdint.h>
#include "Serializer.h"

uint32 const MINIMAL_STATIC_VALUE_OF_STEPPING_DELAY_US = 1000; // 1ms is safe for starting from 0
uint32 const MINIMAL_DYNAMIC_VALUE_OF_STEPPING_DELAY_US = 50; // 50us is safe to drive
bool const DESIRED_POSITION_REACHED = true;
bool const DESIRED_POSITION_NOT_REACHED = false;

struct Stepper{
       Stepper(uint8_t const step_pin, uint8_t const dir_pin, uint8_t const en_pin);
  void halt();
  bool is_enabled() const;
  void setup_pins();
  void set_position_absolute(int32_t const new_position);  
  void set_position_relative(int32_t const position_delta);
  
  void runnable_slew_to_desired();
  void step_motor();
  template <typename Printer>
  void print_position(Printer& printer){
    printer.print("CURRENT ");
    printer.print(_motor_position);
    printer.print(" DESIRED ");
    printer.println(_desired_position);
  }
private:
  void enable_motor();
  void disable_motor();
  void change_dir(bool const forward);
  
  uint8_t const _step_pin;
  uint8_t const _dir_pin;
  uint8_t const _en_pin;

  int16_t _delay_us;
  bool    _dir_forward;
  int32_t _motor_position;
  int32_t _desired_position;
  bool    _is_enabled;
};

#endif  // BHS_STEPPER_H
