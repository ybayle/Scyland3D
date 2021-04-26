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

class TestsProject3Dto2D:
    def test_project3Dto2D(self):
        points3D = []
        points2D = Scyland3D.project3Dto2D(points3D)
        print(points2D)
        assert False
