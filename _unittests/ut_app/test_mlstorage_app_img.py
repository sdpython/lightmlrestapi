# -*- coding: utf-8 -*-
"""
@brief      test log(time=3s)
"""

import sys
import os
import unittest
import pickle
import base64
import numpy
import falcon
import falcon.testing as testing
from PIL import Image
from pyquickhelper.pycode import get_temp_folder
import ujson


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

from src.lightmlrestapi.testing import dummy_mlstorage
from src.lightmlrestapi.args.args_images import bytes2string
from src.lightmlrestapi.args import zip_dict
from src.lightmlrestapi.testing import template_dl_light
from src.lightmlrestapi.testing.data import get_wiki_img


class TestMLStorageAppImage(testing.TestBase):

    def before(self):
        temp = get_temp_folder(__file__, "temp_dummy_app_storage")
        dummy_mlstorage(self.api, folder_storage=temp, folder=temp)

    def _data_dl(self, tweak=False):
        # model

        # file
        name = template_dl_light.__file__
        with open(name, "r", encoding="utf-8") as f:
            code = f.read()
        if tweak:
            code = code.replace("def restapi", "def rest3api")
        code = code.encode("utf-8")

        img = get_wiki_img()
        arr = numpy.array(Image.open(img))
        model_data = pickle.dumps(arr)

        data = {"dlimg.pkl": model_data,
                "model.py": code}

        zipped = zip_dict(data)
        ret = {'cmd': 'upload',
               'name': 'ml/img',
               'zip': bytes2string(zipped)}
        return ret, arr

    def test_dummy_app_storage_img(self):
        # upload model
        obs, X = self._data_dl()
        bodyin = ujson.dumps(obs)
        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)
        d = ujson.loads(body)
        self.assertEqual(d, {'name': 'ml/img'})

        # test model
        ba = base64.b64encode(pickle.dumps(X))
        obs = dict(cmd='predict', name='ml/img', input=ba, format='img')
        bodyin = ujson.dumps(obs)
        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        res = ujson.loads(body)
        self.assertIn('output', res)
        self.assertIn('version', res)
        pred = res['output']
        self.assertEqual(pred, 0)

        # upload model
        obs, X = self._data_dl(tweak=True)
        bodyin = ujson.dumps(obs)
        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        self.assertIn("Unable to upload model due to:", body)

        # test model
        js = base64.b64encode(b"r" + pickle.dumps(X))
        obs = dict(cmd='predict', name='ml/img', input=js, format='img')
        bodyin = ujson.dumps(obs)
        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        res = ujson.loads(body)
        self.assertIn('title', res)
        self.assertIn("Unable to predict with model 'ml/img'", res['title'])


if __name__ == "__main__":
    unittest.main()
