from .SimpleFocuserDriver import SimpleFocuserDriver
from .MyDeviceDriver import MyDeviceDriver
from Drivers.ComPortDistributor import ComPortDistributor
import time
from struct import unpack


STEPPER_TYPE_ID = 2
RETRIES_FOR_STATUS_POLL = 5
POLLING_MIN_PERIOD_IN_SECONDS = 1


def deserialize_stepper(raw_payload):
    try:
        (position, desired, delay, direction, is_enabled, is_slewing, raw_name) = unpack("iiH???4s", raw_payload)
    except Exception as e:
        print(e)
        return 0, 0, 0, 0
    name = raw_name.decode('UTF-8').strip()
    # logger.write(f"{raw_name},{delay},{direction},{position},{desired},{is_enabled},{is_slewing},\n")
    print(f"Name = {name}, is_slewing = {is_slewing}, direction_forward = {direction}")
    #####################################
    return position, desired, is_slewing, direction


class MegaFocuserDriver(SimpleFocuserDriver):
    def __init__(self, config):
        super().__init__(config)
        self.__last_poll = 0
        self.__config = config
        self.__is_slewing = False
        self.__arduino = ComPortDistributor.get_port(self.__config["com_port"])
        if self.__arduino is not None:
            time.sleep(1)
            message = self.__arduino.readline().decode('UTF-8').rstrip()
            print("Welcome message = " + message)

    def __del__(self):
        ComPortDistributor.drop_port(self.__config["com_port"])
        print("Finalizing focuser!")

    def halt(self):
        if self.__arduino is None:
            return
        print("Sending command halt...")
        command = "HALT\n"
        self.__arduino.write(command.encode())

    def move(self, position):
        if self.__arduino is None:
            return
        print("Sending command move...")
        command = "FO_MOVE_REL "+str(position) + "\n"
        self.__arduino.write(command.encode())

    @property
    def connected(self):
        if self.__arduino is None:
            return False
        return MyDeviceDriver.connected.fget(self)

    @connected.setter
    def connected(self, value):
        if value == self.is_connected:
            return

        if self.__arduino is None:
            self.__arduino = ComPortDistributor.get_port(self.__config["com_port"])
            return

        if value:
            print("Sending command to go back to normal mode...")
            self.__arduino.write(b"FO_LOW_CUR_OFF\n")
        else:
            print("Sending command to go into low current halt mode...")
            self.__arduino.write(b"FO_LOW_CUR_ON\n")

        MyDeviceDriver.connected.fset(self, value)


    @property
    def ismoving(self):
        if self.__arduino is None:
            return False
        time_now = time.time()
        interval = time_now - self.__last_poll
        print(f"Last poll of focuser status: {self.__last_poll}, interval passed = {interval}")
        if interval < POLLING_MIN_PERIOD_IN_SECONDS:
            return self.__is_slewing

        self.__last_poll = time_now
        print("Sending command position...")
        self.__arduino.write(b"FO_POSITION\n")
        print("Acquiring response about position....")

        for i in range(0, RETRIES_FOR_STATUS_POLL):
            message = self.__arduino.readline()
            print(f"Message {i} = {message}")
            try:
                prefix = message.decode('UTF-8').rstrip()
                if "BHS" == prefix:
                    break
            except Exception as e:
                print(f"Exception = {e}")
                self.__is_slewing

        new_message = self.__arduino.readline()
        print(f"New message = {new_message}")
        type_id = int(new_message)

        if type_id != STEPPER_TYPE_ID:
            print(f"Type mismatch: {type_id}, expected {STEPPER_TYPE_ID}")
            return self.__is_slewing

        data_size = int(self.__arduino.readline())
        print(f"Data size = {data_size}")

        raw_payload = self.__arduino.read(data_size)
        print(f"raw payload = {raw_payload}")
        (current, desired, is_slewing, direction) = deserialize_stepper(raw_payload)
        self.__position = current
        print(f"Current = {current}, desired = {desired}, is slewing? {is_slewing}, forward? {direction}")
        self.__is_slewing = is_slewing
        return is_slewing

    @property
    def position(self):
        self.ismoving()
        return self.__position
