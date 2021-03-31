import subprocess
import os
import time


def solve_image():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"Dir path = {dir_path}")

    current_ra = 101
    current_dec = 22
    search_radius = 20


    current_ra_str = str(current_ra)
    current_dec_str = str(current_dec)
    search_radius_str = str(search_radius)

    pixel_size_um = 3.75
    pixel_size_um_str = str(pixel_size_um)
    focal_length = 135
    focal_length_str = str(focal_length)
    input_file_name = "input.fits"
    output_file_name = input_file_name + "_ps_.txt"
    input_file_path = os.path.join(dir_path, input_file_name)
    output_file_path = os.path.join(dir_path, output_file_name)
    exe_file_path = "C:\\Program Files (x86)\\PlateSolver\\PlateSolver.exe"
    exe_command = "/solvefile"

    time_start = time.time()
    subprocess.call([exe_file_path,
                      exe_command,
                      input_file_path,
                      output_file_path,
                      focal_length_str,
                      pixel_size_um_str,
                      current_ra_str,
                      current_dec_str,
                      search_radius_str])
    #subprocess.call([exe_file_path,
    #                 exe_command,
    #                 input_file_path,
    #                 output_file_path,
    #                 focal_length_str,
    #                 pixel_size_um_str])

    time_end = time.time()
    solve_time_formatted = "{:.2f}".format(time_end-time_start)
    print(f"Solving took {solve_time_formatted} seconds")

    with open(output_file_path) as f:
        lines = f.readlines()
    os.remove(output_file_path)

    is_result_ok = (lines[0].strip() == "OK")
    if is_result_ok is not True:
        print(f"Plate solve failed! First line = {lines[0]}")
        return None

    solved_ra = float(lines[1])
    solved_dec = float(lines[2])
    return solved_ra, solved_dec


if __name__ == "__main__":
    print(solve_image())
