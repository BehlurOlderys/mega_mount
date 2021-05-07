from .SimpleEQMountDriver import SimpleEQMountDriver
from Drivers.COMPortReader import SerialReader, get_ra_stepper_messages_length, get_last_ra_stepper_message, get_unspecified_messages_length, get_last_unspecified_message
import logging
log = logging.getLogger(__name__)
import time

MOVE_THRESHOLD = 0.0001
RA_AXIS_NUMBER = 1
DEC_AXIS_NUMBER = 0
global_thread_killer = False
global_keep_logging = False

ENCODER_TYPE_ID = 1


class MegaMountDriver(SimpleEQMountDriver):
    def __init__(self, config):
        super().__init__(config)
        self.__last_poll = 0
        self.__config = config
        self.__is_slewing = False
        self.__tracking = False
        log.debug("Mega mount initialized")

    def __del__(self):
        log.debug("Finalizing mega mount!")

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
        log.debug(f"Setting tracking to {value}")
        if value is True:
            command = "RA_TRACK_ON\n"
        else:
            command = "RA_TRACK_OFF\n"

        SerialReader.write(command)
        # log.debug("Getting ack:")
        # command = "IS_TRACKING\n"
        # current_size = get_unspecified_messages_length()
        # SerialReader.write(command)
        # log.debug("Acquiring response...")
        # max_wait_ms = 1000
        # current_wait_ms = 0
        # while (current_wait_ms < max_wait_ms) and (current_size >= get_unspecified_messages_length()):
        #     time.sleep(0.001)
        #     current_wait_ms += 1
        #
        # new_message = get_last_unspecified_message()
        # log.debug(f"Response = {new_message}")
        self.__tracking = value

    def moveaxis(self, axis_str, rate_str):
        axis = int(axis_str)
        rate = float(rate_str)
        log.debug(f"Move axis with axis={axis} and rate={rate}")
        if axis == RA_AXIS_NUMBER:  # DEC
            if abs(rate) < MOVE_THRESHOLD:
                command = "RA_STOP\n"
            else:
                direction = 1 if rate > 0 else 0
                command = "RA_MOVE " +str(direction) +"\n"

            log.debug(f"Sending command:{command}!")
            SerialReader.write(command)
        elif axis == DEC_AXIS_NUMBER:  # DEC
            if abs(rate) < MOVE_THRESHOLD:
                command = "DE_STOP\n"
            else:
                direction = 1 if rate > 0 else 0
                command = "DE_MOVE " +str(direction) +"\n"

            log.debug(f"Sending command:{command}!")
            SerialReader.write(command)
        else:
            log.warning(f"Unknown axis: {axis}!")