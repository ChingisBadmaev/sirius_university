import math
import unittest


class Prime:
    # empty constructor
    def __init__(self):
        pass

    def is_prime(self, n):
        for i in range(2, int(math.sqrt(n) + 1)):
            if n % i == 0:
                return False
        return True

    def prime_numbers(self, start, finish):
        sum = 0
        for i in range(start, finish + 1, 1):
            if self.is_prime(i):
                sum += i
        return sum


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.prime = Prime()

    def test_1(self):
        self.assertEqual(self.prime.prime_numbers(10, 20), 60)

    def test2(self):
        self.assertEqual(self.prime.prime_numbers(2, 50), 328)

    def test3(self):
        self.assertEqual(self.prime.prime_numbers(15, 63), 460)

    def test4(self):
        self.assertEqual(self.prime.prime_numbers(80, 100), 269)

    def test5(self):
        self.assertEqual(self.prime.prime_numbers(3, 4), 3)

    def test6(self):
        self.assertEqual(self.prime.prime_numbers(0, 0), 0)

    def test7(self):
        self.assertEqual(self.prime.prime_numbers(170, 180), 352)

    def test8(self):
        self.assertEqual(self.prime.prime_numbers(80, 100), 269)

    def test9(self):
        self.assertEqual(self.prime.prime_numbers(500, 1000), 54591)

    def test10(self):
        self.assertEqual(self.prime.prime_numbers(1000, 1100), 16826)


if __name__ == "__main__":
    unittest.main()
