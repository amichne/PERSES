from random import random
from csv import writer
from math import ceil, sin, pi
from typing import List, Tuple

class TasProfile:
	def __init__(self, filepath, filepath_two=None):
		# H_m: Hour where min temp occurs
		# H_x: Hour where max temp occurs
		self.H_m = 6.0
		self.H_x = 15.0
		self.max_values = list()
		self.min_values = list()

		if filepath_two == None:
			lines = open(filepath, 'r').readlines()
			for line in lines:
				min_, max_ = line.split(',')
				self.min_values.append(float(min_))
				self.max_values.append(float(max_))
		else:
			min_lines = open(filepath, 'r', encoding="utf-8-sig").readlines()
			self.min_values = self.parse_temps(min_lines)
			max_lines = open(filepath_two, 'r', encoding="utf-8-sig").readlines()
			self.max_values = self.parse_temps(max_lines)

	def __eq__(self, value):
		if not isinstance(value, TasProfile):
			return False
		if (self.max_values != value.max_values) or (self.min_values != value.min_values):
			return False 
		return True

	def parse_temps(self, lines):
		values = list()
		for line in lines:
			try:
				values.append(float(line.split(',')[1]))
			except Exception:
				values.append(float(line))
		return values

	def diurnal_estimation(self, time_seconds):
		# t: time of day in hours, 0 <= t < 24
		# T_m: Daily minimum temp
		# T_x: Daily maximum temp
		# T_t: Temperature at hour t
		t = int(time_seconds / 3600) % 24
		T_m = self.min_values[int(time_seconds / 86400)]
		T_x = self.max_values[int(time_seconds / 86400)]
		sin_comp = sin(
			(pi * (
					(t - self.H_m) / (self.H_x - self.H_m))
			 ) - (pi / 2))
		T_t = T_m + ((T_x - T_m) / 2) * (1 + sin_comp)
		return T_t


			

if __name__ == "__main__":
	def write_two_col(tasProfile: TasProfile, filepath: str):
		with open(filepath, 'w+') as csv_handle:
			csv_writer = writer(csv_handle)
			for n in range(len(tasProfile.max_values)):
				if (tasProfile.min_values[n] > tasProfile.max_values[n]):
					raise Exception(f'Error at line {n}')
				csv_writer.writerow([tasProfile.min_values[n], tasProfile.max_values[n]])
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
		write_two_col(single_col_profile, two_col_prefix + scenario)

	for scenario in scenarios:
		two_col_profiles[scenario] = TasProfile(two_col_prefix + scenario)

	for scenario in scenarios:
		if (two_col_profiles[scenario] != single_col_profiles[scenario]):
			raise Exception(f'Error convertering the scenario {scenario} from one to two columns')


