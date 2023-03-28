import unittest

from graycode import gen_gray_codes, gray_code_to_tc, tc_to_gray_code


class GrayCodeTestCase(unittest.TestCase):
    def setUp(self):
        self._num_bits = 8
        self._gray_codes = gen_gray_codes(self._num_bits)

    def test_gen_gray_codes_3_bits(self):
        assert self._num_bits >= 3
        self.assertEqual(self._gray_codes[:8], [0, 1, 3, 2, 6, 7, 5, 4])

    def test_gen_gray_codes_unique(self):
        s = set()
        for g in self._gray_codes:
            self.assertNotIn(g, s)
            s.add(g)

    def test_gray_code_to_tc(self):
        for x in range(1 << self._num_bits):
            g = self._gray_codes[x]
            self.assertEqual(x, gray_code_to_tc(g))

    def test_tc_to_gray_code(self):
        for x in range(1 << self._num_bits):
            self.assertEqual(self._gray_codes[x], tc_to_gray_code(x))

    def test_gray_code_to_tc_bijection(self):
        for x in range(1 << self._num_bits):
            self.assertEqual(x, gray_code_to_tc(tc_to_gray_code(x)))
            self.assertEqual(x, tc_to_gray_code(gray_code_to_tc(x)))


if __name__ == '__main__':
    unittest.main()
