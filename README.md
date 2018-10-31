# Transposon

A genetic algorithm problem solver loosely based on transposons. Can be used to solve non deterministic problems and approach general optimums. 

*"(Noun) A transposable element (TE or transposon) is a DNA sequence that can change its position within a genome, sometimes creating or reversing mutations and altering the cell's genetic identity and genome size." -Wikipedia*

## Overview

Transposon attempts to solve complex problems through evolutionary algorithms. The program mutates integer arrays of set length based on a provided fitness function. 

<b>*See the examples folder for examples using the transposon class including a traveling salesman example.</b>

### Example instantiation:
```python
transposon = Transposon(
	vector_len=len(cities),
	fitness_func=fitness_func,
	min_value=0,
	max_value=max_value,
	population_size=1000,
	max_fitness=MAX_FITNESS,
	max_generations=100,
	mutation_rate=0.13,
	transposon_rate=0.13,
	transposon_len=5,
	verbose=True)
results = transposon.evolve()
print("BEST RESULT :", results[0])

```

### Example array (gene): 
```
[0,1,2,1,0,20,14] 
```

These arrays can then be applied to a fitness function 

### Example fitness function:

```python
def my_fitness_func(vector):
	""" each fitness function must accept an array of integers and return a numerical value """
	
	#simple fitness function, return the sum of the first three items
	return vector[0]+vector[1]+vector[2]
```

## Variables

`vector_len = <int>` The length of the arrays that will be returned from the transposon class and sent to the fitness function, must be > 0. 

`fitness_func = <function>` This is the provided fitness function must accept an array of integers and return a numerical value. This is where you add your specific domain based problem. 

Note: The array can have duplicates in the numbers (not unique) thus its important to make sure if you are mapping these integers to unique values to keep this in mind. See the traveling salesman example for turning a list of numbers with duplicates into a list of cities without duplicates. 

`min_value = <int>` This is the minimum value possible in the integer array (gene)

`max_value = <int>` This is hte maximum value possible in the integer array (gene)

`population_size = <int>` This is the number of individuals we will have for each generation

`max_fitness = <float>` This is the maximum fitness or target we are approaching. The genetic algorithm will quit when this target has been reached or exceeded. 

Note: some optimization problems try to minimize a fitness, see the traveling salesman problem for an example of how to handle this

`max_generations = <int>` The maximum number of generations that will be run before either reaching the desired fitness or quitting

`mutation_rate = <float>` The rate of random mutations occuring per item in array, sampled independently. Each item in the array will be mutated based on this probability to a random value within the acceptable range. Value must be between 0.0 and 1.0

`transposon_rate=<float>` The rate at which an individual is selected for a transposon insertion. If the individual is selected then there will be a random transposon extraction/insertion.  

`transposon_len=<int>` The length of the transposon sequence which will be shuffled. 

`winner_pool = <float>` The percentage of "winners" we will retain from generation to generation. Must be between 0.0 and 1.0. 

`verbose = <boolean> ` Whether or not to print a report during each generation on the current fitness






