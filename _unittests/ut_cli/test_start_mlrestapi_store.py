"""
@brief      test tree node (time=8s)
"""
import unittest
from pyquickhelper.pycode import get_temp_folder, ExtTestCase
from lightmlrestapi.cli.make_ml_store import start_mlreststor
from lightmlrestapi.__main__ import main


class TestStartMlRestApiStore(ExtTestCase):

    def test_start_mlreststor_help(self):
        rows = []

        def flog(*args):
            rows.append(args)

        main(args=['start_mlreststor', '-h'], fLOG=flog)

        r = rows[0][0]
        if not r.startswith("usage: start_mlreststor"):
            raise Exception(r)

    def test_start_mlreststor(self):
        rows = []

        def flog(*li):
            rows.append(" ".join(str(_) for _ in li))

        temp = get_temp_folder(__file__, "temp_start_mlreststor")
        app = start_mlreststor(location=temp, nostart=True, fLOG=flog)
        self.assertNotEmpty(app)
        log = "\n".join(rows)
        self.assertIn("[start_mlreststor] do not run serve", log)


if __name__ == "__main__":
    unittest.main()
