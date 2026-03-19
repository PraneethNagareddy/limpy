from driver import *
import sys


if not len(sys.argv) != 3:
        print("invalid usage. Provide exactly three arguments, i.e X,Y,Z co-ordinates")

X = int(sys.argv[1])
Y = int(sys.argv[2])
Z = int(sys.argv[3])

front_right_leg.move_to_position(X, Y, Z)