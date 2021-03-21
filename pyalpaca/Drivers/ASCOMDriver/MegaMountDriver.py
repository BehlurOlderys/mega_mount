from .SimpleEQMountDriver import SimpleEQMountDriver
from Drivers.ComPortDistributor import ComPortDistributor
import time
from struct import unpack


MOVE_THRESHOLD = 0.0001

class MegaMountDriver(SimpleEQMountDriver):
    def __init__(self, config):
        super().__init__(config)
        self.__last_poll = 0
        self.__config = config
        self.__is_slewing = False
        self.__tracking = False
        self.__arduino = ComPortDistributor.get_port(self.__config["com_port"])
        time.sleep(1)
        print("Mega mount initialized")

    def __del__(self):
        ComPortDistributor.drop_port(self.__config["com_port"])
        print("Finalizing mega mount!")

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
        message = self.__arduino.readline()
        print(f"Response = {message}")
        self.__tracking = value

    def moveaxis(self, axis, rate):
        if axis == 0:  # RA
            if abs(rate) < MOVE_THRESHOLD:
                command = "RA_STOP\n"
            else:
                direction = 1 if rate > 0 else 0
                command = "RA_MOVE " +str(direction) +"\n"

            self.__arduino.write(command.encode())
        if axis == 1:  # DEC
            if abs(rate) < MOVE_THRESHOLD:
                command = "DE_STOP\n"
            else:
                direction = 1 if rate > 0 else 0
                command = "DE_MOVE " +str(direction) +"\n"

            self.__arduino.write(command.encode())
        else:
            print(f"Unknown axis: {axis}!")