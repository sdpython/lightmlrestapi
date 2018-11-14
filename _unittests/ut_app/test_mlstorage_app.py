# -*- coding: utf-8 -*-
"""
@brief      test log(time=3s)
"""

import sys
import os
import unittest
import pickle
import textwrap
import numpy
import falcon
import falcon.testing as testing
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


class TestMLStorageApp(testing.TestBase):

    def before(self):
        temp = get_temp_folder(__file__, "temp_dummy_app_storage")
        dummy_mlstorage(self.api, folder_storage=temp, folder=temp)

    def _data(self, tweak=False):
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
        code = textwrap.dedent("""
        import pickle

        # We declare an id for the REST API.
        def restapi_version():
            return "0.1.1234"

        # We declare a loading function.
        def restapi_load():
            with open("iris2.pkl", "rb") as f:
                loaded_model = pickle.load(f)
            return loaded_model

        # We declare a predict function.
        def restapi_predict(clf, X):
            return clf.predict_proba(X)
        """)
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
        obs, X, clf = self._data()
        bodyin = ujson.dumps(obs)
        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)
        d = ujson.loads(body)
        self.assertEqual(d, {'name': 'ml/iris'})

        # test model
        js = ujson.dumps([list(X[0])])
        obs = dict(cmd='predict', name='ml/iris', input=js, format='json')
        bodyin = ujson.dumps(obs)
        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        res = ujson.loads(body)
        self.assertIn('output', res)
        pred = res['output']
        exp = clf.predict_proba(X[:1])
        res = numpy.array(pred)
        self.assertEqual(res.shape, exp.shape)
        res = res.ravel()
        exp = exp.ravel()
        diff = numpy.abs(res - exp).sum()
        self.assertTrue(diff < 1e-5)

        # upload model
        obs, X, clf = self._data(tweak=True)
        bodyin = ujson.dumps(obs)
        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        self.assertIn("Unable to upload model due to:", body)

        # test model
        js = ujson.dumps([[list(X[0])]])
        obs = dict(cmd='predict', name='ml/iris', input=js, format='json')
        bodyin = ujson.dumps(obs)
        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        res = ujson.loads(body)
        self.assertIn('title', res)
        self.assertIn("Unable to predict with model 'ml/iris'", res['title'])


if __name__ == "__main__":
    unittest.main()
