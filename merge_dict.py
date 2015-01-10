def merge_dict(x, y):
	# take two dicts, x and y, and return a single dict
	# after http://stackoverflow.com/a/39437
	z = x.copy()
	z.update(y)
	return z