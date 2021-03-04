import serial
import sys
from struct import unpack

def unpack_type(type_id, raw_payload):
    if type_id == 1:
        (position, timestamp, raw_name) = unpack("iI5s", raw_payload)
        name = raw_name.decode('UTF-8').strip()
        print("Name = " + name[:-1] + ", position = " + str(position) + ", timestamp = " + str(timestamp))


class EncoderReader:
    def __init__(self):
        self.log_file = open("log_file_fast.txt", "w", buffering=1)
        self.ser = serial.Serial(
            port='COM3',
            baudrate=115200
        )

        self.current_position = 0
        self.current_time = 0
        self.previous_signals = None
        self.current_error = 0

    def __del__(self):
        self.log_file.close()

    def loop(self):
        while True:
            try:
                message = self.ser.readline().decode('UTF-8').rstrip()
                if "BHS" == message:
                    type_id = int(self.ser.readline())
                    data_size = int(self.ser.readline())
                    raw_payload = self.ser.read(data_size)
                    unpack_type(type_id, raw_payload)

            except Exception as e:
                print("Exception: " + str(e))
                continue

            # self.log_file.write(f"{self.current_time},{self.current_position},{self.current_error},\n")
            sys.stdout.write(f"\rmessage = {message}     ")
            sys.stdout.flush()


reader = EncoderReader()
reader.loop()

