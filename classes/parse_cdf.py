
class CumulativeDistFailure:
	''' The CDF file exists as a text file where each
        line holds a float, representing the percent
        of the population failed at that (deg C) * Year'''
	values = None
	component = None
	meta = None

	def __init__(self, filepath, component, meta=""):
		with open(filepath, 'r') as handle:
			self.values = [float(x.strip()) for x in handle.readlines()]
		self.component = component
        self.meta = meta