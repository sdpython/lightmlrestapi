# -*- coding: utf-8 -*-
"""
@brief      test log(time=10s)
"""

import sys
import os
import unittest
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


class TestStorage(ExtTestCase):

    def test_storage(self):
        temp = get_temp_folder(__file__, "temp_storage")
        stor = MLStorage(temp)
        data = {'one.txt': b"1", 'two.txt': b"2"}
        stor.add("dto-/k_", data)
        data2 = stor.get("dto-/k_")
        self.assertEqual(data, data2)
        names = list(stor.enumerate_names())
        self.assertEqual(names, ["dto-/k_"])


if __name__ == "__main__":
    unittest.main()
