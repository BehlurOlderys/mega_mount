import tornado
import pyrestful
import services

from services.dome_service import DomeService
from services.SimpleTelescopeService import SimpleTelescopeService
from services.SimpleFocuserService import SimpleFocuserService
from services.SimpleFilterWheelService import SimpleFilterWheelService
from services.config import ascomConfig, initConfig

Services = []


def instantiate_driver(config):

    if not('driver_instance' in config):
        config['driver_instance'] = None
    
    driver = config['driver_instance']
    if driver is None:
        if config['device_type'] == 'dome':
            # TODO  dynamically instantiate the drivers
        
            if config['device_driver'] == 'MyASCOMDomeDriver':
                from Drivers.ASCOMDriver.MyDomeDriver import MyDomeDriver
                driver = MyDomeDriver()  # TODO pass driver_config as well ?
                config['driver_instance'] = driver
        elif config['device_type'] == 'filterwheel':
            if config['device_driver'] == 'SimpleFilterWheelDriver':
                from Drivers.ASCOMDriver.SimpleFilterWheelDriver import SimpleFilterWheelDriver
                print("Choosing driver for SimpleFilterWheelDriver")
                driver = SimpleFilterWheelDriver(config["driver_config"])
                config['driver_instance'] = driver

        elif config['device_type'] == 'telescope':
            if config['device_driver'] == 'DummyMountDriver':
                from Drivers.ASCOMDriver.SimpleEQMountDriver import SimpleEQMountDriver
                print("Choosing driver for SimpleEQMountDriver")
                driver = SimpleEQMountDriver(config["driver_config"])
                config['driver_instance'] = driver
            if config['device_driver'] == 'MegaMountDriver':
                from Drivers.ASCOMDriver.MegaMountDriver import MegaMountDriver
                print("Choosing driver for MegaMountDriver")
                driver = MegaMountDriver(config["driver_config"])
                config['driver_instance'] = driver
        elif config['device_type'] == 'focuser':
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


if __name__ == '__main__':
    try:
        initConfig()
        handlers = get_rest_handlers()
        print("Start the service")
        app = pyrestful.rest.RestService(handlers)
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(11111)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nStop the service")
