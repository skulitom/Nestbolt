"""Regression for material errors introduced by browser SVGMatrix float rounding."""
import math
import unittest

from svg_export_transform import rigid_matrix, groups_from_exports


class SvgExportPrecisionTests(unittest.TestCase):
    def test_native_fractional_coordinates_are_preserved(self):
        literal = 'translate(15598.1814491 -3951.8785134) rotate(90)'
        matrix = rigid_matrix(literal)
        self.assertEqual(matrix[4:], [15598.1814491, -3951.8785134])
        self.assertNotEqual(matrix[4], 15598.181640625)  # actual Chromium SVGMatrix value
        self.assertAlmostEqual(matrix[1], 1)
        exported = f'<svg xmlns="http://www.w3.org/2000/svg"><g transform="{literal}"><polygon id="copy-0" points="0,0 1,0 0,1"/><polygon id="copy-0-hole-1"/></g></svg>'
        self.assertEqual(groups_from_exports([exported])[0][0], {'outer_id':'copy-0','hole_ids':['copy-0-hole-1'],'matrix':matrix})

    def test_nonquarter_and_scientific_notation_remain_rigid(self):
        matrix = rigid_matrix(' translate(2.3e-12, -4.5e+3) rotate(-22.5) ')
        self.assertEqual(matrix[4:], [2.3e-12,-4500])
        self.assertAlmostEqual(matrix[0],math.cos(math.radians(-22.5)))
        self.assertAlmostEqual(matrix[1],math.sin(math.radians(-22.5)))
        self.assertAlmostEqual(matrix[0]*matrix[3]-matrix[1]*matrix[2],1)

    def test_extra_transform_unknown_syntax_and_nonfinite_fail(self):
        for text in ['scale(2)', 'translate(1 2) rotate(3) scale(2)', 'translate(1e999 0) rotate(0)', 'matrix(1 0 0 1 0 0)']:
            with self.assertRaises(ValueError):rigid_matrix(text)
        with self.assertRaises(ValueError):
            groups_from_exports(['<svg xmlns="http://www.w3.org/2000/svg"><g transform="translate(1 2) rotate(0)"><polygon id="copy-0" transform="scale(2)"/></g></svg>'])


if __name__ == '__main__':
    unittest.main()
