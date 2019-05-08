# -*- coding: utf-8 -*-
"""
@brief      test log(time=3s)
"""
import unittest
import pickle
import numpy
import falcon
import falcon.testing as testing
import ujson
from pyquickhelper.pycode import get_temp_folder
from lightmlrestapi.testing import dummy_mlstorage
from lightmlrestapi.args.args_images import bytes2string
from lightmlrestapi.args import zip_dict
from lightmlrestapi.testing import template_ml


class TestMLStorageApp(testing.TestCase):

    def setUp(self):
        super(TestMLStorageApp, self).setUp()
        temp = get_temp_folder(__file__, "temp_dummy_app_storage")
        self.app = dummy_mlstorage(self.app, folder_storage=temp, folder=temp)

    def _data_sklearn(self, tweak=False):
        # model
        from sklearn import datasets
        from sklearn.linear_model import LogisticRegression

        iris = datasets.load_iris()
        X = iris.data[:, :2]  # we only take the first two features.
        y = iris.target
        clf = LogisticRegression()
        clf.fit(X, y)
        model_data = pickle.dumps(clf)

        # file
        name = template_ml.__file__
        with open(name, "r", encoding="utf-8") as f:
            code = f.read()
        if tweak:
            code = code.replace("def restapi", "def rest3api")
        code = code.encode("utf-8")

        data = {"iris2.pkl": model_data,
                "model.py": code}

        zipped = zip_dict(data)
        ret = {'cmd': 'upload',
               'name': 'ml/iris',
               'zip': bytes2string(zipped)}
        return ret, X, clf

    def test_dummy_app_storage(self):
        # upload model
        obs, X, clf = self._data_sklearn()
        bodyin = ujson.dumps(obs)
        body = self.simulate_post('/', body=bodyin)
        self.assertEqual(body.status, falcon.HTTP_201)
        d = ujson.loads(body.content)
        self.assertEqual(d, {'name': 'ml/iris'})

        # test model
        js = ujson.dumps([list(X[0])])
        obs = dict(cmd='predict', name='ml/iris', input=js, format='json')
        bodyin = ujson.dumps(obs)
        body = self.simulate_post('/', body=bodyin)
        res = ujson.loads(body.content)
        self.assertIn('output', res)
        self.assertIn('version', res)
        pred = res['output']
        exp = clf.predict_proba(X[:1])
        res = numpy.array(pred)
        self.assertEqual(res.shape, exp.shape)
        res = res.ravel()
        exp = exp.ravel()
        diff = numpy.abs(res - exp).sum()
        self.assertTrue(diff < 1e-5)

        # upload model
        obs, X, clf = self._data_sklearn(tweak=True)
        bodyin = ujson.dumps(obs)
        body = self.simulate_post('/', body=bodyin)
        self.assertEqual(body.status, falcon.HTTP_400)
        self.assertIn(b"Unable to upload model due to:", body.content)

        # test model
        js = ujson.dumps([[list(X[0])]])
        obs = dict(cmd='predict', name='ml/iris', input=js, format='json')
        bodyin = ujson.dumps(obs)
        body = self.simulate_post('/', body=bodyin)
        self.assertEqual(body.status, falcon.HTTP_400)
        res = ujson.loads(body.content)
        self.assertIn('title', res)
        self.assertIn("Unable to predict with model 'ml/iris'", res['title'])


if __name__ == "__main__":
    unittest.main()
