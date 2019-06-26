# -*- coding: utf-8 -*-
#
# Authors   Fidji Berio and Yann Bayle
# E-mails   fidji.berio@ens-lyon.fr and bayle.yann@live.fr
# License   MIT
# Created   15/02/2018
# Updated   25/06/2019
#

import os
import csv
import sys
import getopt
import numpy as np


def _export2csv(data, nb_landmark, outdir=None, feature_names=None, modif=""):
    """export2csv
    Export data to a CSV named indir + "../landmarks" + modif + ".csv".

    Args:
        data (array): The landmarks to export.
        nb_landmark (int): The number of landmarks.
        outdir (str): The name of the directory where the output files will be stored. If not
            provided the current working directory will be used.
        feature_names (str or array of str): String describing each feature names separated with a
            comma or array of string (e.g. "age,sex,size" if supplied from the command line or
            ["age", "sex", "size"] if supplied in python script).
        modif (str): The name of the modification applied to the data (e.g. none, reversed, and/or
            reordered).
    """
    # Generate the header of the csv
    fieldnames = ["ID"]
    assert nb_landmark > 0, "The number of landmarks must be positive."
    for numb in range(1, nb_landmark + 1):
        for axe in ["x", "y", "z"]:
            fieldnames.append(axe + str(numb))
    nb_feature = len(data[0]) - nb_landmark * 3 - 1
    if feature_names is not None:
        if isinstance(feature_names, str):
            feature_names = feature_names.split(",")
        assert nb_feature == len(feature_names), (
            "The number of feature names provided ("
            + str(len(feature_names))
            + ") does not match the number of features detected in the files ("
            + str(nb_feature)
            + ")."
        )
        for feature_name in feature_names:
            fieldnames.append(feature_name)
    else:
        for numb in range(1, nb_feature + 1):
            fieldnames.append("Feature" + str(numb))
    # Export the header and the data
    if outdir is None:
        outdir = "./"
    output_filename = os.path.join(os.path.abspath(outdir), "landmarks" + modif + ".csv")
    with open(output_filename, "w") as out_file:
        csv.DictWriter(out_file, fieldnames=fieldnames).writeheader()
        csv.writer(out_file).writerows(data)
    print("File successfully generated: " + output_filename)


def _list_pts(indir):
    """list_pts
    Recursively lists all .pts file from indir.

    Args:
        indir (str): The name of the directory where the .pts files are stored.

    Returns:
        An array of .pts file names to process. 
    """
    assert os.path.exists(indir) and os.path.isdir(indir), indir + " not found."
    filenames = [
        os.path.join(dp, f)
        for dp, dn, fn in os.walk(os.path.expanduser(indir))
        for f in fn
    ]
    filenames = [filen for filen in filenames if ".pts" in filen]
    assert filenames, "There are no .pts files in " + indir
    return filenames


def _remove_duplicates(data):
    """remove_duplicates
    Remove the duplicates landmarks and semi-landmarks.

    Args:
        data (array): Contains the landmarks.

    Returns:
        An array of landmarks where duplicates were removed.
    """
    # Remove easy duplicates where the string are an exact match
    data = sorted(set(data), key=data.index)
    # Remove duplicates because some landmarks and semilandmarks are sometimes exported twice.
    coord = []
    for item in data:
        coord.append([float(xyz) for xyz in item.split(",")])
    index_to_remove = []
    for k in range(3):
        for i in range(len(coord) - 1):
            for j in range(len(coord) - i - 1):
                if coord[i][k] == coord[i + j + 1][k]:
                    # If two landmarks share at least two similar coordinates, then the rows are
                    # considered as duplicates and the second one will be removed.
                    tmp = [0, 1, 2]
                    tmp.remove(k)
                    if (coord[i][tmp[0]] == coord[i + j + 1][tmp[0]]) or (
                        coord[i][tmp[1]] == coord[i + j + 1][tmp[1]]
                    ):
                        index_to_remove.append(i + j + 1)
    new_data = []
    for i, item in enumerate(coord):
        if i not in index_to_remove:
            new_data.append(item)
    return new_data


