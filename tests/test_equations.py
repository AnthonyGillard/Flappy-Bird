import unittest
from equations import calculate_derivative_multi_by_time


class TestEquations(unittest.TestCase):
    def test_calculate_derivative_multi_by_time_returns_expected_with_int_result(self):
        derivative = 20
        time = 2

        delta = calculate_derivative_multi_by_time(derivative, time)

        self.assertEqual(40, delta)

    def test_calculate_derivative_multi_by_time_returns_expected_with_non_int_result(self):
        derivative = 20.4
        time = 2

        delta = calculate_derivative_multi_by_time(derivative, time)

        self.assertEqual(40, delta)
