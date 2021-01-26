import abc


class IAscomDriver(abc.ABC):
    """ASCOM.Interface ASCOM Driver Common Base Interface"""

    @abc.abstractproperty
    def connected(self):
      # Set True to enable the link. Set False to disable the link.
        pass

    @abc.abstractproperty
    def description(self):
      # Returns a description of the driver
        pass

    @abc.abstractproperty
    def name(self):
      # Returns a description of the driver
        pass
