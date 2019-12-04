from typing import T, List, Dict, Tuple
import pandas as pd
from random import random

from exposure import Exposure
from cdf import CumulativeDistFailure
from component import Component

class Subpopulation:
	name: str
	exposure: Exposure
	cdf: CumulativeDistFailure 
	god_factor_depth: int 
	components: List[Component]
	failures: List[Tuple[T,int]]

	def __init__(self, name: str, exposure: Exposure,
			cdf: CumulativeDistFailure, count: int, ids=None,
			 god_factor_depth=25):
		self.name = name
		self.exposure = exposure
		self.cdf = cdf
		self.components = list() 
		for i in range(count):
			self.components.append(Component(i, god_factor_depth)) 

	def get_failures(self): 
		self.failures = list()
		for component in self.components:
			component.calculate_failures(self.exposure, self.cdf)
			self.failures.extend(zip([component.id_]*len(component.failures), component.failures))
		self.failures.sort(key=lambda fail: fail[1]) # sort failures by time in seconds

	def write_failures(self, filepath):
		pd.DataFrame(self.failures).to_csv(filepath, header=['component_id', 'time_seconds'], index=False)
	
if __name__ == "__main__":
	scenarios = [
		"1950-2099_RCP_4.5_avg.csv",
		"1950-2099_RCP_4.5_min.csv",
		"1950-2099_RCP_4.5_max.csv", 
		"1950-2099_RCP_8.5_avg.csv",
		"1950-2099_RCP_8.5_min.csv",
		"1950-2099_RCP_8.5_max.csv"
		]
	cdf_prefix = ['best', 'mid', 'worst']
	cdf_postfix = ['electronics', 'motor', 'pvc', 'iron']
	pop_count = {'electronics': 4, 'motor': 4, 'pvc': 480, 'iron': 190}

	increxp_prefix = "/users/austinmichne/documents/cleanperses/data/exposure/1950-2099_incr_exp/"
	cumexp_prefix = "/users/austinmichne/documents/cleanperses/data/exposure/1950-2099_cum_exp/"
	cdf_path = "/users/austinmichne/documents/cleanperses/data/cdf/"
	failure_path = "/users/austinmichne/documents/cleanperses/data/failure/"

	for scenario in scenarios:
		exposure = Exposure()
		exposure.load_csv(increxp_prefix + scenarios[0], cumexp_prefix + scenarios[0])
		for pre in cdf_prefix:
			for component_type in cdf_postfix: 
				cdf = CumulativeDistFailure(f'{pre}_{component_type}',
											f'{cdf_path}{pre}_case_{component_type}.csv')
				subpop = Subpopulation('example', exposure, cdf, pop_count[component_type])
				subpop.get_failures() 
				# print(subpop.failures)
				# print(len(subpop.failures)) 
				# print([x[0] for x in subpop.failures].count(subpop.failures[0][0]))
				rcp = scenario.split(sep='_', maxsplit=1)[1].rsplit('.',maxsplit=1)[0]
				subpop.write_failures(f'{failure_path}{rcp}_{pre}_case_{component_type}.csv')
