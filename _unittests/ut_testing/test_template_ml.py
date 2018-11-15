"""
@brief      test tree node (time=8s)
"""


import sys
import os
import unittest
import pickle
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

from src.lightmlrestapi.testing.template_ml import restapi_version, restapi_load, restapi_predict


class TestTemplateMl(ExtTestCase):

    def test_template_ml(self):
        self.assertEqual(restapi_version(), "0.1.1234")
        temp = get_temp_folder(__file__, "temp_template_ml")

        iris = datasets.load_iris()
        X = iris.data[:, :2]  # we only take the first two features.
        y = iris.target
        clf = LogisticRegression()
        clf.fit(X, y)

        pkl = os.path.join(temp, "model.pkl")
        with open(pkl, "wb") as f:
            pickle.dump(clf, f)

        mo = restapi_load(pkl)
        pred = restapi_predict(mo, X[:1])
        exp = clf.predict_proba(X[:1])
        self.assertEqual(pred, exp)


if __name__ == "__main__":
    unittest.main()
