from .SimpleFocuserDriver import SimpleFocuserDriver
import serial
import time


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
        command = "MOVE "+str(position) + "\n"
        self.arduino.write(command.encode())

    @property
    def ismoving(self):
        print("Sending command position...")
        self.arduino.write(b"POSITION\n")
        print("Acquiring response about position....")
        position_output = self.arduino.readline().decode('UTF-8').rstrip()
        print(position_output)
        _, current, _, desired = position_output.split(" ")
        print("Obtained: Current = " + current + ", desired = " + desired)
        self.__is_moving = not (int(current) == int(desired))
        return self.__is_moving

    @property
    def position(self):

        return self.__position
