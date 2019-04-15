"""
@brief      test tree node (time=12s)
"""
import os
import unittest
import numpy
from PIL import Image
from pyquickhelper.pycode import get_temp_folder, ExtTestCase
from lightmlrestapi.testing.template_dl_keras import restapi_version, restapi_load, restapi_predict


def get_keras():
    try:
        import keras
        return keras
    except ImportError:
        return None


class TestTemplateDlKeras(ExtTestCase):

    @unittest.skipIf(get_keras() is None, reason="no keras")
    def test_template_dl_keras(self):
        self.assertEqual(restapi_version(), "0.1.1237")
        temp = get_temp_folder(__file__, "temp_template_dl_keras")

        from keras.applications.mobilenet import MobileNet  # pylint: disable=E0401
        model = MobileNet(input_shape=None, alpha=1.0, depth_multiplier=1,
                          dropout=1e-3, include_top=True,
                          weights='imagenet', input_tensor=None,
                          pooling=None, classes=1000)
        model_name = os.path.join(temp, "model.keras")
        model.save(model_name)

        img_input = os.path.join(temp, "..", "data", "wiki_modified2.png")
        img_input = numpy.array(Image.open(img_input))

        mo = restapi_load({'model': model_name})
        pred = restapi_predict(mo, img_input)
        self.assertIsInstance(pred, numpy.ndarray)
        self.assertEqual(pred.shape, (1, 1000))


if __name__ == "__main__":
    unittest.main()
