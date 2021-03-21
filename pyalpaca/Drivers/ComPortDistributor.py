import serial

com_ports = {}


class ComPortDistributor:
    @staticmethod
    def get_port(port_name):
        if not port_name in com_ports:
            com_ports[port_name] = {"ref": serial.Serial(port_name, 115200, timeout=.5),
                                    "instances": 0}
        com_ports[port_name]["instances"] += 1
        return com_ports[port_name]["ref"]

    @staticmethod
    def drop_port(port_name):
        if port_name in com_ports:
            com_ports[port_name]["instances"] -= 1
            if com_ports[port_name]["instances"] <= 0:
                com_ports[port_name]["ref"].Close()
                del com_ports[port_name]