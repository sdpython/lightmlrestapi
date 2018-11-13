# -*- coding: utf-8 -*-
"""
@brief      test log(time=10s)
"""

import sys
import os
import unittest
import pickle
import textwrap
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
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

from src.lightmlrestapi.mlapp.mlstorage import MLStorage, ZipStorage


class TestStorage(ExtTestCase):

    def test_storage(self):
        temp = get_temp_folder(__file__, "temp_zip_storage")
        stor = ZipStorage(temp)
        data = {'one.txt': b"1", 'two.txt': b"2"}
        stor.add("dto-/k_", data)
        data2 = stor.get("dto-/k_")
        self.assertEqual(data, data2)
        names = list(stor.enumerate_names())
        self.assertEqual(names, ["dto-/k_"])
        meta = stor.get_metadata("dto-/k_")
        self.assertEqual(meta, {})

    def mlstorage(self, n):

        # Train a model
        iris = datasets.load_iris()
        X = iris.data[:, :2]  # we only take the first two features.
        y = iris.target
        clf = LogisticRegression()
        clf.fit(X, y)
        model_data = pickle.dumps(clf)

        # application
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

        app = {"iris2.pkl": model_data, "model.py": code}

        temp = get_temp_folder(__file__, "temp_ml_storage")
        stor = MLStorage(temp, cache_size=3)

        for i in range(0, n):
            name = "ml/iris%d" % i
            stor.add(name, app)
            data2 = stor.get(name)
            self.assertEqual(app, data2)
            names = list(stor.enumerate_names())
            self.assertNotEmpty(names)
            meta = stor.get_metadata(name)
            self.assertEqual(meta, {'main_script': 'model.py'})

            exp = clf.predict_proba(X[:1, :2])
            predict = stor.call_predict(name, X[:1, :2])
            self.assertEqual(exp, predict)

        self.assertLesser(len(stor._cache), n)  # pylint: disable=W0212

    def test_mlstorage(self):
        self.mlstorage(1)

    def test_mlstorage_multi(self):
        self.mlstorage(6)


if __name__ == "__main__":
    unittest.main()
