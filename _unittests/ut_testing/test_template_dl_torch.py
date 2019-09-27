"""
@brief      test tree node (time=12s)
"""
import os
import unittest
import numpy
from PIL import Image
from pyquickhelper.pycode import get_temp_folder, ExtTestCase
from lightmlrestapi.testing.template_dl_torch import restapi_version, restapi_load, restapi_predict


def get_torch():
    try:
        import torch  # pylint: disable=C0415
        return torch
    except ImportError:
        return None


class TestTemplateDlTorch(ExtTestCase):

    @unittest.skipIf(get_torch() is None, reason="no torch")
    def test_template_dl_keras(self):
        self.assertEqual(restapi_version(), "0.1.1238")
        temp = get_temp_folder(__file__, "temp_template_dl_torch")

        import torchvision.models as models  # pylint: disable=E0401,C0415
        import torch  # pylint: disable=E0401,C0415
        model = models.squeezenet1_0(pretrained=True)
        model_name = os.path.join(temp, "model.torch")
        torch.save(model, model_name)

        img_input = os.path.join(temp, "..", "data", "wiki_modified2.png")
        img_input = numpy.array(Image.open(img_input))

        mo = restapi_load({'model': model_name})
        pred = restapi_predict(mo, img_input)
        self.assertIsInstance(pred, numpy.ndarray)
        self.assertEqual(pred.shape, (1, 1000))


if __name__ == "__main__":
    unittest.main()
