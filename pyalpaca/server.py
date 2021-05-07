import tornado
import pyrestful
import services
import threading

from Drivers.COMPortReader import SerialReader
from services.dome_service import DomeService
from services.SimpleTelescopeService import SimpleTelescopeService
from services.SimpleFocuserService import SimpleFocuserService
from services.SimpleFilterWheelService import SimpleFilterWheelService
from services.config import ascomConfig, initConfig
import logging

Services = []


def instantiate_driver(config):

    if not('driver_instance' in config):
        config['driver_instance'] = None
    
    driver = config['driver_instance']
    if driver is None:
        #
        # elif config['device_type'] == 'telescope':
        #     if config['device_driver'] == 'DummyMountDriver':
        #         from Drivers.ASCOMDriver.SimpleEQMountDriver import SimpleEQMountDriver
        #         print("Choosing driver for SimpleEQMountDriver")
        #         driver = SimpleEQMountDriver(config["driver_config"])
        #         config['driver_instance'] = driver
        #     if config['device_driver'] == 'MegaMountDriver':
        #         from Drivers.ASCOMDriver.MegaMountDriver import MegaMountDriver
        #         print("Choosing driver for MegaMountDriver")
        #         driver = MegaMountDriver(config["driver_config"])
        #         config['driver_instance'] = driver
        if config['device_type'] == 'focuser':
            if config['device_driver'] == 'MegaFocuserDriver':
                from Drivers.ASCOMDriver.MegaFocuserDriver import MegaFocuserDriver
                print("Choosing driver for MegaFocuserDriver")
                driver = MegaFocuserDriver(config["driver_config"])
                config['driver_instance'] = driver

    return driver


config_services_map ={
    "dome": DomeService,
    "filterwheel": SimpleFilterWheelService,
    "telescope": SimpleTelescopeService,
    "focuser": SimpleFocuserService
}


def instantiate_rest_handler(config):
    return config_services_map[config['device_type']]


def get_rest_handlers():
    # instantiate all necessary services defined in the config file
    handlers = []
    for config in services.config.ascomConfig['drivers']:
        instantiate_driver(config)
        handler = instantiate_rest_handler(config)
        if not(handler is None):
            handlers.append(handler)

    return handlers


def init_logging():
    logFormatter = logging.Formatter("%(asctime)s [%(filename)s] [%(lineno)d] [%(funcName)s] [%(levelname)-.4s]  %(message)s")
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler("main_server.log")
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    rootLogger.setLevel(logging.INFO)


class Server:
    def __init__(self):
        init_logging()
        self.serial_handler_thread = None
        try:
            initConfig()
            com_port = services.config.ascomConfig["common_port"]
            print(f"COM port = {com_port}")
            serial_reader = SerialReader(com_port)
            self.serial_handler_thread = threading.Thread(target=serial_reader.loop)
            self.serial_handler_thread.start()
            handlers = get_rest_handlers()
            print("Start the service")
            app = pyrestful.rest.RestService(handlers)
            http_server = tornado.httpserver.HTTPServer(app)
            http_server.listen(11111)
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            print("\nStop the service")

    def __del__(self):
        self.serial_handler_thread.join()


if __name__ == '__main__':
    server = Server()

