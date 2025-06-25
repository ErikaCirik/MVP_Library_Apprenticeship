import unittest
from calculator import Calculator

#xy = Calculator(a=6, b=7)
#print(xy.get_product())

class TestOperations(unittest.TestCase):

    def setUp(self):
            self.operation = Calculator(8,2)

    def test_sum(self): #it must always start with test_
        self.assertEqual(self.operation.get_sum(), 10, 'The sum is wrong')

    def test_diff(self):
        self.assertEqual(self.operation.get_difference(), 6, 'The difference is wrong')

    def test_product(self):
        self.assertEqual(self.operation.get_product(), 16, 'The product is wrong')

    def test_quotient(self):
        self.assertEqual(self.operation.get_quotient(), 4, 'The quotient is wrong')

    def test_division_by_zero(self):
        calculation = Calculator(8, 0)
        with self.assertRaises(ValueError, msg="Division by zero should raise ValueError"):
            calculation.get_quotient()

    def test_negative_division(self):
        calculation = Calculator(-8, 2)
        self.assertEqual(calculation.get_quotient(), -4, "Negative division result is incorrect")

    def test_float_division(self):
        calculation = Calculator(7, 2)
        self.assertAlmostEqual(calculation.get_quotient(), 3.5, places=1, msg="Float division result is incorrect")

    def test_zero_dividend(self):
        calculation = Calculator(0, 5)
        self.assertEqual(calculation.get_quotient(), 0, "Zero dividend result is incorrect")
        
    def test_large_numbers(self):
        calculation = Calculator(10**10, 10**5)
        self.assertEqual(calculation.get_quotient(), 10**5, "Large number division result is incorrect")

    def test_small_floating_point_numbers(self):
        calculation = Calculator(0.0001, 0.0002)
        self.assertAlmostEqual(calculation.get_quotient(), 0.5, places=5, msg="Small floating-point division result is incorrect")

    def test_invalid_inputs(self):
        with self.assertRaises(TypeError, msg="Non-numeric inputs should raise TypeError"):
            Calculator("8", 2).get_quotient()

    def test_boundary_values_divide_by_one(self):
        calculation = Calculator(8, 1)
        self.assertEqual(calculation.get_quotient(), 8, "Division by one result is incorrect")

    def test_boundary_values_one_divided_by_number(self):
        calculation = Calculator(1, 8)
        self.assertAlmostEqual(calculation.get_quotient(), 0.125, places=3, msg="One divided by number result is incorrect")

if __name__ == '__main__':
    unittest.main()

