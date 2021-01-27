import random


class RandomDithering:
   def __init__(self, radius_as):
      self.radius_as = radius_as

   def get_random_axis_direction_and_amount(self):
      axis = random.choice(["DEC", "RA"])
      direction = random.choice(["P", "N"])
      amount = int(self.radius_as*random.random())
      return axis, direction, amount


