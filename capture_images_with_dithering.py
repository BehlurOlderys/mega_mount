import time
import os
import sys
#sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("C:\\Users\\Florek\Desktop\\_STEROWANIE")


from random_dithering import RandomDithering
from mount_commander import MountCommander


def PerformSingleDitheredImagingSession(N):
   ditherer = RandomDithering(75)
   mount = MountCommander(150, ra_backlash_s=7, dec_backlash_s=6)

   clr.AddReference("System.Drawing")
   import System.Drawing
   SharpCap.SelectedCamera.Controls.OutputFormat.Value = 'TIFF files (*.tif)'
   # SharpCap.SelectedCamera.Controls.Exposure.Value = E
   for i in range(0, N):
      SharpCap.SelectedCamera.CaptureSingleFrameTo("C:\\Users\\Florek\Desktop\\_STEROWANIE\\test_output\\capture_"+str(i)+".tif")
      # if i % 2:
      mount.move_arcsec(*ditherer.get_random_axis_direction_and_amount())
      time.sleep(2)  # to reduce vibrations


PerformSingleDitheredImagingSession(10)
