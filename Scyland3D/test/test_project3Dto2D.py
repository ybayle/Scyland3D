# -*- coding: utf-8 -*-
#
# Authors   Fidji Berio and Yann Bayle
# E-mails   fidji.berio@ens-lyon.fr and bayle.yann@live.fr
# License   MIT
# Created   26/04/2021
#

import os
import sys
sys.path.insert(0, os.path.join(__file__, "..", ".."))
import Scyland3D
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

class TestsProject3Dto2D:
    def test_exportToDelete(self):
        dirn = os.path.join(os.path.dirname(__file__), "")
        filen = dirn + "3d_hatchlings.txt"
        new_str = ""
        with open(filen, "r") as filep:
            new_str += next(filep)
            for line in filep:
                points3D = line
                points3D = points3D.split(",")[1:3*38+1]
                xs = []
                ys = []
                zs = []
                for i in np.arange(len(points3D), step=3):
                    xs.append(float(points3D[i]))
                    ys.append(float(points3D[i+1]))
                    zs.append(float(points3D[i+2]))
                data = []
                for val_x, val_y, val_z in zip(xs, ys, zs):
                    data.append([val_x, val_y, val_z])

                newData = Scyland3D._reverse_z(data)

                new_str += line.split(",")[0] + ","
                for xyz in newData:
                    new_str += str(xyz[0]) + "," + str(xyz[1]) + "," + str(xyz[2]) + ","
                new_str += ",".join(line.split(",")[3*38+1:])
        with open(dirn + "hatchlings_2D_plane_in_3D.txt", "w") as filep:
            filep.write(new_str)

        assert False

    def test_project3Dto2D(self):
        
        def displayPoints(xs, ys, zs):
            plt.figure()
            ax = plt.axes(projection='3d')
            # ax.plot3D(xs, ys, zs)
            ax.scatter(xs, ys, zs)
            plt.show()

        dirn = os.path.join(os.path.dirname(__file__), "")
        filen = dirn + "3d_hatchlings.txt"
        with open(filen, "r") as filep:
            next(filep)
            points3D = next(filep)
        points3D = points3D.split(",")[1:3*38+1]
        xs = []
        ys = []
        zs = []
        for i in np.arange(len(points3D), step=3):
            xs.append(float(points3D[i]))
            ys.append(float(points3D[i+1]))
            zs.append(float(points3D[i+2]))

        displayPoints(xs, ys, zs)

        data = []
        for val_x, val_y, val_z in zip(xs, ys, zs):
            data.append([val_x, val_y, val_z])

        newData = Scyland3D._reverse_z(data)
        new_xs = []
        new_ys = []
        new_zs = []
        for xyz in newData:
            new_xs.append(xyz[0])
            new_ys.append(xyz[1])
            new_zs.append(xyz[2])
        displayPoints(new_xs, new_ys, new_zs)

        # points2D = Scyland3D.project3Dto2D(points3D)

        plt.figure()
        plt.plot(new_xs, new_ys, "o")
        plt.show()

        assert False
