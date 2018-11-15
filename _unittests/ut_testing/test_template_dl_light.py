"""
@brief      test tree node (time=8s)
"""


import sys
import os
import unittest
import pickle
import numpy
from PIL import Image
from pyquickhelper.pycode import get_temp_folder, ExtTestCase

try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

from src.lightmlrestapi.testing.template_dl_light import restapi_version, restapi_load, restapi_predict
from src.lightmlrestapi.testing.data import get_wiki_img


class TestTemplateDlLight(ExtTestCase):

    def test_template_dl_light(self):
        self.assertEqual(restapi_version(), "0.1.1235")
        temp = get_temp_folder(__file__, "temp_template_dl_light")
        img_input = os.path.join(temp, "..", "data", "wiki_modified2.png")
        img_input = numpy.array(Image.open(img_input))

        img = get_wiki_img()
        arr = numpy.array(Image.open(img))

        pkl = os.path.join(temp, "model.pkl")
        with open(pkl, "wb") as f:
            pickle.dump(arr, f)

        mo = restapi_load(pkl)
        pred = restapi_predict(mo, arr)
        self.assertEqual(pred, 0)
        pred = restapi_predict(mo, img_input)
        self.assertAlmostEqual(pred, 0.000577306896768102)


if __name__ == "__main__":
    unittest.main()
