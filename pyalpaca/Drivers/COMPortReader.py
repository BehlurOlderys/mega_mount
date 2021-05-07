import serial
import sys
from struct import unpack

UNSPECIFIED_TYPE_ID = 0
ENCODER_TYPE_ID = 1
STEPPER_TYPE_ID = 2
ABS_ENCODER_TYPE_ID = 3

something_to_write = None
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
    #####################################
    return position, name


def deserialize_stepper(raw_payload, logger):
    (delay, direction, position, desired, is_enabled, is_slewing, raw_name) = unpack("iiH???4s", raw_payload)
    name = raw_name.decode('UTF-8').strip()

    info_dict = {
        "position": position,
        "direction": direction,
        "delay": delay,
        "desired": desired,
        "is_enabled": is_enabled,
        "is_slewing": is_slewing,
        "name": name
    }

    if name not in serial_mega_info[STEPPER_TYPE_ID]:
        serial_mega_info[STEPPER_TYPE_ID][name] = []
    serial_mega_info[STEPPER_TYPE_ID][name].append(info_dict)
    return info_dict


map_of_deserializers = {
  ENCODER_TYPE_ID: deserialize_encoder,
  STEPPER_TYPE_ID: deserialize_stepper,
  ABS_ENCODER_TYPE_ID: deserialize_abs_encoder
}


def unpack_type(type_id, raw_payload, logger):
    deserializer = map_of_deserializers[type_id]
    return deserializer(raw_payload, logger)


class SerialReader:
    def __init__(self, com_port):
        self.log_file = open("log_entire_serial.txt", "w", buffering=1)
        self.ser = serial.Serial(
            port=com_port,
            baudrate=115200
        )

        self.current_position = 0
        self.current_time = 0
        self.previous_signals = None
        self.current_error = 0

    @staticmethod
    def write(something):
        global something_to_write
        something_to_write = something

    def __del__(self):
        self.log_file.close()

    def loop(self):
        global something_to_write
        while True:
            try:
                if something_to_write:
                    self.ser.write(something_to_write.encode())
                    print(f"Written {something_to_write} to serial")
                    something_to_write = None

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


if __name__ == "__main__":
    reader = SerialReader('COM6')
    reader.loop()
