from tas_profile import TasProfile
# from classes.parse_single_col_temp import TasProfile
from typing import List
import numpy as np
import pandas as pd

class Exposure: 
	increment: int 
	duration: int
	increments: int
	temperature_t: pd.DataFrame
	cumexposure_t: pd.DataFrame
	total_exposure: float
	INDEX_COL = 'increment'

	def __init__(self, increment=3600, duration=4698864000):
		self.increment = increment
		self.duration = duration
		self.increments = duration // increment

		self.temperature_t = pd.DataFrame(np.zeros((self.increments, 2)))
		self.temperature_t.columns = ['time_s', 'temperature']
		self.temperature_t.index.name = Exposure.INDEX_COL

		self.exposure_t = pd.DataFrame(np.zeros((self.increments, 2)))
		self.exposure_t.columns = ['time_s', 'exposure']
		self.exposure_t.index.name = Exposure.INDEX_COL

		self.cumexposure_t = pd.DataFrame(np.zeros((self.increments, 2)))
		self.cumexposure_t.columns = ['time_s', 'cumexposure']
		self.cumexposure_t.index.name = Exposure.INDEX_COL
		self.total_exposure = None

	def print_dims(self):
		print(f'Increment Duration (in seconds): {self.increment}')
		print(f'Total Duration (in seconds): {self.duration}')
		print(f'Increments Generated (row count): {self.increments}')


	def generate_increments(self, tasProfile: TasProfile):
		self.temperature_t['time_s'] = np.arange(0, self.duration, self.increment)
		for i, time in zip(range(self.increments), range(0, self.duration, self.increment)):
			self.temperature_t.iat[i,1] = tasProfile.diurnal_estimation(time)

	def generate_cumexposure(self):
		self.exposure_t['time_s'] = self.temperature_t['time_s']
		self.cumexposure_t['time_s'] = self.temperature_t['time_s']
		coeff = (((1.0 / 60.0) / 60.0) / 24.0) / 365.0
		self.exposure_t['exposure'] = self.temperature_t['temperature'] * (coeff * self.increment) 
		self.cumexposure_t['cumexposure'] = self.exposure_t['exposure'].cumsum()
		self.total_exposure = float(self.cumexposure_t.tail(1).iat[0,1])

	def load_csv(self, increxp_fp, cumexp_fp):
		self.exposure_t = pd.read_csv(increxp_fp, index_col=Exposure.INDEX_COL)
		self.cumexposure_t = pd.read_csv(cumexp_fp, index_col=Exposure.INDEX_COL) 
		self.total_exposure = float(self.cumexposure_t.tail(1).iat[0,1])

	def to_csv(self, increxp_fp, cumexp_fp):
		self.exposure_t.to_csv(increxp_fp, index_label=Exposure.INDEX_COL)
		self.cumexposure_t.to_csv(cumexp_fp, index_label=Exposure.INDEX_COL)

if __name__ == '__main__': 
	scenarios = [
		"1950-2099_RCP_4.5_avg.csv",
		"1950-2099_RCP_4.5_min.csv",
		"1950-2099_RCP_4.5_max.csv", 
		"1950-2099_RCP_8.5_avg.csv",
		"1950-2099_RCP_8.5_min.csv",
		"1950-2099_RCP_8.5_max.csv"
		]
	two_col_prefix = "/users/austinmichne/documents/cleanperses/data/temperature/1950-2099_two_col/"
	increxp_prefix = "/users/austinmichne/documents/cleanperses/data/exposure/1950-2099_incr_exp/"
	cumexp_prefix = "/users/austinmichne/documents/cleanperses/data/exposure/1950-2099_cum_exp/"

	for scenario in scenarios:
		profile = TasProfile(two_col_prefix + scenario) 
		exposure = Exposure(increment=3600, duration=4698864000)
		exposure.print_dims()
		exposure.generate_increments(profile)
		exposure.generate_cumexposure()
		exposure.to_csv(increxp_prefix + scenario, cumexp_prefix + scenario) 
	