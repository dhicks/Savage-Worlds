#!/usr/bin/env python

'''
merge_dict.py: Provides merge_dict(x, y).  
This function takes two dicts, x and y, and returns a single merged one.  
'''

__author__  = 'Dan Hicks'
__email__   = 'hicks.daniel.j@gmail.com'
__credits__ = 'http://stackoverflow.com/a/39437'

def merge_dict(x, y):
	'''
	take two dicts, x and y, and return a single dict
	after http://stackoverflow.com/a/39437
	'''
	z = x.copy()
	z.update(y)
	return z