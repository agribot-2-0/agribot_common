#!/usr/bin/env python3

import sys
import os
import glob


def convert_tms(main_directory):
    for z in os.listdir(main_directory):
        z_direcotry = os.path.join(main_directory, z)
        if os.path.isdir(z_direcotry):
            print("Z: {}".format(z))
            os.chdir(z_direcotry)

            for x in os.listdir(z_direcotry):
                x_direcotry = os.path.join(z_direcotry, x)
                if os.path.isdir(x_direcotry):
                    print("  X: {}".format(x))
                    os.chdir(x_direcotry)

                    for filename_png in sorted(glob.glob('*.png')):
                        zoom_level = int(z)
                        y_old = int(filename_png.split('.')[0])
                        y_new = (2**zoom_level) - y_old - 1
                        y_filename_new = "{}.{}".format(y_new, "png")
                        os.rename(filename_png, y_filename_new)
                        print("    Y: {} -> {}".format(filename_png, y_filename_new))

    print('Tiles successfully converted!')


if __name__ == "__main__":
    if len(sys.argv) == 2:
        convert_tms(sys.argv[1])
    else:
        print("Enter the path of the folder containing.")
        print("Example: ( $ ./tms-to-xyz.py /home/agribot/agribot_maps )")
