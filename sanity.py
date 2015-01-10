#!/usr/bin/env python

"""
sanity.py: A module for a homebrew Sanity mechanic for Savage Worlds/Realms of Cthulhu [ROC]

This mechanic uses a compound Guts/Mythos die roll, rather than ROC's Sanity statistic.  
The basic test is Guts - Knowledge (Mythos) - (a situation modifier).  The Guts roll
uses a Wild die (if appropriate), but not the Mythos roll.  Since the overall outcome 
can be negative, there are five possible outcomes:  

* Raise (>=8): Adrenaline surge; all Traits +1 for the Encounter
* Success (4-7): No effect
* Positive failure (0-3): Roll on failure tables (not given here)
* Negative failure (-3--1): Roll on failure tables, -1
* Critical failure (<=-4): Roll on failure tables, -2

The module includes functions to simulate a large number of checks, for game balancing 
purposes.  

Requires dice and merge_dict modules (which should be in this repository), plus Pandas
for the simulations.  

Simulation output:  
(Isolated integers are modifiers; Guts values in columns, Mythos values in rows)

-1
       6      8
0  0.100  0.068
4  0.569  0.465
6  0.644  0.563

0
       6      8
0  0.270  0.191
4  0.699  0.611
6  0.711  0.661

1
       6      8
0  0.439  0.348
4  0.746  0.707
6  0.803  0.726

2
       6      8
0  0.701  0.527
4  0.812  0.758
6  0.818  0.807
"""

from __future__ import division 	# to fix division; must be at very top of file

__author__      = "Dan Hicks"
__email__   = 'hicks.daniel.j@gmail.com'

from dice import roll_die			# to roll dice
from merge_dict import merge_dict	# to combine dicts in building results table

if __name__ == '__main__':			# other modules to import for simulations
	from itertools import product	# to iterate through the Cartesian product of lists
	from pandas import Panel		# to store simulation data
	from random import seed			# to set pseudorandom number generator seed

# define the possible Sanity test results
results = ['raise', 'success', 'positive failure', 'negative failure', 'critical failure']

# construct the roll result table
# TODO: make this construction easier to read, and abstract the lookup in a function
result = {r:'success' for r in range(4,8)}
result = merge_dict(result, {r:'positive failure' for r in range(0,4)})
result = merge_dict(result, {r:'negative failure' for r in range(-3,0)})
# and note upper and lower bounds for determining raises and critical failures
result_max = max(result.keys())
result_min = min(result.keys())

def sanity_check(guts=6, mythos=0, modifier=0, wild=True): 
	'''
	Do a single Sanity check, using the formula Guts - Mythos - situation modifier. 
	Use a Wild die for Guts, but not Mythos.  
	'''
	guts_roll = roll_die(guts, wild)
	mythos_roll = roll_die(mythos, wild=False)
	roll = guts_roll[0] - mythos_roll[0] - modifier
	try:
		return result[roll]
	except KeyError:
		# if roll isn't a valid key in result, probably it was either a raise or 
		# critical failure
		if roll > result_max:
			return 'raise'
		if roll < result_min:
			return 'critical failure'
		else: 
			raise SanityCheckError('bad things!')


# Simulation stuff starts here

def sanity_simulation(guts, mythos, modifier, n, show=False):
	'''
	Run n simulated Sanity checks, using parameters given in arguments
	Returns a dict of counts for each kind of result.  
	show : Show the results of each individual check? 
	'''
	# initialize empty result counter
	result_count = {result:0 for result in results}
	if show:
		print
		print('Simulation: Guts d{}, Mythos d{}, Modifier -{}, n={}'
			.format(guts, mythos, modifier, n))
	for count in range(n):
		this_result = sanity_check(guts, mythos, modifier)
		result_count[this_result] += 1
		if show:
			print(this_result + '; '),
	if show: print # add EOL to the series of individual results
	return result_count

def print_panel(panel, items=None):
	''' 
	Print a Pandas panel at all or the given items
	'''
	if items is None:
		items = panel.items
	for item in items:
		print
		print(item)
		print(panel[item])

if __name__ == '__main__':
	'''
	If this module is loaded directly, run some simulations of the Sanity mechanic.
	'''
	# set a randomization seed
	seed(13527)
	# define die and modifier ranges of interest
	guts_values = [6, 8]
	mythos_values = [0, 4, 6]
	modifier_values = [-1, 0, 1, 2]
	# number of simulations to run
	n = 1000
	# initialize empty pandas Panel with the appropriate axes
	#   note that modifier is the 0th axis of the panel, then mythos, then guts. 
	#   so tables for each modifier will print separately, with guts horizonatal and 
	#   mythos vertical
	fails_count = Panel(
		items=modifier_values, major_axis=mythos_values, minor_axis=guts_values)
	fails_count = fails_count.fillna(0)		# for some reason Pandas seems to default to 1s
# 	print(fails_count)	# this will print a structural summary of the panel
# 	print_panel(fails_count)	# this will print the contents of the panel
		
 	for g, y, o in product(guts_values, mythos_values, modifier_values):
 		sim_results = sanity_simulation(g, y, o, n, show=False)
 		# to make the data human-readable, we'll just count the incidence of 
 		# all kinds of failures
 		fails = (sim_results['positive failure'] + sim_results['negative failure'] + 
 					sim_results['critical failure']) / n
 		fails_count[o][g][y] = fails		# NB indices are: item, minor, major
	print_panel(fails_count)
