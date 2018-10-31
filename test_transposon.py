import unittest
from transposon import Transposon


class TestTransposon(unittest.TestCase):
	""" Test the transposon class"""


	def test_initialize(self):
		""" Test that the initialization method has necessary assertions to avoid a bad initialization"""
		
		#assert that we have assigned a fitness function
		self.assertRaises(AssertionError, Transposon)

		#assert that we check our fitness function for a valid fitness
		self.assertRaises(AssertionError, Transposon, fitness_func=fitness_func_oob)


	def test_create_vector(self):
		""" Test the create vector method is of correct size and range """
		
		#setup our values
		min_value = 0
		max_value = 100
		range_values = [x for x in range(min_value, max_value+1)]
		range_set = set(range_values)
		t = Transposon(vector_len=100, fitness_func=fitness_func_sum3, min_value=min_value, max_value=max_value)
		v1 = t.create_vector()

		#assert that the vector is of correct size
		self.assertEqual(100,len(v1))
		#assert that the vector values are initialized correctly
		self.assertEqual(range_values, t.values)
		#assert that the created vector does not contain any values outside of our range
		for x in t.values:
			self.assertIn(x,range_set) 

	def test_mutate(self):
		""" test our mutate function"""
		pass

	def test_breed(self):
		""" test our breed function"""
		pass

	def test_evaluate(self):
		""" test our evaluation function"""
		pass

	def test_evolve(self):
		""" test our evolution (main loop) function"""
		pass


#misc functions used for testing
def fitness_func_oob(vector):
	""" out of bounds fitness func, returns a negative fitness"""
	return -1

def fitness_func_large(vector):
	""" returns a very large number for fitness"""
	return 9999999999999999999

def fitness_func_sum3(vector):
	""" returns the sum of the first 3 numbers"""
	return vector[0]+vector[1]+vector[2]

if __name__ == '__main__':
	unittest.main()