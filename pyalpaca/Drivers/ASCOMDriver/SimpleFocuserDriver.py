from .MyDeviceDriver import MyDeviceDriver


class SimpleFocuserDriver(MyDeviceDriver):
    def __init__(self, config):
        super().__init__("SimpleFocuserDriver", "minimal focuser")
        self.__config = config
        self.__is_moving = False
        self.__position = 0
        self.__maxincrement = 10
        self.__max_step = 10
        self.__step_size = 10.1
        self.__temperature = 36.6

    @property
    def absolute(self):
        return False

    @property
    def ismoving(self):
        return self.__is_moving

    @property
    def maxincrement(self):
        return self.__maxincrement

    @property
    def maxstep(self):
        return self.__max_step

    @property
    def position(self):
        return self.__position

    @property
    def stepsize(self):
        return self.__step_size

    @property
    def tempcomp(self):
        pass

    @property
    def tempcompavailable(self):
        return False

    @property
    def temperature(self):
        return self.__temperature

    @tempcomp.setter
    def tempcomp(self, value):
        pass

    def halt(self):
        pass

    def move(self, position):
        pass
