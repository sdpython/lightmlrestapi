# -*- coding: utf-8 -*-
"""
@brief      test log(time=3s)
"""
import unittest
import pickle
import base64
import numpy
import falcon
import falcon.testing as testing  # pylint: disable=E0401,R0402
from PIL import Image
import ujson
from pyquickhelper.pycode import get_temp_folder
from lightmlrestapi.testing import dummy_mlstorage
from lightmlrestapi.args.args_images import bytes2string
from lightmlrestapi.args import zip_dict
from lightmlrestapi.testing import template_dl_light
from lightmlrestapi.testing.data import get_wiki_img


class TestMLStorageAppImage(testing.TestCase):

    def setUp(self):
        super(TestMLStorageAppImage, self).setUp()
        temp = get_temp_folder(__file__, "temp_dummy_app_storage_imgn")
        self.app = dummy_mlstorage(self.app, folder_storage=temp, folder=temp)

    def _data_dl(self, tweak=False):
        # file
        name = template_dl_light.__file__
        with open(name, "r", encoding="utf-8") as f:
            code = f.read()
        if tweak:
            code = code.replace("def restapi", "def rest3api")
        code = code.replace("iris2.pkl", "dlimg.pkl")
        code = code.encode("utf-8")

        img = get_wiki_img()
        arr = numpy.array(Image.open(img))
        model_data = pickle.dumps(arr)

        data = {"dlimg.pkl": model_data,
                "model.py": code}

        zipped = zip_dict(data)
        ret = {'cmd': 'upload',
               'name': 'mlapi/imgn',
               'zip': bytes2string(zipped)}
        return ret, arr

    def test_dummy_app_storage_img(self):
        # upload model
        obs, X = self._data_dl()
        bodyin = ujson.dumps(obs, reject_bytes=False)
        body = self.simulate_post('/', body=bodyin)
        self.assertEqual(body.status, falcon.HTTP_201)
        d = ujson.loads(body.content)
        self.assertEqual(d, {'name': 'mlapi/imgn'})

        # test model
        ba = base64.b64encode(pickle.dumps(X))
        obs = dict(cmd='predict', name='mlapi/imgn', input=ba, format='img')
        bodyin = ujson.dumps(obs, reject_bytes=False)
        body = self.simulate_post('/', body=bodyin)
        res = ujson.loads(body.content)
        if 'description' in res:
            raise Exception(res["description"])
        self.assertIn('output', res)
        self.assertIn('version', res)
        pred = res['output']
        self.assertEqual(pred, 0)

        # upload model
        obs, X = self._data_dl(tweak=True)
        bodyin = ujson.dumps(obs, reject_bytes=False)
        body = self.simulate_post('/', body=bodyin)
        self.assertEqual(body.status, falcon.HTTP_400)
        self.assertIn(b"Unable to upload model due to:", body.content)

        # test model
        js = base64.b64encode(b"r" + pickle.dumps(X))
        obs = dict(cmd='predict', name='mlapi/imgn', input=js, format='img')
        bodyin = ujson.dumps(obs, reject_bytes=False)
        body = self.simulate_post('/', body=bodyin)
        self.assertEqual(body.status, falcon.HTTP_400)
        res = ujson.loads(body.content)
        self.assertIn('title', res)
        self.assertIn(
            "Unable to predict with model 'mlapi/imgn'", res['title'])


if __name__ == "__main__":
    unittest.main()
