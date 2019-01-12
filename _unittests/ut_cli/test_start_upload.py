"""
@brief      test tree node (time=2s)
"""


import sys
import os
import unittest
from pyquickhelper.pycode import ExtTestCase

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


from src.lightmlrestapi.cli.make_ml_upload import upload_model
from src.lightmlrestapi.__main__ import main


class TestUploadModel(ExtTestCase):

    def test_upload_model_help(self):
        rows = []

        def flog(*l):
            rows.append(l)

        main(args=['upload_model', '-h'], fLOG=flog)

        r = rows[0][0]
        if not r.startswith("usage: upload_model [-h] [-l LOGIN] [--pwd PWD]"):
            raise Exception(r)

    def test_upload_model(self):
        rows = []

        def flog(*li):
            rows.append(" ".join(str(_) for _ in li))

        self.assertRaise(lambda: upload_model(
            name="name2", fLOG=flog), FileNotFoundError)
        log = "\n".join(rows)
        self.assertIn("Prepare the JSON request", log)


if __name__ == "__main__":
    unittest.main()
