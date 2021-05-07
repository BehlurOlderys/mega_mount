import serial
import sys
from struct import unpack
import logging
log = logging.getLogger(__name__)

UNSPECIFIED_TYPE_ID = 255
ENCODER_TYPE_ID = 1
STEPPER_TYPE_ID = 2
ABS_ENCODER_TYPE_ID = 3

something_to_write = None
handled_ids = [ENCODER_TYPE_ID, STEPPER_TYPE_ID, ABS_ENCODER_TYPE_ID]

serial_mega_info = {
    ENCODER_TYPE_ID: {},
    STEPPER_TYPE_ID: {},
    ABS_ENCODER_TYPE_ID: {},
    UNSPECIFIED_TYPE_ID: []
}

global_thread_killer = False


def get_focuser_messages_length():
    if "FOCU" not in serial_mega_info[STEPPER_TYPE_ID]:
        return 0
    return len(serial_mega_info[STEPPER_TYPE_ID]["FOCU"])


def get_last_focuser_message():
    if "FOCU" not in serial_mega_info[STEPPER_TYPE_ID]:
        return None
    return serial_mega_info[STEPPER_TYPE_ID]["FOCU"][-1]


def get_ra_stepper_messages_length():
    if "STRA" not in serial_mega_info[STEPPER_TYPE_ID]:
        return 0
    return len(serial_mega_info[STEPPER_TYPE_ID]["STRA"])


def get_last_ra_stepper_message():
    if "STRA" not in serial_mega_info[STEPPER_TYPE_ID]:
        return None
    return serial_mega_info[STEPPER_TYPE_ID]["STRA"][-1]


def get_unspecified_messages_length():
    return len(serial_mega_info[UNSPECIFIED_TYPE_ID])


def get_last_unspecified_message():
    return serial_mega_info[UNSPECIFIED_TYPE_ID][-1]



def deserialize_encoder(raw_payload, timestamp, logger):
    (position, timestamp, raw_name) = unpack("iI4s", raw_payload)
    name = raw_name.decode('UTF-8').strip()
    ### logger part to be refactored! ###
    logger.write(f"{timestamp},{position},{raw_name},\n")
    #####################################
    if name not in serial_mega_info[ENCODER_TYPE_ID]:
        serial_mega_info[ENCODER_TYPE_ID][name] = []
    serial_mega_info[ENCODER_TYPE_ID][name].append({"position": position, "timestamp": timestamp})
    return position, timestamp, name


def deserialize_abs_encoder(raw_payload, timestamp, logger):
    (position, raw_name) = unpack("H4s", raw_payload)
    name = raw_name.decode('UTF-8').strip()

    info_dict = {
        "timestamp": timestamp,
        "name": name,
        "position": position,
    }

    logger.write(f"{timestamp} ABS_ENCODER: {info_dict}\n")
    if name not in serial_mega_info[ABS_ENCODER_TYPE_ID]:
        serial_mega_info[ABS_ENCODER_TYPE_ID][name] = []
    serial_mega_info[ABS_ENCODER_TYPE_ID][name].append(info_dict)
    return info_dict


def deserialize_stepper(raw_payload, timestamp, logger):
    (delay, direction, position, desired, is_enabled, is_slewing, raw_name) = unpack("iiH???4s", raw_payload)
    name = raw_name.decode('UTF-8').strip()

    info_dict = {
        "timestamp": timestamp,
        "position": position,
        "direction": direction,
        "delay": delay,
        "desired": desired,
        "is_enabled": is_enabled,
        "is_slewing": is_slewing,
        "name": name
    }

    logger.write(f"{timestamp} STEPPER: {info_dict}\n")
    if name not in serial_mega_info[STEPPER_TYPE_ID]:
        serial_mega_info[STEPPER_TYPE_ID][name] = []
    serial_mega_info[STEPPER_TYPE_ID][name].append(info_dict)
    return info_dict


map_of_deserializers = {
  ENCODER_TYPE_ID: deserialize_encoder,
  STEPPER_TYPE_ID: deserialize_stepper,
  ABS_ENCODER_TYPE_ID: deserialize_abs_encoder
}


def unpack_type(type_id, timestamp, raw_payload, logger):
    deserializer = map_of_deserializers[type_id]
    return deserializer(raw_payload, timestamp, logger)


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
    def kill():
        global global_thread_killer
        global_thread_killer = True

    @staticmethod
    def write(something):
        global something_to_write
        something_to_write = something

    def __del__(self):
        self.log_file.close()

    def loop(self):
        global something_to_write
        while not global_thread_killer:
            try:
                if something_to_write:
                    self.ser.write(something_to_write.encode())
                    log.info(f"Written {something_to_write} to serial")
                    something_to_write = None

                message = self.ser.readline().decode('UTF-8').rstrip()
                if "BHS" == message:
                    timestamp_line = self.ser.readline()
                    try:
                        timestamp = int(timestamp_line.decode('UTF-8').rstrip())
                    except ValueError as ve:
                        log.error(f"Value error {ve} happened when reading timestamp from {timestamp_line}")
                        continue

                    next_line = self.ser.readline()

                    try:
                        type_id = int(next_line)
                    except ValueError as ve:
                        log.error(f"Error reading type id line: {next_line}: {ve}")
                        continue

                    data_size_line = self.ser.readline()
                    if type_id == UNSPECIFIED_TYPE_ID:
                        serial_mega_info[UNSPECIFIED_TYPE_ID].append(data_size_line)
                        continue

                    try:
                        data_size = int(data_size_line)
                    except ValueError as ve:
                        log.error(f"Value error {ve} happened when reading data size line {data_size_line}")
                        continue

                    raw_payload = self.ser.read(data_size)
                    unpack_type(type_id, timestamp, raw_payload, self.log_file)

            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                log.error("SerialReader::loop Exception: " + message)
                continue


if __name__ == "__main__":
    reader = SerialReader('COM6')
    reader.loop()
