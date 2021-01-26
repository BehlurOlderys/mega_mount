from .MyDeviceDriver import MyDeviceDriver


class SimpleFilterWheelDriver(MyDeviceDriver):
    def __init__(self, config):
        super().__init__("SimpleFilterWheelDriver", "typical filter wheel")
        self.__config = config
        self.__position = 0
        self.__names = config['names']

    @property
    def names(self):
        return self.__names

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
