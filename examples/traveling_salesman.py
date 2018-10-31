"""

Attempts to solve the traveling salesman problem using genetic algorithms

"""

import sys
sys.path.append("..") # Adds higher directory to python modules path.
from transposon import Transposon
import geopy.distance

cities = {
	"Fargo, ND": [46.877186, -96.789803],
	"Odessa, TX": [31.845682,-102.367645],
	"Orangeburg, SC": [33.493317, -80.855415],
	"McAllen, TX": [26.203407,-98.230011],
	"Springfield, OH": [39.925751,-83.806694],
	"Pasadena, TX": [29.691063,-95.209099],
	"Lake Worth, FL":[26.616756,-80.068451],
	"Novi, MI": [42.480591,-83.475494],
	"Rochester, MN": [44.016369,-92.475395],
	"London, KY": [37.129986,-84.084122],
	"Santa Clarita, CA": [34.391663,-118.542587],
	"Overland Park, KS": [38.984764,-94.677658],
	"St Cloud, MN": [45.560230,-94.172852],
	"Santee, CA": [32.838383,-116.973915],
	"Bay Point, CA": [38.033878,-121.960709],
	"Longmont, CO": [40.167206,-105.101929],
	"Issaquah, WA": [47.530102,-122.032616],
	"Akron, OH": [41.081757,-81.511452],
	"Hammond, IN": [41.584660,-87.500160],
	"Youngstown, OH": [41.102970,-80.647247],
	"Hugo, MN": [45.159966,-92.993340],
	"Yorba Linda, CA": [33.888504,-117.813255],
	"Smiths Station, AL": [32.540138,-85.098549],
	"Rapid City, SD": [44.080544,-103.231018],
	"Hillsboro, OR": [45.522896,-122.989830],
	"Elkhart, IN": [41.681992,-85.976669],
	"Providence, RI": [41.825226,-71.418884],
	"Rancho Cucamonga, CA": [34.110489,-117.594429],
	"Orange, CA": [33.787914,-117.853104],
	"Madison, WI": [43.073051,-89.401230],
	"Jersey City, NJ": [40.728157,-74.077644],
	"Bradenton, FL": [27.498928,-82.574821],
	"South Burlington, VT": [44.466995,-73.170959],
	"Long Beach, CA": [33.770050,-118.193741],
	"Greenville, NC": [35.612659,-77.366356],
	"Edison, NJ": [40.522964,-74.411674],
	"Yakima, WA": [46.602070,-120.505898],
	"Dunedin, FL": [28.018349,-82.764473],
	"St Paul, MN": [44.949642,-93.093124],
	"Kent, WA": [47.380932,-122.234840]
}

#here we manually set our max fitness, since our actual desired fitness is unknown
#ie: we don't know the shortest path ahead of time
MAX_FITNESS = 9999999
CITYLIST = []

def main():
	#turn each city into an ordered list
	for i,city in enumerate(cities):
		CITYLIST.append(city)

	max_value = len(cities)-1
	#instantiate our transposon class
	transposon = Transposon(
		vector_len=len(cities),
		fitness_func=fitness_func,
		min_value=0,
		max_value=max_value,
		population_size=1000,
		max_fitness=MAX_FITNESS,
		max_generations=100,
		mutation_rate=0.13,
		verbose=True)
	results = transposon.evolve()
	#given the best result, print the path
	print("Optimal path:")
	best_vector = convert_vector(results[0])
	for city in best_vector:
		print(city)
	#now print the total distance
	print("Total Distance:", MAX_FITNESS - fitness_func(results[0]), " km")


def convert_vector(vector):
	""" converts a vector of integers (which can have duplicates)
	to a single list of cities (no duplicates)
	replaces duplicates in a repeatable manner (same vector will yield the same result each time)
	"""
	city_list = CITYLIST.copy()
	city_vector = []
	for idx in vector:
		abs_idx = idx % len(city_list)
		city = city_list[abs_idx]
		city_vector.append(city)
		city_list.pop(abs_idx)
	return city_vector

def fitness_func(vector):
	""" 
	in this simulation our max_fitness is unknown
	so we create a ceiling amount and will subtract the total distance from this amount
	fitness = MAX_FITNESS - distance
	This means we will never quit until the simulation has run through maxium amount of trials
	however, we don't know the minimum distance ahead of time so we cannot verify we have hit the global optimum
	"""
	total_distance = 0
	city_vector = convert_vector(vector)
	for i,city in enumerate(city_vector):
		if i == len(city_vector) - 1:
			#final case, calculate distance from last city to first
			city1 = cities[city]
			city2 = cities[city_vector[0]]
			total_distance += calculate_distance(city1, city2)
		else:
			city1 = cities[city]
			city2 = cities[city_vector[i+1]]
			total_distance += calculate_distance(city1, city2)
	return MAX_FITNESS - total_distance

def calculate_distance(coords_1, coords_2):
	""" given two coordinates (lattitude and longitude)
	calculates the distance in kilometers """
	return geopy.distance.vincenty(coords_1, coords_2).km


if __name__ == "__main__":
	main()
