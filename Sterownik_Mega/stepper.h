#ifndef STEROWNIK_MEGA_STEPPER_H
#define  STEROWNIK_MEGA_STEPPER_H

#include <stdint.h>

struct Stepper{
  Stepper(uint8_t const step_pin, uint8_t const dir_pin, uint8_t const en_pin):
     _step_pin(step_pin),
     _dir_pin(dir_pin),
     _en_pin(en_pin),
     _dir_forward(true),
     _motor_position(0),
     _desired_position(0),
     _is_enabled(false)
  {  
  }

public:  
  bool is_enabled() const;
  void setup_pins();
  void set_position_absolute(int32_t const new_position);  
  void set_position_relative(int32_t const position_delta);
  void move_if_needed();
  template <typename Printer>
  void print_position(Printer& printer){
    printer.print("CURRENT ");
    printer.print(_motor_position);
    printer.print(" DESIRED ");
    printer.println(_desired_position);
  }
private:
  void step_motor(uint16_t delay_ms=50);
  void enable_motor();
  void disable_motor();
  void change_dir(bool const forward);
  
  uint8_t const _step_pin;
  uint8_t const _dir_pin;
  uint8_t const _en_pin;
  
  bool    _dir_forward;
  int32_t _motor_position;
  int32_t _desired_position;
  bool    _is_enabled;
};

#endif  //  STEROWNIK_MEGA_STEPPER_H
