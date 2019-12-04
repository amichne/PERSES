from typing import T, List, Dict, Tuple
from random import random

from exposure import Exposure
from cdf import CumulativeDistFailure

class Component:
    id_: T
    god_factors: List[float]
    failures: List[int]

    def __init__(self, id_, god_factor_depth):
        self.id_ = id_
        self.failures = list()
        self.generate_god_factors(god_factor_depth)

    def generate_god_factors(self, depth):
        self.god_factors = list()
        for i in range(depth):
            self.god_factors.append(random())

    def calculate_failures(self, exposure: Exposure,
                            cdf: CumulativeDistFailure) -> List[int]:
        '''Calculate the failure occurences. Returns
         a list of the failures with the list values
          representing the time of failure in seconds'''
        gf_count = 0
        exp_used = 0
        exp_avail = exposure.total_exposure

        while exp_avail > 0:
            exp_next_fail = cdf.degC_yr_from_percentile(self.god_factors[gf_count])
            exp_avail -= exp_next_fail
            exp_used += exp_next_fail
            gf_count += 1

            if exp_avail > 0:
                series = exposure.cumexposure_t[exposure.cumexposure_t['cumexposure'] < exp_used]
                if not series.empty:
                    increment = int(series.idxmax().iat[1])
                else:
                    increment = 0
                seconds = int(exposure.cumexposure_t.iat[increment,0]) 
                self.failures.append(seconds) 