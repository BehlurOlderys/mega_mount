from .SimpleFocuserDriver import SimpleFocuserDriver
from .MyDeviceDriver import MyDeviceDriver
from Drivers.COMPortReader import *
import time
from struct import unpack
import logging
log = logging.getLogger(__name__)

STEPPER_TYPE_ID = 2
RETRIES_FOR_STATUS_POLL = 5
POLLING_MIN_PERIOD_IN_SECONDS = 1


def deserialize_stepper(raw_payload):
    try:
        (position, desired, delay, direction, is_enabled, is_slewing, raw_name) = unpack("iiH???4s", raw_payload)
    except Exception as e:
        log.error(e)
        return 0, 0, 0, 0
    name = raw_name.decode('UTF-8').strip()
    # logger.write(f"{raw_name},{delay},{direction},{position},{desired},{is_enabled},{is_slewing},\n")
    log.debug(f"Name = {name}, is_slewing = {is_slewing}, direction_forward = {direction}")
    #####################################
    return position, desired, is_slewing, direction


class MegaFocuserDriver(SimpleFocuserDriver):
    def __init__(self, config):
        super().__init__(config)
        self.__last_poll = 0
        self.__config = config
        self.__is_slewing = False

    def __del__(self):
        log.info("Finalizing focuser!")

    def halt(self):
        log.debug("Sending command halt...")
        command = "HALT\n"
        SerialReader.write(command)

    def move(self, position):
        log.debug("Sending command move...")
        command = "FO_MOVE_REL "+str(position) + "\n"
        SerialReader.write(command)

    @property
    def connected(self):
        return MyDeviceDriver.connected.fget(self)

    @connected.setter
    def connected(self, value):
        if value == self.is_connected:
            return

        if value:
            log.debug("Sending command to go back to normal mode...")
            SerialReader.write("FO_LOW_CUR_OFF\n")
        else:
            log.debug("Sending command to go into low current halt mode...")
            SerialReader.write("FO_LOW_CUR_ON\n")

        MyDeviceDriver.connected.fset(self, value)

    @staticmethod
    def get_focuser_messages_length():
        return len(serial_mega_info[STEPPER_TYPE_ID]["FOCU"])

    @staticmethod
    def get_last_focuser_message():
        return serial_mega_info[STEPPER_TYPE_ID]["FOCU"][-1]

    @property
    def ismoving(self):
        time_now = time.time()
        interval = time_now - self.__last_poll
        log.debug(f"Last poll of focuser status: {self.__last_poll}, interval passed = {interval}")
        if interval < POLLING_MIN_PERIOD_IN_SECONDS:
            return self.__is_slewing

        self.__last_poll = time_now
        log.debug("Sending command position...")
        current_size = self.get_focuser_messages_length()
        SerialReader.write("FO_POSITION\n")
        log.debug("Acquiring response about position....")
        max_wait_ms = 1000
        current_wait_ms = 0
        while (current_wait_ms < max_wait_ms) and (current_size >= self.get_focuser_messages_length()):
            time.sleep(0.001)
            current_wait_ms += 1

        new_message = self.get_last_focuser_message()
        log.debug(f"Current = {new_message}")
        self.__position = new_message["position"]
        self.__is_slewing = new_message["is_slewing"]
        return self.__is_slewing
        #
        # for i in range(0, RETRIES_FOR_STATUS_POLL):
        #     message = self.__arduino.readline()
        #     log.debug(f"Message {i} = {message}")
        #     try:
        #         prefix = message.decode('UTF-8').rstrip()
        #         if "BHS" == prefix:
        #             break
        #     except Exception as e:
        #         log.error(f"Exception = {e}")
        #         self.__is_slewing
        #
        # new_message = self.__arduino.readline()
        # log.debug(f"New message = {new_message}")
        # type_id = int(new_message)
        #
        # if type_id != STEPPER_TYPE_ID:
        #     log.warning(f"Type mismatch: {type_id}, expected {STEPPER_TYPE_ID}")
        #     return self.__is_slewing
        #
        # data_size = int(self.__arduino.readline())
        # log.debug(f"Data size = {data_size}")
        #
        # raw_payload = self.__arduino.read(data_size)
        # log.debug(f"raw payload = {raw_payload}")
        # (current, desired, is_slewing, direction) = deserialize_stepper(raw_payload)
        # self.__position = current
        # log.debug(f"Current = {current}, desired = {desired}, is slewing? {is_slewing}, forward? {direction}")
        # self.__is_slewing = is_slewing
        # return is_slewing

    @property
    def position(self):
        self.ismoving()
        return self.__position
