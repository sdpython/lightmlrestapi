"""
@brief      test tree node (time=12s)
"""
import unittest
import numpy
from pyquickhelper.pycode import ExtTestCase
from lightmlrestapi.tools import json_loads, json_dumps


class TestJsonHelper(ExtTestCase):

    def test_dict(self):
        obj = dict(a=1, b='g')
        js = json_dumps(obj)
        obj2 = json_loads(js)
        self.assertEqual(obj, obj2)

    def test_numpy(self):
        obj = numpy.array([[0, 1], [1, 2], [3, 5]])
        js = json_dumps(obj)
        obj2 = json_loads(js)
        self.assertEqualArray(obj, obj2)

    def test_numpy_dict(self):
        obj = dict(t=1, j=numpy.array([[0, 1], [1, 2], [3, 5]]))
        js = json_dumps(obj)
        obj2 = json_loads(js)
        self.assertIsInstance(obj2, dict)
        self.assertIn('j', obj2)
        self.assertEqualArray(obj['j'], obj2['j'])


if __name__ == "__main__":
    unittest.main()
