#ifndef BHS_SERIALIZER_H
#define BHS_SERIALIZER_H

#include "Arduino.h"

template <typename DataType>
uint8_t type_id();

uint8_t const UNSPECIFIED_TYPE_ID = 255;

template <typename SerialType, typename DataType>
void PrintToSerial(SerialType& serial, DataType const& data){
  serial.println("BHS");
  serial.println(micros());
  serial.println(UNSPECIFIED_TYPE_ID);
  serial.println(data);
}

template <typename SerialType, typename DataType>
void Serialize(SerialType& serial, DataType const& data){
  char data_array[sizeof(DataType)];
  memcpy(data_array, &data, sizeof(DataType));
  serial.println("BHS");
  serial.println(micros());
  serial.println(type_id<DataType>());
  serial.println(sizeof(DataType));
  serial.write(data_array, sizeof(DataType));
  serial.println();
}
#endif  // BHS_SERIALIZER_H
