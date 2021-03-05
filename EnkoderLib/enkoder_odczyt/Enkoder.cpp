#include "Enkoder.h"

static int8_t const BAD = 0;
static int8_t const table_of_states[4][4] = {
  {  0,   1,  -1, BAD},  
  { -1,   0, BAD,   1},
  {  1, BAD,   0,  -1},
  {BAD,  -1,   1,   0}
};

Enkoder::Enkoder(int8_t channel_a_pin, int8_t channel_b_pin, const char* name_str):
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

int32_t Enkoder::get_current_position() const {
  return _current_position;
}

const char* Enkoder::get_name() const {
  return _only_four_letters_name;
}  

void Enkoder::reset_encoder(){
  _current_position = 0;
  _last_timestamp = 0;
}

void Enkoder::setup_encoder(){
  pinMode(_channel_a_pin, INPUT_PULLUP);
  pinMode(_channel_b_pin, INPUT_PULLUP);
  reset_encoder();
}

void Enkoder::update_position(){
  uint8_t const channelA = uint16_t(analogRead(_channel_a_pin) > 512);
  uint8_t const channelB = uint16_t(analogRead(_channel_b_pin) > 512);
  uint8_t const current_index = 2*channelA + channelB;
  int8_t const position_progress = table_of_states[_previous_index][current_index];
  _previous_index = current_index;
  _current_position += position_progress;
  _last_timestamp = micros();
}

EncoderDebugData::EncoderDebugData(const char* encoder_four_letter_name) :
  _name{0} 
{
  memcpy(_name, encoder_four_letter_name, sizeof(_name));
}


