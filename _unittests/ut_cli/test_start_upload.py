"""
@brief      test tree node (time=2s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
from lightmlrestapi.cli.make_ml_upload import upload_model
from lightmlrestapi.__main__ import main


class TestUploadModel(ExtTestCase):

    def test_upload_model_help(self):
        rows = []

        def flog(*args):
            rows.append(args)

        main(args=['upload_model', '-h'], fLOG=flog)

        r = rows[0][0]
        if not r.startswith("usage: upload_model"):
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
