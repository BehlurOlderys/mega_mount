#ifndef BHS_ENKODER_H
#define BHS_ENKODER_H

#include <Arduino.h>
#include "Serializer.h"

static int8_t const ENCODER_NAME_SIZE = 4u;
static int8_t const ENCODER_TYPE_ID = 1u;


struct EncoderDebugData{
  EncoderDebugData(const char* encoder_four_letter_name);
  int32_t _position;
  uint32_t _timestamp;
  char _name[ENCODER_NAME_SIZE];
};

struct Enkoder{
              Enkoder(int8_t channel_a_pin, int8_t channel_b_pin, const char* name_str);
  int32_t     get_current_position() const;
  const char* get_name() const;
  void        reset_encoder();
  void        setup_encoder();
  void        update_position();
  template <typename Printer>
  void        print_to(Printer& printer) const{
    EncoderDebugData data_to_serialize(_only_four_letters_name);
    data_to_serialize._position = _current_position;
    data_to_serialize._timestamp = _last_timestamp;
    Serialize(printer, data_to_serialize);
  }


  int8_t const _channel_a_pin;
  int8_t const _channel_b_pin;
  int32_t      _current_position;
  int8_t      _previous_index;
  uint32_t    _last_timestamp;
  char        _only_four_letters_name[ENCODER_NAME_SIZE+1];
};

#endif  // BHS_ENKODER_H
