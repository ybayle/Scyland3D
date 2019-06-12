# -*- coding: utf-8 -*-
#
# Authors   Fidji Berio and Yann Bayle
# E-mails   fidji.berio@ens-lyon.fr and bayle.yann@live.fr
# License   MIT
# Created   15/02/2018
# Updated   12/06/2019
# Version   1.0.3
#

import os
import csv
import sys
import getopt
import numpy as np


def _export2csv(data, nb_landmark, indir, modif=""):
    """export2csv
    Export data to a CSV named indir + "../landmarks" + modif + ".csv"
    """
    # Generate the header of the csv
    fieldnames = ["ID"]
    for numb in range(1, nb_landmark + 1):
        for axe in ["x", "y", "z"]:
            fieldnames.append(axe + str(numb))
    nb_feature = len(data[0]) - nb_landmark * 3 - 1
    for numb in range(1, nb_feature + 1):
        fieldnames.append("Feature" + str(numb))
    # Export the header and the data  
    with open(indir + "../landmarks" + modif + ".csv", "w") as out_file:
        csv.DictWriter(out_file, fieldnames=fieldnames).writeheader()
        csv.writer(out_file).writerows(data)


def _list_pts(indir):
    """list_pts
    Recursively lists all .pts file from indir
    """
    assert os.path.exists(indir) and os.path.isdir(indir), indir + " not found."
    filenames = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(indir)) for f in fn]
    filenames = [filen for filen in filenames if ".pts" in filen]
    assert filenames, "There are no .pts files in " + indir
    return filenames


def _remove_duplicates(data):
    """remove_duplicates
    Remove the duplicates landmarks and semi-landmarks
    """
    # Remove easy duplicates where the string are an exact match
    data = sorted(set(data), key=data.index)
    # Remove duplicates up to epsilon because some (semi-)landmarks are exported with different float precision
    coord = []
    for item in data:
        tmp = []
        for xyz in item.split(","):
            tmp.append(float(xyz))
        coord.append(tmp)
    index_to_remove = []
    for k in range(3):
        for i in range(len(coord) - 1):
            for j in range(len(coord) - i - 1):
                if coord[i][k] == coord[i + j + 1][k]:
                    # If two coordinates are the same, then the rows are duplicates and will be removed
                    tmp = [0, 1, 2]
                    tmp.remove(k)
                    if (coord[i][tmp[0]] == coord[i + j + 1][tmp[0]]) or (coord[i][tmp[1]] == coord[i + j + 1][tmp[1]]):
                        index_to_remove.append(i + j + 1)
    new_data = []
    for i, item in enumerate(coord):
        if i not in index_to_remove:
            new_data.append(item)
    return new_data


def _reverse_z(data):
    """reverse_z
    good https://www.youtube.com/watch?v=86lwcXeZoiA
    wrong https://stackoverflow.com/questions/8954326/how-to-calculate-the-mirror-point-along-a-line#8954454
    """
    matrix_xy = []
    matrix_z = []
    for xyz in data:
        x = xyz[0]
        y = xyz[1]
        z = xyz[2]
        matrix_xy.append([x, y, 1])
        matrix_z.append(z)
    b = np.matrix(matrix_z).T
    A = np.matrix(matrix_xy)
    fit = (A.T * A).I * A.T * b

    A = fit[0]
    B = fit[1]
    C = -1.
    D = -fit[2]
    data_mirror = []
    for xyz in data:
        x = xyz[0]
        y = xyz[1]
        z = xyz[2]
        t = float((D - A*x - B*y - C*z) / (A*A + B*B + C*C))
        xp = float(x + 2.*A*t)
        yp = float(y + 2.*B*t)
        zp = float(z + 2.*C*t)
        data_mirror.append([xp, yp, zp])
    return data_mirror


