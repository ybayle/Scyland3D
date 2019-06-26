# Scyland3D: Processing 3D landmarks

``Scyland3D`` is a Python tool for converting 3D raw landmark and semilandmark coordinates exported from landmark acquisition software (e.g. [Landmark Editor 3.6 from IDAV, UC Davis](http://www.idav.ucdavis.edu/research/EvoMorph)) to a csv format best suited for geometric morphometric analyses.
Processing schemes to mirror and reorder these points are provided to address further symmetry issues.

By:
- Fidji Berio ([GitHub](https://github.com/fberio)) from [ISEM](http://www.isem.univ-montp2.fr/en/) and [IGFL](http://igfl.ens-lyon.fr/igfl/annuaire/berio-fidji),
- Yann Bayle ([Website](http://yannbayle.fr/english/index.php), [GitHub](https://github.com/ybayle)) from [LaBRI](http://www.labri.fr/), [Univ. Bordeaux](https://www.u-bordeaux.fr/), [CNRS](http://www.cnrs.fr/), and [SCRIME](https://scrime.u-bordeaux.fr/).

## Installation

Install and update using pip:

`pip install -U Scyland3D`

Dependencies:

- [Python](https://www.python.org/) 2 or 3. **Scyland3D** has been tested with Python 2.7.16 and 3.6.3 and **should** work with older versions of Python.
- [Numpy](https://www.numpy.org/) >= 1.13.3. **Scyland3D** has been tested with Numpy 1.13.3 and 1.16.2 and **should** work with older versions of Numpy.

If you encounter an error with other versions, please [submit an issue](https://github.com/ybayle/Scyland3D/issues/new).

## Use-case example

To quickly process landmarks files, you can give **Scyland3D** the path to the folder containing the `.pts` files (format defined on page 37 in http://www.idav.ucdavis.edu/research/projects/EvoMorph/supplement/LandmarkDoc_v3_b6.pdf), as shown in the example files provided:

```
import Scyland3D
Scyland3D.pts2csv("example/")
```

This will create a file named `landmarks.csv` that you can use for statistical analyses in any language/software you want.
The example files provided come from a subset of our dataset for studying teeth of the small-spotted catshark *Scyliorhinus canicula*.
We provide 7 landmark and 31 semilandmark coordinates for 2 upper teeth and for 3 lower ones, stored in two folders that describe the specimens they belong to.
A landmark is a point set up by hand as opposed to a semilandmark that is interpolated by the computer between two landmarks by following the curvature of the studied form.

## API documentation

The function `pts2csv()` is the core of **Scyland3D** and is also called when using the script from the terminal with the following arguments:

- *indir* (required)
    - A string containing the input directory where the files are stored. File names can specify the feature modalities separated by `_` (e.g. speciesA_ageX_sex1.pts).
    - Default: Use the "example/" folder
    - Example: `Scyland3D.pts2csv("path/")`
    - Command line: `python Scyland3D.py -i "path/"`
- *order* (optional)
    - A list of integer indicating the new order to apply to the landmarks. The order_factor argument must also be supplied.
    - Default: None
    - Example: `Scyland3D.pts2csv(order_factor="upper", order=[36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 37])`
    - Command line: `python Scyland3D.py -f "upper" -o "36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 37"`
- *order_factor* (optional)
    - A string containing the keyword for items that need their landmarks and semilandmarks to be reordered. The order argument must also be supplied.
    - Default: None
    - Example: if the dataset contains lower and upper teeth where only the upper teeth need to be reordered, one can use: `Scyland3D.pts2csv(order_factor="upper", order=[36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 37])`
    - Command line: `python Scyland3D.py -f "upper" -o "36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 37"`. This is only valid if the keyword `upper` is present in the file name.
- *feature_names* (optional)
    - A list of string containing the feature names.
    - Default: None
    - Example: `Scyland3D.pts2csv(feature_names=["identifier", "species", "location", "length", "sex", "stage", "jaw", "position", "generation"])`
    - Command line: `python Scyland3D.py -n "identifier,species,location,length,sex,stage,jaw,position,generation"`
- *verbose* (optional)
    - A boolean indicating if information should be printed on the console by the process.
    - Default: True
    - Example: `Scyland3D.pts2csv(verbose=False)`
    - Command line: `python Scyland3D.py -v False` for removing the display of information to the console.
- *mirror_factor* (optional)
    - A string containing the keyword for items to be mirrored in the 3D space.
    - Default: None
    - Example: `Scyland3D.pts2csv(mirror_factor="upper")`
    - Command line: `python Scyland3D.py -m "upper"` will mirror in 3D the files containing the keyword `upper` before processing them with the remaining `lower` items as depicted in the figure below:

![Landmarks on a tooth](https://raw.githubusercontent.com/ybayle/Scyland3D/master/paper/figure1.png)

More information can be found on the [related article](https://github.com/openjournals/joss-papers/blob/joss.01153/joss.01153/10.21105.joss.01153.pdf).

## How To Contribute

Contributions are welcome!
Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

**Scyland3D** is licensed under the MIT License as described in the [license file](LICENSE). Please use the following citation:

```
@article{Berio2019,
    author  = {Berio, Fidji and Bayle, Yann},
    title   = {{Scyland3D: Processing 3D landmarks}},
    journal = {{The Journal of Open Source Software}},
    page    = {1153--1155},
    volume  = {4},
    issue   = {33},
    doi     = {10.21105/joss.01153},
    note    = {Review pending}
}
```

## Acknowledgements

We acknowledge the contribution of SFR Biosciences (UMS3444/CNRS, US8/Inserm, ENS de Lyon, UCBL) facilities: AniRA-ImmOs and Mathilde Bouchet for her help with X-ray microtomography.
