from .SimpleFocuserDriver import SimpleFocuserDriver
import serial
import time
from struct import unpack


STEPPER_TYPE_ID = 2


def deserialize_stepper(raw_payload):
    try:
        print("A")
        (position, desired, delay, direction, is_enabled, is_slewing, raw_name) = unpack("iiH???4s", raw_payload)
        print("B")
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
        self.arduino = serial.Serial(config["com_port"], 115200, timeout=.5)
        time.sleep(1)
        message = self.arduino.readline().decode('UTF-8').rstrip()
        print("Welcome message = " + message)

    def __del__(self):
        print("Finalizing mount!")
        self.arduino.Close()

    def halt(self):
        print("Sending command halt...")
        command = "HALT\n"
        self.arduino.write(command.encode())

    def move(self, position):
        print("Sending command move...")
        command = "FO_MOVE_REL "+str(position) + "\n"
        self.arduino.write(command.encode())

    @property
    def ismoving(self):
        print("Sending command position...")
        self.arduino.write(b"FO_POSITION\n")
        print("Acquiring response about position....")

        for i in range(0, 5):
            message = self.arduino.readline()
            print(f"Message {i} = {message}")
            try:
                prefix = message.decode('UTF-8').rstrip()
                if "BHS" == prefix:
                    break
            except Exception as e:
                print(f"Exception = {e}")

        new_message = self.arduino.readline()
        print(f"New message = {new_message}")
        type_id = int(new_message)

        if type_id != STEPPER_TYPE_ID:
            print(f"Type mismatch: {type_id}, expected {STEPPER_TYPE_ID}")
            return False

        data_size = int(self.arduino.readline())
        print(f"Data size = {data_size}")

        raw_payload = self.arduino.read(data_size)
        print(f"raw payload = {raw_payload}")
        (current, desired, is_slewing, direction) = deserialize_stepper(raw_payload)
        self.__position = current
        print(f"Current = {current}, desired = {desired}, is slewing? {is_slewing}, forward? {direction}")
        return is_slewing

        # if "BHS" != message:
        #     print(f"Expected BHS prefix, but did not find anything like it: {message}")
        #     return False
        #
        # type_id = int(self.ser.readline())
        # if type_id != STEPPER_TYPE_ID:
        #     print(f"Type mismatch: {type_id}, expected {STEPPER_TYPE_ID}")
        #     return False
        #
        # data_size = int(self.ser.readline())
        # raw_payload = self.ser.read(data_size)
        # (current, desired, is_slewing, direction) = deserialize_stepper(raw_payload)
        # self.__position = current
        # print(f"Current = {current}, desired = {desired}, is slewing? {is_slewing}, forward? {direction}")
        # return is_slewing

    @property
    def position(self):
        self.ismoving()
        return self.__position
