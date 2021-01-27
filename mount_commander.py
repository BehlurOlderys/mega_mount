import time
from System.IO.Ports import SerialPort

commands = {
   "RA" : {
      "P" : "RA_PLUS",
      "N" : "RA_MINUS"
   },
   "DEC":{
      "P" : "DEC_PLUS",
      "N" : "DEC_MINUS"
   }
}


class MountCommander:
   def __init__(self, speed_as_per_s, ra_backlash_s, dec_backlash_s):
      self.speed_as_per_s = speed_as_per_s
      self.backlash_s = {"RA": ra_backlash_s, "DEC": dec_backlash_s}
      self.last_dir = {"RA": "P", "DEC": "P"}

      self.ser = SerialPort(PortName='COM3', BaudRate=115200)
      self.ser.ReadTimeout = 500
      self.ser.WriteTimeout = 500
      self.ser.Open()
      time.sleep(1)

      reply = self.ser.ReadLine().rstrip()

      while not (reply == "OK"):
         self.ser.WriteLine("INIT_COMMAND 0")
         reply = self.ser.ReadLine().rstrip()
         print("Init replied with: "+reply)
         time.sleep(1)

      # pre-load dec
      self._move_seconds("DEC", "P", 0)

   def __del__(self):
      print("Finalizing mount!")
      self.ser.Close()

   def _move_seconds(self, axis, direction, amount):
      antibacklash_ra = False
      if axis == "DEC" and direction is not self.last_dir[axis]:
         amount += self.backlash_s[axis]
         self.last_dir[axis] = direction
      if axis == "RA":
         if direction is "N":
            amount += self.backlash_s[axis]
            antibacklash_ra = True



      print("Moving in axis "+axis+" in direction "+direction+" for "+str(amount)+"s")
      amount_ms = int(amount*1000)

      send_command = commands[axis][direction] + " " + str(amount_ms) + "\n"
      print("Sending command: " + send_command)
      self.ser.Write(send_command)
      print("Mount answered: " + self.ser.ReadLine())
      time.sleep(amount+1)

      if antibacklash_ra is True:
         print("Resetting backlash in RA axis for "+str(self.backlash_s["RA"])+"s")
         amount_ms = int(1000*self.backlash_s["RA"])
         send_command = commands["RA"]["P"] + " " + str(amount_ms) + "\n"
         print("Sending command: " + send_command)
         self.ser.Write(send_command)
         print("Mount answered: " + self.ser.ReadLine())
         time.sleep(self.backlash_s["RA"]+1)


   def move_arcsec(self, axis, direction, amount):
      amount_s = amount / self.speed_as_per_s
      self._move_seconds(axis, direction, amount_s)