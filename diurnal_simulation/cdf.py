from typing import T, List, Dict
import numpy as np
import pandas as pd

class CumulativeDistFailure:
	''' The CDF file exists as a text file where each
		line holds a float, representing the percent
		of the population failed at that (deg C) * Year'''
	INDEX_COL = 'degC_yr_exp'
	name: str
	percentiles: pd.DataFrame 

	def __init__(self, name, filepath):
		self.name = name
		self.percentiles = pd.read_csv(filepath,
		 index_col=CumulativeDistFailure.INDEX_COL)
		# print(self.percentiles)
		# input()

	def degC_yr_from_percentile(self, percentile: float) ->  float:
		# exp_col = list(self.percentiles.columns).index(CumulativeDistFailure.INDEX_COL)
		exp_col = 0
		lower_exp = int(self.percentiles[self.percentiles['percent_failure'] < percentile].idxmax()) 
		upper_exp = lower_exp + 1
		lower_percentile = float(self.percentiles.iat[lower_exp, exp_col])
		upper_percentile = float(self.percentiles.iat[upper_exp, exp_col])

		# Doing linearization to get to float degC_yr exposure
		# Allows interpolation to get closer reprsentation  of failure
		delta = upper_percentile - lower_percentile
		diff = percentile - lower_percentile
		if (delta == 0):
			percent_diff = 0
		else:
			percent_diff = 1.0 / (delta / diff)

		# print(upper_percentile, lower_percentile, delta, diff, percent_diff)
		# input()
		adjusted_exp = lower_exp + percent_diff
		return adjusted_exp 

# if __name__ == '__main__':
# prefix = ['best', 'mid', 'worst']
# postfix = ['electronics', 'motor', 'pvc', 'iron']
# 	mid = '_case_'
# 	path = 'data/cdf/'

# 	for pre in prefix:
# 		for post in postfix:
# 			with open(f'{path}{pre}{mid}{post}.txt', 'r') as handle:
# 				values = [float(x.strip()) for x in handle.readlines()]
# 			df = pd.DataFrame(values)
# 			df.columns = ['percent_failure']
# 			df.to_csv(f'{path}{pre}{mid}{post}.csv', index_label='degC_yr_exp')