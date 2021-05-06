#ifndef BHS_ABSOLUTE_ENCODER_H
#define BHS_ABSOLUTE_ENCODER_H
#include "Arduino.h"
#include "Serializer.h"

static int8_t const ABSOLUTE_ENCODER_NAME_SIZE = 4u;
static int8_t const ABSOLUTE_ENCODER_TYPE_ID = 3u;
static int8_t const NUMBER_OF_BITS = 12;

struct AbsoluteEncoderDebugData{
  AbsoluteEncoderDebugData(const char* four_letter_name);
  uint16_t _position;
  char _name[ABSOLUTE_ENCODER_NAME_SIZE];
};

struct AbsoluteEncoder{
  AbsoluteEncoder(int8_t CSn_pin, int8_t DO_pin, int8_t CLK_pin, const char* name_str);
  void setup_encoder();
  uint16_t get_position();

  template <typename Printer>
    void        print_to(Printer& printer) const{
      AbsoluteEncoderDebugData data_to_serialize(_only_four_letters_name);
      data_to_serialize._position = _current_position;
      Serialize(printer, data_to_serialize);
    }

  int8_t const _csn_pin;
  int8_t const _do_pin;
  int8_t const _clk_pin;
  uint16_t _current_position;
  char        _only_four_letters_name[ABSOLUTE_ENCODER_NAME_SIZE+1];
};

#endif // BHS_ABSOLUTE_ENCODER_H
