"""
@brief      test tree node (time=12s)
"""


import sys
import os
import unittest
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

from src.lightmlrestapi.testing.template_dl_torch import restapi_version, restapi_load, restapi_predict


def get_torch():
    try:
        import torch
        return torch
    except ImportError:
        return None


class TestTemplateDlTorch(ExtTestCase):

    @unittest.skipIf(get_torch() is None, reason="no torch")
    def test_template_dl_keras(self):
        self.assertEqual(restapi_version(), "0.1.1238")
        temp = get_temp_folder(__file__, "temp_template_dl_torch")

        import torchvision.models as models  # pylint: disable=E0401
        import torch  # pylint: disable=E0401
        model = models.squeezenet1_0(pretrained=True)
        model_name = os.path.join(temp, "model.torch")
        torch.save(model, model_name)

        img_input = os.path.join(temp, "..", "data", "wiki_modified2.png")
        img_input = numpy.array(Image.open(img_input))

        mo = restapi_load(model_name)
        pred = restapi_predict(mo, img_input)
        self.assertIsInstance(pred, numpy.ndarray)
        self.assertEqual(pred.shape, (1, 1000))


if __name__ == "__main__":
    unittest.main()
