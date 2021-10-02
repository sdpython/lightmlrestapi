"""
@brief      test log(time=0s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import check_pep8, ExtTestCase


class TestCodeStyle(ExtTestCase):
    """Test style."""

    def test_style_src(self):
        thi = os.path.abspath(os.path.dirname(__file__))
        src_ = os.path.normpath(os.path.join(thi, "..", "..", "src"))
        check_pep8(src_, fLOG=fLOG,
                   pylint_ignore=('C0103', 'C1801', 'R0201', 'R1705', 'W0108', 'W0613',
                                  'E1101', 'W0201', 'W0107', 'C0415', 'R1725', 'W0707',
                                  'R1732', 'W1514', 'E0012', 'C0209'))

    def test_style_test(self):
        thi = os.path.abspath(os.path.dirname(__file__))
        test = os.path.normpath(os.path.join(thi, "..", ))
        check_pep8(test, fLOG=fLOG, neg_pattern="temp_.*",
                   pylint_ignore=('C0103', 'C1801', 'R0201', 'R1705', 'W0108', 'W0613',
                                  'C0111', 'C0414', 'W0107', 'C0415', 'R1725', 'W0707',
                                  'R1732', 'W1514', 'E0012', 'C0209'),
                   skip=["Instance of 'tuple' has no ",
                         "Module 'ujson' has no ",
                         "Module 'falcon' has no 'HTTP_",
                         "should be placed before ",
                         ])


if __name__ == "__main__":
    unittest.main()
