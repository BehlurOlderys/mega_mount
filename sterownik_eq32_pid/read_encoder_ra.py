import serial
import sys
from struct import unpack

ENCODER_TYPE_ID = 1


def deserialize_encoder(raw_payload, logger):
    (position, timestamp, raw_name) = unpack("iI4s", raw_payload)
    name = raw_name.decode('UTF-8').strip()
    ### logger part to be refactored! ###
    logger.write(f"{timestamp},{position},{raw_name},\n")
    print(f"Name = {name}, position = {position}, timestamp = {timestamp}")
    #####################################
    return position, timestamp, name


map_of_deserializers = {
  ENCODER_TYPE_ID: deserialize_encoder
}


def unpack_type(type_id, raw_payload):
    deserializer = map_of_deserializers[type_id]
    return deserializer(raw_payload)


class SerialReader:
    def __init__(self):
        self.log_file = open("log_file_fast.txt", "w", buffering=1)
        self.ser = serial.Serial(
            port='COM3',
            baudrate=115200
        )

        self.current_position = 0
        self.current_time = 0
        self.previous_signals = None
        self.current_error = 0

    def __del__(self):
        self.log_file.close()

    def loop(self):
        while True:
            try:
                message = self.ser.readline().decode('UTF-8').rstrip()
                if "BHS" == message:
                    type_id = int(self.ser.readline())
                    data_size = int(self.ser.readline())
                    raw_payload = self.ser.read(data_size)
                    unpack_type(type_id, raw_payload, self.log_file)

            except Exception as e:
                print("Exception: " + str(e))
                continue

            sys.stdout.write(f"\rmessage = {message}     ")
            sys.stdout.flush()


reader = SerialReader()
reader.loop()

