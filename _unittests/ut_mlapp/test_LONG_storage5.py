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

from src.lightmlrestapi.mlapp.mlstorage import MLStorage


class TestStorage5(ExtTestCase):

    def mlstorage(self, n, suf):

        # Train a model
        iris = datasets.load_iris()
        X = iris.data[:, :2]  # we only take the first two features.
        y = iris.target
        clf = LogisticRegression()
        clf.fit(X, y)
        model_data = pickle.dumps(clf)

        # application
        code = textwrap.dedent("""
        import os
        import pickle

        # We declare an id for the REST API.
        def restapi_version():
            return "0.1.1234"

        # We declare a loading function.
        def restapi_load():
            here = os.path.dirname(__file__)
            with open(os.path.join(here, "iris2.pkl"), "rb") as f:
                loaded_model = pickle.load(f)
            return loaded_model

        # We declare a predict function.
        def restapi_predict(clf, X):
            return clf.predict_proba(X)
        """)
        temp = get_temp_folder(__file__, "temp_ml_storage" + suf)
        stor = MLStorage(temp, cache_size=3)

        for i in range(0, n):
            app = {"iris_%d.pkl" % i: model_data,
                   "model.py": code.replace("iris2.pkl", "iris_%d.pkl" % i).encode("utf-8")}

            name = "ml%s/iris%d" % (suf, i)
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
            version = stor.call_version(name)
            self.assertEqual(version, "0.1.1234")

        self.assertLesser(len(stor._cache), n)  # pylint: disable=W0212

    def test_mlstorage_multi(self):
        self.mlstorage(5, "5")


if __name__ == "__main__":
    unittest.main()