def _reverse_z(data):
    """reverse_z
    Find the relative z-axis for a given set of point by computing a plane that minimizes the
    difference between it and the given points.
    Then reverses the set of points relatively to this new plane, so no user specific plane has to
    be supplied.
    Inspired from https://www.youtube.com/watch?v=86lwcXeZoiA and the suggestion from
    https://stackoverflow.com/questions/8954326/how-to-calculate-the-mirror-point-along-a-line#8954454
    is not applicable here as it is not valid in 3D and does not take into account relative axes. 

    Args:
        data (array): Contains the landmarks.

    Returns:
        An array of landmarks inverted along the z-axis.
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
    C = -1.0
    D = -fit[2]
    data_mirror = []
    for xyz in data:
        x = xyz[0]
        y = xyz[1]
        z = xyz[2]
        t = float((D - A * x - B * y - C * z) / (A * A + B * B + C * C))
        xp = float(x + 2.0 * A * t)
        yp = float(y + 2.0 * B * t)
        zp = float(z + 2.0 * C * t)
        data_mirror.append([xp, yp, zp])
    return data_mirror


def _get_path(filen):
    """_get_path
    Return the absolute path of the provided file name from the absolute resources directory.

    Args:
        filen (str): The name of the file in the relative path of the package.

    Returns:
        An absolute path to the custom resources provided with the package.
    """
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), filen)


def pts2csv(
    indir=None,
    outdir=None,
    mirror_factor=None,
    order=None,
    order_factor=None,
    feature_names=None,
    verbose=True,
):
    """pts2csv
    Convert .pts files from indir to a single .csv file

    Args:
        indir (str): The name of the directory where the output files will be stored.
        mirror_factor (str): The name of the factor to use for mirroring the landmarks on the z-axis.
        order (str or array of int): A string (if supplied by the command line) or an array of int
        (if called from another python script) indicating how to reorder the landmarks (e.g. "1,3,2"
        if supplied from the command line or [1, 3, 2] if supplied by another python script).
        order_factor (str): The name of the factor to use for reordering the landmarks.
        feature_names (str or array of str): String describing each feature names separated with a
        comma or array of string (e.g. "age,sex,size" if supplied from the command line or 
        ["age", "sex", "size"] if supplied in python script).
        verbose (bool): Whether to output details during the process.
    """
    if indir is None:
        indir = _get_path("example/")
        print("Using default example directory: " + indir)
    assert os.path.exists(indir) and os.path.isdir(indir), indir + " not found."
    assert (order is None and order_factor is None) or (
        order is not None
        and order_factor is not None
        and (isinstance(order_factor, str) or isinstance(order_factor, list))
    ), "Must supply order and order_factor."
    if indir[-1] != os.sep:
        indir += os.sep

    nb_feature = 0
    nb_landmark = 0
    list_pts_files = _list_pts(indir)
    data2write = []
    order_factor_found_at_least_in_one_file = False
    # For each .pts file
    for index, filen in enumerate(list_pts_files):
        if verbose:
            print(str(index + 1) + "/" + str(len(list_pts_files)) + " " + filen)
        # Count the number of feature in that file
        nb_detected_feature = filen[filen.find(os.sep) + 1 :].count("_") + filen.count(
            os.sep
        )
        if nb_feature == 0:
            # Use the number of features from the first .pts file as reference
            nb_feature = nb_detected_feature
        else:
            # Check that the number of feature between all .pts files are consistent
            assert nb_feature == nb_detected_feature, (
                "The name of the file or of the directory does not seems to be consistent because for "
                + filen
                + " because there are "
                + str(nb_detected_feature)
                + " detected features while "
                + str(nb_feature)
                + " were expected."
            )
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
        assert len(data) == nb_landmark, (
            "Some landmarks may not be correctly superimposed for "
            + filen
            + " because there are "
            + str(len(data))
            + " landmarks detected instead of "
            + str(nb_landmark)
        )
        modif = ""
        # Apply a z-axis mirror to the landmarks to study left-right differences in the given species
        if (
            mirror_factor is not None
            and isinstance(mirror_factor, str)
            and mirror_factor in filen
        ):
            data = _reverse_z(data)
            modif += "_reversed"
        # Reorder the landmarks as specified by the order argument only for the files containing the
        # order_factor string.
        if order_factor is not None and order_factor in filen:
            order_factor_found_at_least_in_one_file = True
            if isinstance(order, str):
                order = [int(val) for val in order.split(",")]
            data = np.array(data)
            data = data[order]
            data = data.tolist()
            modif += "_reordered"
        # Add new row to data
        row = ["/".join(filen.split(os.sep)[-2:])]
        data = np.array(data)
        for val in data.reshape(data.shape[0] * data.shape[1]):
            row.append(val)
        filen = filen.split(".")[-2]
        for feature in (
            filen[filen.find(os.sep) + 1 :]
            .replace("_", ",")
            .replace("-", ".")
            .split(os.sep)[-1]
            .split(",")
        ):
            row.append(feature)
        data2write.append(row)
    if order_factor is not None:
        assert order_factor_found_at_least_in_one_file, (
            "The order_factor ("
            + order_factor
            + ") provided has not been found in any file names."
        )
    _export2csv(
        outdir=outdir,
        data=data2write,
        nb_landmark=nb_landmark,
        feature_names=feature_names,
        modif=modif,
    )


def _usage():
    """usage
    Print usage to the user when using option -h or when invalid options are provided
    """
    sys.exit(
        "Scyland3D.py -i <input_directory> [-m <mirror_factor>] [-o <order> -f <order_factor>] [-n <feature_names>] [-v <verbosity_level>]"
    )


def main(argv):
    """main entry point
    Parse arguments and call the function to convert multiple .pts files to a single csv file

    Args:
        argv (array): The list of arguments.
    """
    indir = None
    outdir = None
    mirror_factor = None
    order = None
    order_factor = None
    feature_names = None
    verbose = True
    try:
        opts, args = getopt.getopt(
            argv,
            "hi:o:m:r:f:n:v:",
            [
                "indir=",
                "outdir=",
                "mirror_factor=",
                "order=",
                "order_factor=", "feature_names=", "verbose=",
            ],
        )
    except getopt.GetoptError:
        _usage()
    for opt, arg in opts:
        if opt == "-h":
            _usage()
        elif opt in ("-i", "--indir"):
            indir = arg
        elif opt in ("-o", "--outdir"):
            outdir = arg
        elif opt in ("-m", "--mirror_factor"):
            mirror_factor = arg
        elif opt in ("-r", "--order"):
            order = arg
        elif opt in ("-f", "--order_factor"):
            order_factor = arg
        elif opt in ("-n", "--feature_names"):
            feature_names = arg
        elif opt in ("-v", "--verbose"):
            verbose = (
                True
                if arg == "True" or arg == "true" or arg == "t" or arg == "T"
                else False
            )
    pts2csv(
        indir=indir,
        outdir=outdir,
        mirror_factor=mirror_factor,
        order=order,
        order_factor=order_factor,
        feature_names=feature_names,
        verbose=verbose,
    )


def _same_file(filen1, filen2):
    assert filen1 != filen2, "File names must be different."
    with open(filen1, "r") as filep_ref:
        with open(filen2, "r") as filep_test:
            for line_ref, line_test in zip(filep_ref, filep_test):
                assert line_ref == line_test, "Invalid line " + line_ref
    return True


def _validation_against_ref():
    print("Testing default behavior...")
    dirn = _get_path("./")
    assert _same_file(
        dirn + "landmarks.csv", dirn + "test/landmarks_ref.csv"
    ), "Generated file does not match the default reference."
    print("Ok!")
    print("Testing reordering...")
    assert _same_file(
        dirn + "landmarks_reordered.csv", dirn + "test/landmarks_reordered_ref.csv"
    ), "Generated file does not match the reference for the reordering."
    print("Ok!")
    print("Testing reversing...")
    assert _same_file(
        dirn + "landmarks_reversed.csv", dirn + "test/landmarks_reversed_ref.csv"
    ), "Generated file does not match the reference for the reversing."
    print("Ok!")


def test_no_regression():
    verbose = False
    order_factor = "upper"
    outdir = _get_path("./")
    order = [
        36,
        35,
        34,
        33,
        32,
        31,
        30,
        29,
        28,
        27,
        26,
        25,
        24,
        23,
        22,
        21,
        20,
        19,
        18,
        17,
        16,
        15,
        14,
        13,
        12,
        11,
        10,
        9,
        8,
        7,
        6,
        5,
        4,
        3,
        2,
        1,
        0,
        37,
    ]
    mirror_factor = "upper"
    feature_names = [
        "identifier",
        "species",
        "location",
        "length",
        "sex",
        "stage",
        "jaw",
        "position",
        "generation",
    ]
    pts2csv(
        outdir=outdir,
        mirror_factor=None,
        order=None,
        order_factor=None,
        feature_names=None,
        verbose=verbose,
    )
    pts2csv(
        outdir=outdir,
        mirror_factor=None,
        order=order,
        order_factor=order_factor,
        feature_names=None,
        verbose=verbose,
    )
    pts2csv(
        outdir=outdir,
        mirror_factor=mirror_factor,
        order=None,
        order_factor=None,
        feature_names=feature_names,
        verbose=verbose,
    )
    _validation_against_ref()


if __name__ == "__main__":
    main(sys.argv[1:])
