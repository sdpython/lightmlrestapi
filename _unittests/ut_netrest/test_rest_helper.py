# -*- coding: utf-8 -*-
"""
@brief      test log(time=10s)
"""
import os
import unittest
import pickle
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from pyquickhelper.pycode import get_temp_folder, ExtTestCase
from lightmlrestapi.netrest import json_upload_model, json_predict_model
from lightmlrestapi.testing import template_ml


class TestRestHelper(ExtTestCase):

    def test_json_upload_model(self):
        temp = get_temp_folder(__file__, "temp_json_upload_model")

        # train a model
        iris = datasets.load_iris()
        X = iris.data[:, :2]  # we only take the first two features.
        y = iris.target
        clf = LogisticRegression()
        clf.fit(X, y)
        model_data = pickle.dumps(clf)

        model_file = os.path.join(temp, "model_iris.pkl")
        with open(model_file, "wb") as f:
            f.write(model_data)

        # application
        with open(template_ml.__file__, "r") as f:
            code = f.read()
        code = code.replace("iris2.pkl", "model_iris.pkl")
        pyfile = os.path.join(temp, "model.py")
        with open(pyfile, "w", encoding="utf-8") as f:
            f.write(code)

        req = json_upload_model(name="m1", pyfile=pyfile, data=model_file)
        js = req
        self.assertIn('name', js)
        self.assertIn('cmd', js)
        self.assertIn('zip', js)

    def test_json_predict_model(self):
        iris = datasets.load_iris()
        X = iris.data[:, :2]  # we only take the first two features.
        name = "m1"
        req = json_predict_model(name, X)
        self.assertIsInstance(req, dict)
        self.assertIn('cmd', req)
        self.assertIn('name', req)
        self.assertIn('input', req)


if __name__ == "__main__":
    unittest.main()