def pts2csv(indir="example/", mirror_factor=None, order=None, order_factor=None, verbose=True):
    """pts2csv
    Convert .pts files from indir to a single .csv file
    """
    assert os.path.exists(indir) and os.path.isdir(indir), indir + " not found."
    assert (order is None and order_factor is None) or (order is not None and order_factor is not None), "Must supply order and order_factor."
    if indir[-1] != os.sep:
        indir += os.sep

    nb_feature = 0
    nb_landmark = 0
    list_pts_files = _list_pts(indir)
    data2write = []
    # For each .pts file
    for index, filen in enumerate(list_pts_files):
        if verbose:
            print(str(index + 1) + "/" + str(len(list_pts_files)) + " " + filen)
        # Count the number of feature in that file
        nb_detected_feature = filen[filen.find(os.sep) + 1:].count("_") + filen.count(os.sep)
        if nb_feature == 0:
            # Use the number of features from the first .pts file as reference
            nb_feature = nb_detected_feature
        else:
            # Check that the number of feature between all .pts files are consistent
            assert nb_feature == nb_detected_feature, "The name of the file or of the directory does not seems to be consistent because for " + filen + " because there are " + str(nb_detected_feature) + " detected features while " + str(nb_feature) + " were expected."
        data = []
        # Gather semi-landmarks (S) and landmarks (C)
        with open(filen, "r") as filep:
            for line in filep:
                if line[0] in ["S", "C"]:
                    data.append(",".join(line[:-1].split("  ")[1:]))
        # Remove duplicates landmarks generated that are generally present in the .pts files
        data = _remove_duplicates(data)
        if nb_landmark == 0:
            nb_landmark = len(data)
        assert len(data) == nb_landmark, "Some landmarks may not be correctly superimposed for " + filen + " because there are " + str(len(data)) + " landmarks detected instead of " + str(nb_landmark)
        modif = ""
        # Apply a z-axis mirror to the landmarks to study left-right differences in the given species 
        if mirror_factor is not None and mirror_factor in filen:
            data = _reverse_z(data)
            modif += "_reversed"
        # Reorder the landmarks to avoir bias during landmarks set up by humans
        if order_factor is not None and order_factor in filen:
            data = np.array(data)
            data = data[order]
            data = data.tolist()
            modif += "_reordered"
        # Add new row to data
        row = [filen]
        data = np.array(data)
        for val in data.reshape(data.shape[0] * data.shape[1]):
            row.append(val) 
        filen = filen.split(".")[0]
        for feature in filen[filen.find(os.sep) + 1:].replace("_", ",").replace("-", ".").replace("/", ",").replace("\\", ",").split(","):
            row.append(feature) 
        data2write.append(row)
    _export2csv(data2write, nb_landmark, indir, modif)


def _usage():
    """usage
    Print usage to the user when using option -h or when invalid options are provided
    """
    sys.exit("Scyland3D.py -i <input_directory> [-m <mirror_factor>] [-o <order> -f <order_factor>] [-v <verbosity_level>]")


def main(argv):
    """main entry point
    Parse arguments and call the function to convert multiple .pts files to a single csv file
    """
    indir = "example/"
    mirror_factor = None
    order = None
    order_factor = None
    verbose = True
    try:
        opts, args = getopt.getopt(argv,"hi:m:o:f:v:", ["indir=", "mirror_factor=", "order=", "order_factor=" "verbose="])
    except getopt.GetoptError:
        _usage()
    for opt, arg in opts:
        if opt == "-h":
            _usage()
        elif opt in ("-i", "--indir"):
            indir = arg
        elif opt in ("-m", "--mirror_factor"):
            mirror_factor = arg
        elif opt in ("-o", "--order"):
            order = arg
        elif opt in ("-f", "--order_factor"):
            order_factor = arg
        elif opt in ("-v", "--verbose"):
            verbose = [True if arg == "True" or arg == "true" or arg == "t" or arg == "T" else False]
    pts2csv(indir=indir, mirror_factor=mirror_factor, order=order, order_factor=order_factor, verbose=verbose)


if __name__ == '__main__':
    main(sys.argv[1:])
