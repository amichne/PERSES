import numpy as np
import pandas as pd
from csv import writer, reader
from math import ceil, sin, pi
from typing import List, Tuple

class TasProfile:
	H_m: float
	H_x: float
	values: pd.DataFrame
	max_values: pd.Series
	min_values: pd.Series
	INDEX_COL = 'day_n'

	def __init__(self, filepath, filepath_two=None):
		# H_m: Hour where min temp occurs
		# H_x: Hour where max temp occurs
		self.H_m = 6.0
		self.H_x = 15.0

		if filepath_two == None:
			self.values = pd.read_csv(filepath, index_col=TasProfile.INDEX_COL)
			self.values.replace('', np.nan, inplace=True)
			self.values.dropna(inplace=True)
			self.min_values = self.values['T_min']
			self.max_values = self.values['T_max']

		else:
			min_lines = open(filepath, 'r', encoding="utf-8-sig").readlines()
			self.min_values = pd.Series([float(line) for line in min_lines])
			max_lines = open(filepath_two, 'r', encoding="utf-8-sig").readlines()
			self.max_values = pd.Series([float(line) for line in max_lines])
			self.values = pd.DataFrame({'T_min':self.min_values, 'T_max':self.max_values})
		self.values.index.name = TasProfile.INDEX_COL

	def __eq__(self, value) -> bool:
		if not isinstance(value, TasProfile):
			return False
		# TODO: Find a better way to do this comparison
		if not (self.max_values.equals(value.max_values) and self.min_values.equals(value.min_values)): 
			print(f'Two Col min dims: {self.min_values.shape} \t One Col min dims: {value.min_values.shape}')
			print(self.min_values.head())
			print(value.min_values.head())
			print(f'Two Col max dims: {self.max_values.shape} \t One Col dims: {value.max_values.shape}')
			print(self.max_values.head())
			print(value.max_values.head()) 
			return False 
		return True 

	def diurnal_estimation(self, time_seconds, debug=False) -> float:
		# t: time of day in hours, 0 <= t < 24
		# T_m: Daily minimum temp
		# T_x: Daily maximum temp
		# T_t: Temperature at hour t
		t = float(int(time_seconds / 3600) % 24)
		T_m = self.min_values.iat[int(time_seconds / 86400)]
		T_x = self.max_values.iat[int(time_seconds / 86400)]
		sin_comp = sin(
			(pi * (
					(t - self.H_m) / (self.H_x - self.H_m))
			 ) - (pi / 2.0))
		T_t = T_m + float(float(float(T_x - T_m) / 2.0) * (1.0 + sin_comp))
		if debug:
			print(f'Temp min: {T_m} \t Temp max: {T_x} \t Temp predicted at hour {t}: {T_t}')
		return T_t 
			
	def to_csv(self, filepath: str):
		self.values.to_csv(filepath, index_label=TasProfile.INDEX_COL) 

if __name__ == "__main__": 
	scenarios = [
		"1950-2099_RCP_4.5_avg.csv",
		"1950-2099_RCP_4.5_min.csv",
		"1950-2099_RCP_4.5_max.csv", 
		"1950-2099_RCP_8.5_avg.csv",
		"1950-2099_RCP_8.5_min.csv",
		"1950-2099_RCP_8.5_max.csv"
		] 
	min_prefix = "/Users/austinmichne/Documents/CleanPerses/data/temperature/1950-2099_min_daily/"
	max_prefix = "/users/austinmichne/documents/cleanperses/data/temperature/1950-2099_max_daily/"
	two_col_prefix = "/users/austinmichne/documents/cleanperses/data/temperature/1950-2099_two_col/"
	single_col_profiles = dict()
	two_col_profiles = dict()

	for scenario in scenarios: 
		single_col_profile = TasProfile(min_prefix + scenario, max_prefix + scenario) 
		single_col_profiles[scenario] = single_col_profile
		single_col_profile.to_csv(two_col_prefix + scenario)

	for scenario in scenarios:
		two_col_profiles[scenario] = TasProfile(two_col_prefix + scenario)

	# This is a validation measure that is currently not working correctly
	# for scenario in scenarios:
	# 	if (two_col_profiles[scenario] != single_col_profiles[scenario]):
	# 		raise Exception(f'Error convertering the scenario {scenario} from one to two columns') 
	
	profile = two_col_profiles[scenarios[0]]
	