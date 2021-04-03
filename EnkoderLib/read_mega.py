import serial
import sys
from struct import unpack

ENCODER_TYPE_ID = 1
STEPPER_TYPE_ID = 2


def deserialize_encoder(raw_payload, logger):
    (position, timestamp, raw_name) = unpack("iI4s", raw_payload)
    name = raw_name.decode('UTF-8').strip()
    ### logger part to be refactored! ###
    logger.write(f"{raw_name},{timestamp},{position},\n")
    print(f"Name = {name}, position = {position}, timestamp = {timestamp}")
    #####################################
    return position, timestamp, name


def deserialize_stepper(raw_payload, logger):
    (delay, direction, position, desired, is_enabled, is_slewing, raw_name) = unpack("i?II??4s", raw_payload)
    name = raw_name.decode('UTF-8').strip()
    logger.write(f"{raw_name},{delay},{direction},{position},{desired},{is_enabled},{is_slewing},\n")
    print(f"Name = {name}, is_slewing = {is_slewing}, direction_forward = {direction}")
    #####################################
    return position, is_slewing, direction

map_of_deserializers = {
  ENCODER_TYPE_ID: deserialize_encoder,
  # STEPPER_TYPE_ID: deserialize_stepper
}


def unpack_type(type_id, raw_payload, logger):
    if type_id == 2:
        return
    deserializer = map_of_deserializers[type_id]
    return deserializer(raw_payload, logger)


class SerialReader:
    def __init__(self):
        self.log_file = open("log_file_fast.txt", "w", buffering=1)
        self.ser = serial.Serial(
            port='COM6',
            baudrate=115200
        )

        self.current_position = 0
        self.current_time = 0
        self.previous_signals = None
        self.current_error = 0

    def __del__(self):
        self.log_file.close()

    def setup(self):
        import time
        self.ser.write(b"FO_LOW_CUR_ON\n")
        time.sleep(1)
        self.ser.write(b"RA_TRACK_ON\n")

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

            # sys.stdout.write(f"\rmessage = {message}     ")
            # sys.stdout.flush()


reader = SerialReader()
reader.setup()
reader.loop()

