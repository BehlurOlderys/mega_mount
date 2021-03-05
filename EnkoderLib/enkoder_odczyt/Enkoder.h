#ifndef BHS_ENKODER_H
#define BHS_ENKODER_H

#include <Arduino.h>
#include "Serializer.h"

static int8_t const ENCODER_NAME_SIZE = 4u;
static int8_t const ENCODER_TYPE_ID = 1u;

struct Enkoder{
              Enkoder(int8_t channel_a_pin, int8_t channel_b_pin, const char* name_str);
  int32_t     get_current_position() const;
  const char* get_name() const;
  void        reset_encoder();
  void        setup_encoder();
  void        update_position();
  template <typename Printer>
  void        print_to(Printer& printer) const;

  int8_t const _channel_a_pin;
  int8_t const _channel_b_pin;
  int32_t      _current_position;
  int8_t      _previous_index;
  uint32_t    _last_timestamp;
  char        _only_four_letters_name[ENCODER_NAME_SIZE+1];
};

struct EncoderDebugData{
  EncoderDebugData(const char* encoder_four_letter_name) : _name{0} {
    memcpy(_name, encoder_four_letter_name, sizeof(_name));
  }
  int32_t _position;
  uint32_t _timestamp;
  char _name[ENCODER_NAME_SIZE];
};

template <>
uint8_t type_id<EncoderDebugData>(){ return ENCODER_TYPE_ID; }

#endif  // BHS_ENKODER_H
