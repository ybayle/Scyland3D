# Scyland3D: Processing 3D landmarks

**Scyland3D** is a Python tool for converting 3D raw landmark and semilandmark coordinates to a usable format for geometric morphometric analyses.
Processing schemes to mirror and reorder these points are provided to address further symmetry issues.

By:
- Fidji Berio ([GitHub](https://github.com/fberio)) from [ISEM](http://www.isem.univ-montp2.fr/en/) and [IGFL](http://igfl.ens-lyon.fr/igfl/annuaire/berio-fidji),
- Yann Bayle ([Website](http://yannbayle.fr/english/index.php), [GitHub](https://github.com/ybayle)) from [LaBRI](http://www.labri.fr/), [Univ. Bordeaux](https://www.u-bordeaux.fr/), [CNRS](http://www.cnrs.fr/), and [SCRIME](https://scrime.u-bordeaux.fr/).

## Installation

Install and update using pip:

`pip install -U Scyland3D`

Dependencies:

- [Python](https://www.python.org/)
- [Numpy](https://www.numpy.org/)

## Use-case example

To quickly process landmarks files, you can give **Scyland3D** the path to the folder containing the `.pts` files, as shown in the example files provided:

```
import Scyland3D
Scyland3D.pts2csv("example/")
```

This will create a file named `landmarks.csv` that you can use for statistical analyses in any language/software you want.
The example files provided come from a subset of our dataset for studying teeth of the small-spotted catshark *Scyliorhinus canicula*.
We provide 7 landmark and 31 semilandmark coordinates for 2 upper teeth and for 3 lower ones, stored in two folders that describe the specimens they belong to.

## API documentation

The function `pts2csv()` is the core of **Scyland3D** and takes the following arguments:

- *indir* (required)
    - A string containing the input directory where the files are stored. You can use any number of sub-directories. Folder and file names can specify the feature modalities separated by `_` (e.g. speciesA_ageX_sex1.pts).
    - Example: `Scyland3D.pts2csv("example/")`
- *mirror_factor* (optional)
    - A string containing the keyword for items to be mirrored in the 3D space.
    - Default: None
    - Example: `Scyland3D.pts2csv("example/", mirror_factor="upper")` will mirror in 3D the files containing the keyword `upper` before processing them with the remaining `lower` items.
- *order* (optional)
    - A list of integer indicating the new order to apply to the landmarks.
    - Default: None
    - Example: `Scyland3D.pts2csv("example/", order_factor="upper", order=[36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 37])`
- *order_factor* (optional)
    - A string containing the keyword for items that need their landmarks and semilandmarks to be reordered.
    - Default: None
    - Example: `Scyland3D.pts2csv("example/", order_factor="upper", order=[36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 37])`
- *feature_names* (optional)
    - A list of string containing the feature names.
    - Default: None
    - Example: `Scyland3D.pts2csv("example/", feature_names=["identifier", "species", "location", "length", "sex", "stage", "jaw", "position", "generation"])`
- *verbose* (optional)
    - A boolean indicating if information should be printed on the console by the process.
    - Default: True
    - Example: `Scyland3D.pts2csv("example/", verbose=False)` for removing the display of information to the console.

More information can be found on the [related article](TODOLinkToJOSS).

## How To Contribute

Contributions are welcome!
Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

**Scyland3D** is licensed under the GNU Affero General Public License v3.0 as described in the [license file](LICENSE).
**Scyland3D** was mainly created for research purposes and thus can be used freely for research and academic use with the following citation:

```
@article{Berio2019,
    author  = {Berio, Fidji and Bayle, Yann},
    title   = {{Scyland3D: Processing 3D landmarks}},
    journal = {{The Journal of Open Source Software}},
    page    = {1--3},
    note    = {Review pending}
}
```

## Acknowledgements

We acknowledge the contribution of SFR Biosciences (UMS3444/CNRS, US8/Inserm, ENS de Lyon, UCBL) facilities: AniRA-ImmOs and Mathilde Bouchet for her help with X-ray microtomography.
