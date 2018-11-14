# -*- coding: utf-8 -*-
"""
@brief      test log(time=3s)
"""

import sys
import os
import unittest
import pickle
import textwrap
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


class TestMLStorageApp(testing.TestBase):

    def before(self):
        temp = get_temp_folder(__file__, "temp_dummy_app_storage")
        dummy_mlstorage(self.api, folder_storage=temp, folder=temp)

    def _data(self):
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
        code = code.encode("utf-8")

        return {"iris2.pkl": bytes2string(model_data),
                "model.py": bytes2string(code),
                'cmd': 'upload', 'name': 'ml/iris'}

    def test_dummy_app_storage(self):
        obs = self._data()
        bodyin = ujson.dumps(obs)
        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        self.assertEqual(self.srmock.status, falcon.HTTP_201)
        d = ujson.loads(body)
        self.assertEqual(d, {'name': 'ml/iris'})

    def a_test_dummy_error(self):
        bodyin = ujson.dumps({'X': [0.1, 0.2, 0.3]})
        body = self.simulate_request(
            '/', decode='utf-8', method="POST", body=bodyin)
        self.assertEqual(self.srmock.status, falcon.HTTP_400)
        d = ujson.loads(body)
        self.assertIn('Unable to predict', d['title'])
        self.assertIn('X has 3 features per sample; expecting 2', d['title'])
        self.assertIn('.py', d['description'])


if __name__ == "__main__":
    unittest.main()
