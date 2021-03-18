#ifndef BHS_SERIALIZER_H
#define BHS_SERIALIZER_H

template <typename DataType>
uint8_t type_id(){ return 2; }

template <typename SerialType, typename DataType>
void Serialize(SerialType& serial, DataType const& data){
  char data_array[sizeof(DataType)];
  memcpy(data_array, &data, sizeof(DataType));
  serial.println("BHS");
  serial.println(type_id<DataType>());
  serial.println(sizeof(DataType));
  serial.write(data_array, sizeof(DataType));
  serial.println();
}
#endif  // BHS_SERIALIZER_H
