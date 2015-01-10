from __future__ import division # to fix division

from copy import copy
from dice import roll_die		# to roll dice
from itertools import product	# to iterate through Cartesian product of lists
from merge_dict import *		# to merge dicts in constructing results tables
from padnums import pprint_table# to print simulation output nicely

results = ['raise', 'success', 'positive failure', 'negative failure', 'critical failure']

def sanity_check(guts, mythos=0, modifier=0, wild=True): 
	# Do a single Sanity check, using the formula Guts - Mythos - situation modifier. 
	# define roll result table
	# TODO: this works but is rather clunky! just use for loops instead? 
	result = {r:'success' for r in range(4,8)}
	result = merge_dict(result, {r:'positive failure' for r in range(0,4)})
	result = merge_dict(result, {r:'negative failure' for r in range(-3,0)})
#	print result
	result_max = max(result.keys())
	result_min = min(result.keys())
	
	guts_roll = roll_die(guts, wild)
	mythos_roll = roll_die(mythos, wild)
	roll = guts_roll[0] - mythos_roll[0] - modifier
#	print roll
	try:
		return result[roll]
	except KeyError:
		if roll > result_max:
			return 'raise'
		if roll < result_min:
			return 'critical failure'



def sanity_simulation(guts, mythos, modifier, n):
	result_count = {result:0 for result in results}
	for count in range(n):
		this_result = sanity_check(guts, mythos, modifier)
		result_count[this_result] += 1
	return result_count
	
# def print_simulation_results(sim_results, guts_values, mythos_values, modifier_values):
# 	def _nl():
# 		print('\033[{}C'.format(offset)),
# 
# 	for modifier_value in modifier_values:
# 		offset = 15*len(modifier_values)
# 		print('\033[5;{}H'.format(offset)),
# 		print('  guts  '),
# 		_nl()
# 		print('  ')
# 		for guts_value in guts_values:
# 			print('  ' + str(guts_value) +),
# 		_nl()
# 		for mythos_value in mythos_values:
# 			print(mythos_value),
# 			for guts_value in guts_values: 
#

def print_simulation_results(sim_results, guts_values, mythos_values, modifier_values): 
	for modifier in modifier_values:
		# convert sim_results into list of lists
		row0 = [' ']				# top row: an empty space, then the guts values
		row0.extend(guts_values)					
		results_table = [row0]		# initialize table with top row
		for (guts, mythos) in product(guts_values, mythos_values):
			print('guts: ' + str(guts))
			print('mythos: ' + str(mythos))
			row = [mythos]		# on each row, first value is mythos value
			row.append(sim_results[(guts, mythos, modifier)])
								# then add the simulation results
			print(row)
			results_table.append(row)	# append this to the table
		print(results_table)
		# print using pprint_table
#		pprint_table(results_array)

if __name__ == '__main__':
	guts_values = [6, 8]
	mythos_values = [0, 4, 6]
	modifier_values = [0]
	n = 1000
	fails_count = {}
	for i in product(guts_values, mythos_values, modifier_values):
		sim_results = sanity_simulation(i[0], i[1], i[2], n)
		fails = (sim_results['positive failure'] + sim_results['negative failure'] + 
					sim_results['critical failure']) / n
		fails_count[i] = fails
	print(fails_count)
#	print_simulation_results(fails_count, guts_values, mythos_values, modifier_values)
	