from pyrestful import mediatypes
from pyrestful.rest import get, post, put, delete
from .device_service import DeviceService
from .config import getDriverInstance


class SimpleFocuserService(DeviceService):
    @get(_path="/api/v1/{device_type}/{device_number}/absolute", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def get_absolute(self, device_type, device_number):
        super().get_resource(device_type, device_number, "absolute")

    @get(_path="/api/v1/{device_type}/{device_number}/ismoving", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def get_ismoving(self, device_type, device_number):
        super().get_resource(device_type, device_number, "ismoving")

    @get(_path="/api/v1/{device_type}/{device_number}/maxincrement", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def get_maxincrement(self, device_type, device_number):
        super().get_resource(device_type, device_number, "maxincrement")

    @get(_path="/api/v1/{device_type}/{device_number}/maxstep", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def get_maxstep(self, device_type, device_number):
        super().get_resource(device_type, device_number, "maxstep")

    @get(_path="/api/v1/{device_type}/{device_number}/position", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def get_position(self, device_type, device_number):
        super().get_resource(device_type, device_number, "position")

    @get(_path="/api/v1/{device_type}/{device_number}/stepsize", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def get_stepsize(self, device_type, device_number):
        super().get_resource(device_type, device_number, "stepsize")

    @get(_path="/api/v1/{device_type}/{device_number}/tempcomp", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def get_tempcomp(self, device_type, device_number):
        super().get_resource(device_type, device_number, "tempcomp")

    @get(_path="/api/v1/{device_type}/{device_number}/tempcompavailable", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def get_tempcompavailable(self, device_type, device_number):
        super().get_resource(device_type, device_number, "tempcompavailable")

    @get(_path="/api/v1/{device_type}/{device_number}/temperature", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def get_temperature(self, device_type, device_number):
        super().get_resource(device_type, device_number, "temperature")

    @put(_path="/api/v1/{device_type}/{device_number}/tempcomp", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def set_tempcomp(self, device_type, device_number):
        super().set_one_boolean_resource(device_type, device_number, "TempComp", "tempcomp")

    @put(_path="/api/v1/{device_type}/{device_number}/halt", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def halt(self, device_type, device_number):
        super().standard_response_for_put(device_type, device_number, lambda driver: driver.halt())

    @put(_path="/api/v1/{device_type}/{device_number}/move", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def move(self, device_type, device_number):
        super().set_one_integer_resource(device_type, device_number, "Position", "move")
