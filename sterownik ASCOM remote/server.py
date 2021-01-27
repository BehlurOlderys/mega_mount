import tornado
import pyrestful
import services
import sys

from services.mount_service import FilterWheelService

Services = []


if __name__ == '__main__':
    try:
        print("Start the service")
        app = pyrestful.rest.RestService([FilterWheelService(["A", "B", "C"])])
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(11113)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nStop the service")
