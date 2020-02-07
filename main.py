

from models import Reprocessing
from solver import Ore_Reprocessing_Solver

r = Ore_Reprocessing_Solver()
r.set_reprocessing(0.874)
r.set_mineral_constraints([2555556, 666667, 194444, 22222, 17222, 1778, 8444, 0])
r.solve()
