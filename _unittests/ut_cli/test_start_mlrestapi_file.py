"""
@brief      test tree node (time=8s)
"""


import sys
import os
import unittest
import pickle
import re
import textwrap

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


try:
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..", "..", "pyquickhelper", "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyquickhelper as skip_


from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder
from src.lightmlrestapi.cli.make_ml_app import _start_mlrestapi


class TestStartMlRestApiFile(unittest.TestCase):

    def test_start_mlrestapi_file(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        # We build a model.
        from sklearn import datasets
        from sklearn.linear_model import LogisticRegression
        temp = get_temp_folder(__file__, "temp_start_mlrestapi_file")

        iris = datasets.load_iris()
        X = iris.data[:, :2]  # we only take the first two features.
        y = iris.target
        clf = LogisticRegression()
        clf.fit(X, y)

        dest = os.path.join(temp, "iris2.pickle")
        with open(dest, "wb") as f:
            pickle.dump(clf, f)

        # We extract the code from
        doc = os.path.join(temp, "..", "..", "..", "_doc",
                           "sphinxdoc", "source", "tutorial", "first_rest_api.rst")
        with open(doc, "r", encoding="utf-8") as f:
            page = f.read()
        page = page.replace("\r", "").replace("\n", "#LINE#")
        reg = re.compile("[.][.] runpython::(.*?)if __name__")
        fall = reg.findall(page)
        if len(fall) == 0:
            raise Exception("Unable to find code in\n{0}".format(
                page.replace('#LINE#', '\n')))
        code = fall[0]
        if ".. runpython::" in code:
            code = code.split(".. runpython::")[-1]
        code = code.replace('#LINE#', '\n')
        code = code.replace(':showcode:', '')
        code = textwrap.dedent(code)
        code = code.replace('iris2.pickle', dest.replace('\\', '\\\\'))

        dest = os.path.join(temp, "mymlrestapi.py")
        with open(dest, "w", encoding="utf-8") as f:
            f.write(code)

        # We run the app.
        rows = []

        def flog(*l):
            rows.append(l)

        _start_mlrestapi(args=['--name=dummyfct', '--option={0}'.format(dest),
                               '--nostart=True'], fLOG=flog)

        r = rows[0][0]
        if not r.startswith("[start_mlrestapi] do not run serve"):
            raise Exception(r)


if __name__ == "__main__":
    unittest.main()
