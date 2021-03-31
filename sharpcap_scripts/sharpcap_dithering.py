# IronPython Pad. Write code snippets here and F5 to run. If code is selected, only selection is run.
import os
import time
import random

dither_max_ra = 50
dither_max_dec = 200
RA_AXIS = 1
DEC_AXIS = 0
last_dec_dir = 0


def get_random_xy():
    xx = random.randrange(-dither_max_ra, dither_max_ra)
    yy = random.randrange(-dither_max_dec, dither_max_dec)
    return xx, yy


def move_to(ra, dec):
    global last_dec_dir
    delta_ra = ra - current_RA
    delta_dec = dec - current_DEC
    print("Current ra = " + str(current_RA) + ", current dec = " + str(current_DEC))
    print("Moving to ra=" + str(ra) + ", dec=" + str(dec))
    time_to_move_in_ra = float(abs(delta_ra)) / 1000.0
    time_to_move_in_dec = float(abs(delta_dec)) / 1000.0
    dir_ra = -1.0 if delta_ra < 0 else 1.0
    dir_dec = -2.0 if delta_dec < 0 else 2.0
    print("delta dec = " + str(delta_dec) + ", dir dec = " + str(dir_dec))
    print("delta ra = " + str(delta_ra) + ", dir ra = " + str(dir_ra))
    if last_dec_dir != dir_dec:
        time_to_move_in_dec += 0.3
        pass
    last_dec_dir = dir_dec
    SharpCap.Mounts.SelectedMount.MoveAxis(RA_AXIS, dir_ra)
    print("RA: sleeping for " + str(time_to_move_in_ra))
    time.sleep(time_to_move_in_ra)
    SharpCap.Mounts.SelectedMount.MoveAxis(RA_AXIS, 0)
    time.sleep(1)
    SharpCap.Mounts.SelectedMount.MoveAxis(DEC_AXIS, dir_dec)
    print("DEC: sleeping for " + str(time_to_move_in_dec))
    time.sleep(time_to_move_in_dec)
    SharpCap.Mounts.SelectedMount.MoveAxis(DEC_AXIS, 0)
    time.sleep(3)


def take_picture(i):
    file_name = "capture" + str(i) + ".fits"
    file_path = os.path.join(SharpCap.Settings.CaptureFolder, "dithering", file_name)
    print("file path = " + file_path)
    SharpCap.SelectedCamera.CaptureSingleFrameTo(file_path)


def dither():
    x, y = get_random_xy()
    move_to(x, y)
    return x, y


N = 600
M = 10
current_RA = 0
current_DEC = 0

for i in range(100, N):
    take_picture(i)
    if (i % M) == M-1:
        print("Start dithering...")
        ra, dec = dither()
        current_RA = ra
        current_DEC = dec
        print("Dithering finished!")

