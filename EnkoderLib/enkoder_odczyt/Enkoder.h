#include <Arduino.h>
#include "Serializer.h"

int8_t const BAD = 0;
int8_t const table_of_states[4][4] = {
  {  0,   1,  -1, BAD},  
  { -1,   0, BAD,   1},
  {  1, BAD,   0,  -1},
  {BAD,  -1,   1,   0}
};


static int8_t const ENCODER_NAME_SIZE = 4u;

struct Enkoder{
  Enkoder(int8_t channel_a_pin, int8_t channel_b_pin, const char* name_str):
    _channel_a_pin(channel_a_pin),
    _channel_b_pin(channel_b_pin),
    _current_position(0),
    _previous_index(0),
    _last_timestamp(0),
    _only_four_letters_name()
  {
    memset(_only_four_letters_name, 0, sizeof(_only_four_letters_name));
    strncpy(_only_four_letters_name, name_str, ENCODER_NAME_SIZE);
  }

  int32_t get_current_position() const {
    return _current_position;
  }

  const char* get_name() const {
    return _only_four_letters_name;
  }  

  void reset_encoder(){
    _current_position = 0;
    _last_timestamp = 0;
  }

  void setup_encoder(){
    pinMode(_channel_a_pin, INPUT_PULLUP);
    pinMode(_channel_b_pin, INPUT_PULLUP);
    reset_encoder();
  }

  void update_position(){
    uint8_t const channelA = uint16_t(analogRead(_channel_a_pin) > 512);
    uint8_t const channelB = uint16_t(analogRead(_channel_b_pin) > 512);
    uint8_t const current_index = 2*channelA + channelB;
    int8_t const position_progress = table_of_states[_previous_index][current_index];
    _previous_index = current_index;
    _current_position += position_progress;
    _last_timestamp = micros();
  }
  
  template <typename Printer>
  void print_to(Printer& printer) const {
    EncoderDebugData data_to_serialize("RAEN");
    data_to_serialize._position = _current_position;
    data_to_serialize._timestamp = _last_timestamp;
    Serialize(printer, data_to_serialize);
  }

  int8_t const _channel_a_pin;
  int8_t const _channel_b_pin;
  int32_t _current_position;
  int8_t _previous_index;
  uint32_t _last_timestamp;
  char _only_four_letters_name[ENCODER_NAME_SIZE+1];
};

static int8_t const ENCODER_TYPE_ID = 1u;

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

