from .SimpleEQMountDriver import SimpleEQMountDriver
from Drivers.ComPortDistributor import ComPortDistributor
import time
import threading
from struct import unpack


MOVE_THRESHOLD = 0.0001
RA_AXIS_NUMBER = 1
DEC_AXIS_NUMBER = 0
global_thread_killer = False
global_keep_logging = True


def encoder_logging(ser):
    print("Starting encoder logging!")
    log_file = open("encoder_log.txt", "w")
    while not global_thread_killer:
        if not global_keep_logging:
            continue
        try:
            message = ser.readline().decode('UTF-8').rstrip()
            if "BHS" == message:
                type_id = int(ser.readline())
                data_size = int(ser.readline())
                raw_payload = ser.read(data_size)
                (position, timestamp, raw_name) = unpack("iI4s", raw_payload)
                name = raw_name.decode('UTF-8').strip()
                log_file.write(f"{raw_name},{timestamp},{position},\n")

        except Exception as e:
            print("Exception: " + str(e))
            continue

    log_file.close()


class MegaMountDriver(SimpleEQMountDriver):
    def __init__(self, config):
        super().__init__(config)
        self.__last_poll = 0
        self.__config = config
        self.__is_slewing = False
        self.__tracking = False
        self.__arduino = ComPortDistributor.get_port(self.__config["com_port"])
        time.sleep(1)
        self.encoder_log_thread = threading.Thread(target=encoder_logging, args=(self.__arduino,))
        self.encoder_log_thread.start()
        print("Mega mount initialized")

    def __del__(self):
        global global_thread_killer
        global_thread_killer = True
        ComPortDistributor.drop_port(self.__config["com_port"])
        self.encoder_log_thread.join()
        print("Finalizing mega mount!")

    def __read_line_from_arduino(self):
        global global_keep_logging
        global_keep_logging = False
        message = self.__arduino.readline()
        global_keep_logging = True
        return message

    def axis_rates(self, axis):
        rates = [
                    [
                        {"Maximum": 0.0833, "Minimum": 0.0417}
                    ],
                    [
                        {"Maximum": 0.0833, "Minimum": 0.0417},
                    ]
                ]
        return rates[axis]

    @property
    def tracking(self):
        return self.__tracking

    @tracking.setter
    def tracking(self, value):
        print(f"Setting tracking to {value}")
        if value is True:
            command = "RA_TRACK_ON\n"
        else:
            command = "RA_TRACK_OFF\n"

        self.__arduino.write(command.encode())
        print("Getting ack:")
        command = "IS_TRACKING\n"
        self.__arduino.write(command.encode())
        print("Acquiring response...")
        message = self.__read_line_from_arduino()
        print(f"Response = {message}")
        self.__tracking = value

    def moveaxis(self, axis_str, rate_str):
        axis = int(axis_str)
        rate = float(rate_str)
        print(f"Move axis with axis={axis} and rate={rate}")
        if axis == RA_AXIS_NUMBER:  # DEC
            if abs(rate) < MOVE_THRESHOLD:
                command = "RA_STOP\n"
            else:
                direction = 1 if rate > 0 else 0
                command = "RA_MOVE " +str(direction) +"\n"

            print(f"Sending command:{command}!")
            self.__arduino.write(command.encode())
        elif axis == DEC_AXIS_NUMBER:  # DEC
            if abs(rate) < MOVE_THRESHOLD:
                command = "DE_STOP\n"
            else:
                direction = 1 if rate > 0 else 0
                command = "DE_MOVE " +str(direction) +"\n"

            print(f"Sending command:{command}!")
            self.__arduino.write(command.encode())
        else:
            print(f"Unknown axis: {axis}!")