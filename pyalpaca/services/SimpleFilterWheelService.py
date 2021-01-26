from pyrestful import mediatypes
from pyrestful.rest import get, post, put, delete
from .device_service import DeviceService


class SimpleFilterWheelService(DeviceService):
    # SHOULD BE IMPLEMENTED HERE ONLY THE RESOURCES WHICH CANNOT BE EASILY QUERIED ONTO
    # THE ASCOM DRIVER USING REFLECTION AT THE DeviceService LEVEL.
    @get(_path="/api/v1/{device_type}/{device_number}/names", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def get_names(self, device_type, device_number):
        print("get names method called")
        super().get_resource(device_type, device_number, "names")

    @get(_path="/api/v1/{device_type}/{device_number}/position", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def get_position(self, device_type, device_number):
        print("get position method called")
        super().get_resource(device_type, device_number, "position")

    @put(_path="/api/v1/{device_type}/{device_number}/position", _types=[str, str], _produces=mediatypes.APPLICATION_JSON)
    def set_position(self, device_type, device_number):
        print("set position method called")
        super().set_one_integer_resource(device_type, device_number, "Position", "position")

