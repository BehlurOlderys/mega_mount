import serial
import sys
from struct import unpack

UNSPECIFIED_TYPE_ID = 0
ENCODER_TYPE_ID = 1
STEPPER_TYPE_ID = 2
ABS_ENCODER_TYPE_ID = 3

handled_ids = [ENCODER_TYPE_ID, STEPPER_TYPE_ID, ABS_ENCODER_TYPE_ID]

serial_mega_info = {
    ENCODER_TYPE_ID : {},
    STEPPER_TYPE_ID : {},
    ABS_ENCODER_TYPE_ID : {},
    UNSPECIFIED_TYPE_ID: []
}

def deserialize_encoder(raw_payload, logger):
    (position, timestamp, raw_name) = unpack("iI4s", raw_payload)
    name = raw_name.decode('UTF-8').strip()
    ### logger part to be refactored! ###
    logger.write(f"{timestamp},{position},{raw_name},\n")
    print(f"Name = {name}, position = {position}, timestamp = {timestamp}")
    #####################################
    if name not in serial_mega_info[ENCODER_TYPE_ID]:
        serial_mega_info[ENCODER_TYPE_ID][name] = []
    serial_mega_info[ENCODER_TYPE_ID][name].append({"position": position, "timestamp": timestamp})
    return position, timestamp, name

def deserialize_abs_encoder(raw_payload, logger):
    (position, raw_name) = unpack("H4s", raw_payload)
    name = raw_name.decode('UTF-8').strip()
    ### logger part to be refactored! ###
    logger.write(f"{position},{raw_name},\n")
    if name not in serial_mega_info[ABS_ENCODER_TYPE_ID]:
        serial_mega_info[ABS_ENCODER_TYPE_ID][name] = []
    serial_mega_info[ABS_ENCODER_TYPE_ID][name].append({"position": position})
    print(f"Name = {name}, position = {position/4}")
    #####################################
    return position, name

def deserialize_stepper(raw_payload, logger):
    (delay, direction, position, desired, is_enabled, is_slewing, raw_name) = unpack("iiH???4s", raw_payload)
    name = raw_name.decode('UTF-8').strip()

    if name not in serial_mega_info[STEPPER_TYPE_ID]:
        serial_mega_info[STEPPER_TYPE_ID][name] = []
    serial_mega_info[STEPPER_TYPE_ID][name].append({"position": position, "direction": direction})
    return name

map_of_deserializers = {
  ENCODER_TYPE_ID: deserialize_encoder,
  STEPPER_TYPE_ID: deserialize_stepper,
  ABS_ENCODER_TYPE_ID: deserialize_abs_encoder
}


def unpack_type(type_id, raw_payload, logger):
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

    def loop(self):
        while True:
            try:
                message = self.ser.readline().decode('UTF-8').rstrip()
                if "BHS" == message:
                    next_line = self.ser.readline()
                    try:
                        type_id = int(next_line)
                    except ValueError as ve:
                        serial_mega_info[UNSPECIFIED_TYPE_ID].append(next_line)
                        continue

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

