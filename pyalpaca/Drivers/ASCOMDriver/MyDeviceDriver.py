import logging

from .DeviceInterfaces.IAscomDriver import IAscomDriver


class MyDeviceDriver(IAscomDriver):

    FORMAT = '%(asctime)-15s %(identifier)s %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('MyASCOMDriver')

    def __init__(self, name, description):
        self.__connected_state = False
        self.__name = name
        self.__description = description
        self.__interface_version = 1
        self.__driver_info = "TODO driver info"
        self.__driver_version = "1.0"
        self.__supported_actions = ["todo_action_1","todo_action_2","todo_action_3"]

    #
    # IAscomDriver
    #

    @property
    def interface_version(self):
        return self.__interface_version

    @property
    def driver_info(self):
        return self.__driver_info

    @property
    def driver_version(self):
        return self.__driver_version

    @property
    def is_connected(self):
        #  TODO check that the driver hardware connection exists and is connected to the hardware
        return self.__connected_state

    def check_connected(self, message):
        # Use this function to throw an exception if we aren't connected to the hardware
        if not self.is_connected:
            raise ValueError("Not Connected : %s" % message)
        pass

    @property
    def connected(self):
        return self.is_connected

    @connected.setter
    def connected(self, value):
        if value == self.is_connected:
            return

        self.__connected_state = value
        info_string = "Connecting to " if value else "Disconnecting from "
        info_string += ("device %s" % self.__name)
        MyDeviceDriver.logger.info(info_string)
        # TODO connect to the device
        # TODO disconnect from the device

    @property
    def description(self):
        # TODO customize this device description
        return self.__description

    @property
    def name(self):
        self.__name = "Short driver name - please customise"
        return self.__name

    #
    # IDeviceControl
    #

    def action(self, action_name, action_parameters):
        raise NotImplementedError(
            "Action %s is not implemented by this driver" % action_name)

    @property
    def supported_actions(self):
        return self.__supported_actions

    def command_blind(self, command, raw=False):
        self.check_connected("command_blind")
        # Call CommandString and return as soon as it finishes
        self.command_string(command, raw)
        # or
        raise NotImplementedError("command_blind")
        # DO NOT have both these sections!  One or the other

    def command_bool(self, command, raw=False):
        self.check_connected("command_bool")
        ret = self.command_string(command, raw)
        # TODO decode the return string and return true or false
        # or
        raise NotImplementedError("command_bool")
        # DO NOT have both these sections!  One or the other

    def command_string(self, command, raw=False):
        self.check_connected("command_string")
        # it's a good idea to put all the low level communication with the device here,
        # then all communication calls this function
        # you need something to ensure that only one command is in progress at a time

        raise NotImplementedError("command_string")

        return "the expected return value"


if __name__ == "__main__":
    d = MyDeviceDriver("Test name", "Test description")
    print(d.connected)
    d.connected = True
    print(d.connected)
    pass
