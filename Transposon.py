import numpy as np
from random import randint

class Transposon(object):
	""" Transposon is our general class used for evolutionary 
	algorithms applied to vectors"""

	def __init__(self, 
			vector_len=100, 
			fitness_func=None,
			min_value=0,
			max_value=100,
			population_size=1000,
			max_fitness=1.0,
			max_generations=1000,
			mutation_rate=0.13,
			transposon_rate=0.13,
			transposon_len=5,
			winner_pool=0.10,
			verbose=False):
		
		self.vector_len = vector_len
		self.fitness_func = fitness_func
		self.population_size = population_size
		self.max_fitness = max_fitness
		self.verbose = verbose
		self.winner_pool = winner_pool
		self.values = [x for x in range(min_value, max_value+1)]
		self.max_generations = max_generations
		self.mutation_rate = mutation_rate
		self.min_value = min_value
		self.max_value = max_value
		self.transposon_len = transposon_len
		self.transposon_rate = transposon_rate
		self.initialize()

	def initialize(self):
		""" sets up our population and asserts 
		our fitness func is of correct type
		"""
		assert self.mutation_rate >= 0.0
		assert self.mutation_rate <= 1.0
		assert self.fitness_func != None
		assert self.winner_pool >= 0.0
		assert self.winner_pool <= 1.0
		assert self.vector_len >= 0.0

		#setup a random vector and assert that our fitness_func is of correct type
		random_vector = self.create_vector()
		#use our fitness function, assert that the value is correct
		fitness = self.fitness_func(random_vector)
		assert fitness >= 0.0
		#now create our population
		population = [random_vector]
		for i in range(1,self.population_size):
			population.append(self.create_vector())
		self.population = population


	def create_vector(self, replace=False):
		"""
		Create a random vector
		replace = whether or not we can replace values (default false, ie: each value is unique)
		"""
		return np.random.choice(self.values, self.vector_len, replace=replace).tolist()

	def mutate(self):
		""" create mutations randomly based on the mutation rate
		preserves winner pool so that the best individuals aren't mutated
		"""
		
		if self.mutation_rate == 0:
			return

		mutated_population = []
		
		for i,individual in enumerate(self.population):
			mutation_vec = np.random.choice(2, len(individual), p=[1.0-self.mutation_rate, self.mutation_rate])
			combined_vec = []

			for i,m in enumerate(mutation_vec):
				if m == 1:
					#random mutation
					rand = randint(self.min_value, self.max_value)
					combined_vec.append(rand)
				else:
					#no mutation
					combined_vec.append(individual[i])
			mutated_population.append(combined_vec)

		#now we preserve our best individuals and drop the last x mutated individuals
		num_best = int(self.winner_pool*self.population_size)
		self.population = self.population[:num_best] + mutated_population[:len(mutated_population)-num_best]


	def transpose(self):
		""" Transpose is another mutation function where we mimic actual transposons
		moving a random sequence from one location and inserting it into another location
		
		If a transposon is chosen for this individual, 
		a transposon of the chosen length will be extracted and randomly inserted 

		"""
		if self.mutation_rate == 0:
			return

		mutated_population = []
		
		for i,individual in enumerate(self.population):
			do_transposon = np.random.choice(2, 1, p=[1.0-self.transposon_rate, self.transposon_rate])
			
			combined_vec = individual
			if do_transposon[0] == 1:
				#transposon
				extract_point = randint(0, len(individual))
				insert_point = randint(0, len(individual))
				end_point = extract_point + self.transposon_len
				if end_point >= len(individual):
					end_point = len(individual)
				transposon = individual[extract_point:end_point]
				combined_vec = individual[:extract_point] + individual[end_point:]
				combined_vec = combined_vec[:insert_point] + transposon + combined_vec[insert_point:]
			else:
				#no transposon
				pass
			mutated_population.append(combined_vec)

		#now we preserve our best individuals and drop the last x mutated individuals
		num_best = int(self.winner_pool*self.population_size)
		self.population = self.population[:num_best] + mutated_population[:len(mutated_population)-num_best]

	def breed(self, replace=True):
		""" given the top x percent breed new solutions """
		
		num_breeders = int(self.winner_pool*self.population_size)
		breeders = self.population[:num_breeders]

		num_children = self.population_size - num_breeders
		pairings = np.random.choice(num_breeders, num_children, replace=replace)
		children = []

		for i,pair in enumerate(pairings):
			i1 = int(i%len(breeders))
			i2 = int(pair%len(breeders))
			parent1 = breeders[i1]
			parent2 = breeders[i2]
			child_vector = []
			#create our vector [0,1,0,0..] which chooses which item to take from each individual
			breed_vector = np.random.choice(2, len(breeders[0])) 
			for i,v in enumerate(breed_vector):
				if v == 0:
					child_vector.append(parent1[i])
				else:
					child_vector.append(parent2[i])
			children.append(child_vector)
		#now create our new population
		self.population = self.population[:num_breeders] + children

	def evaluate(self):
		""" 
		evaluate the fitness of each individual
		sort the individuals by fitness (descending order with most fit first)
		if any individual is of max_fitness then return true, else false
		"""
		scored = []
		for individual in self.population:
			fitness = self.fitness_func(individual)
			scored.append((individual,fitness))
		#sort our individuals by fitness (Descending)
		sorted_pop = sorted(scored, reverse=True, key=lambda x: x[1])

		#sort our population in descending fitness
		self.population = [x[0] for x in sorted_pop]
		#return just our fitness scores
		return [x[1] for x in sorted_pop]

	def evolve(self):
		""" main for-loop for genetic algorithm"""
		for i in range(0,self.max_generations):
			pop_fitness = self.evaluate()
			if self.verbose == True:
				print("Generation: ", i, " Top fitness: ", pop_fitness[0])
			if pop_fitness[0] >= self.max_fitness:
				return self.population
			self.breed()
			self.mutate()
			self.transpose()
		#reached max generations without getting a max_fitness
		return self.population

