import pyrestful.rest
from pyrestful import mediatypes
from pyrestful.rest import get, put
from tornado.httputil import parse_body_arguments


class BaseDriver(object):
    def __init__(self, name):
        self._name = name
        self._transaction_id = 0
        self._is_connected = False
        self._interface_version = 0


class FilterWheelDriver(BaseDriver):
    def __init__(self, names):
        BaseDriver("SimpleFilterWheelDriver")
        self._names = names
        self._position = 0


drivers = {}


class BaseHandler(pyrestful.rest.RestHandler):
    def _get_simple_response(self):
        client_transaction_id = self.request.arguments["ClientTransactionID"][0].decode()
        response = {
            "ClientTransactionID": client_transaction_id,
            "ServerTransactionID": self._transaction_id,
            "ErrorNumber": 0,
            "ErrorMessage": "",
        }
        self._transaction_id += 1
        return response

    def _response_for_put(self):
        try:
            response = self._get_simple_response()
        except Exception as exc:
            response = {
                "Value": exc
            }
            self.set_status(500, str(exc))
        self.write(response)
        self.finish()

    def _response_with_one_value(self, value):
        try:
            response = self._get_simple_response()
            response["Value"] = value
        except Exception as exc:
            response = {
                "Value": exc
            }
            self.set_status(500, str(exc))
        self.write(response)
        self.finish()

    def _obtain_put_arguments(self):
        values = {}
        files = {}
        parse_body_arguments('application/x-www-form-urlencoded', self.request.body, values, files)
        return values

    @get(_path="/api/v1/{device_type}/{device_number}/interfaceversion", _types=[str, str, str],
         _produces=mediatypes.APPLICATION_JSON)
    def interface_version(self, device_type, device_number):
        self._response_with_one_value(self._interface_version)

    @get(_path="/api/v1/{device_type}/{device_number}/name", _types=[str, str, str],
         _produces=mediatypes.APPLICATION_JSON)
    def interface_version(self, device_type, device_number):
        self._response_with_one_value(self._name)

    @get(_path="/api/v1/{device_type}/{device_number}/connected", _types=[str, int, str], _produces=mediatypes.APPLICATION_JSON)
    def get_connected(self, device_type, device_number):
        self._response_with_one_value(self._is_connected)

    @put(_path="/api/v1/{device_type}/{device_number}/connected", _types=[str, int, str], _produces=mediatypes.APPLICATION_JSON)
    def set_connected(self, device_type, device_number):
        values = self._obtain_put_arguments()
        self._is_connected = (values["Position"][0].decode() == "True")
        response = self._get_simple_response()
        self.write(response)
        self.finish()
        print("PUT CONNECTED")


class FilterWheelService(BaseService):
    def initialize(self, names):
        super().initialize("SimpleFilterWheel")
        self._position = 0
        self._names = names

    @get(_path="/api/v1/{device_type}/{device_number}/position", _types=[str, str, str],
         _produces=mediatypes.APPLICATION_JSON)
    def get_position(self, device_type, device_number):
        self._response_with_one_value(self._position)

    @get(_path="/api/v1/{device_type}/{device_number}/names", _types=[str, str, str],
         _produces=mediatypes.APPLICATION_JSON)
    def get_names(self, device_type, device_number):
        self._response_with_one_value(self._names)

    @put(_path="/api/v1/{device_type}/{device_number}/position", _types=[str, str, str],
         _produces=mediatypes.APPLICATION_JSON)
    def put_position(self, device_type, device_number):
        if self.request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
            values = self._obtain_put_arguments()
            self._position = int(values["Position"][0].decode())

        response = self._get_simple_response()
        self.write(response)
        self.finish()
        print("PUT POSITION " + str(self._position))


class SimpleEQMountService(BaseService):
    def initialize(self):
        super().initialize("SimpleEQMount")

    @get(_path="/api/v1/{device_type}/{device_number}/{whatever}", _types=[str, str, str],
         _produces=mediatypes.APPLICATION_JSON)
    def whatever(self, device_type, device_number, whatever):
        print(whatever)
        print(self.request)