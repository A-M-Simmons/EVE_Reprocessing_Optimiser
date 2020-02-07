import random
import pandas as pd
import pulp as plp

from models import Market_Prices
from models import Reprocessing
from models import Minerals

class Ore_Reprocessing_Solver(Market_Prices, Reprocessing, Minerals):
    def solve(self):
        # Get Mineral Constraints
        mineral_constraints = self.get_mineral_constraints()
        # Get Reprocessing
        repro_values = self.get_reprocessing()
        # Get Market Prices

        # Load Base Ore
        ore_base = pd.read_csv('ore.csv').fillna(0)

        # List of Ores and Minerals
        ores = ore_base['Ore Type']
        minerals = ore_base.columns[2:] # Skip Ore Type and Ore Cat columns

        # Some anonymous functions
        get_min_j_from_ore_i_names  = lambda i, j: ore_base[ore_base['Ore Type']==i][j].item() # Get base mineral j for ore i
        # Get row for 'Ore Type' == i, then get the item from column 'Ore Cat' which is the key for repro_values dict
        get_repro_value_i = lambda i : repro_values[ ore_base[ore_base['Ore Type']==i]['Ore Cat'].item() ] # Get repro_value for ore i

        # Setup Model
        opt_model = plp.LpProblem(name="MIP Model")

        # Set Decision Variables
        ore_qty_vars  = {(i): plp.LpVariable(cat=plp.LpInteger, lowBound=0, name="Variable_"+i) for i in ore_base['Ore Type']}

        # Set Constraints
        constraints = {j : opt_model.addConstraint(
        plp.LpConstraint(
                    e=plp.lpSum(ore_qty_vars[i] * get_min_j_from_ore_i_names(i,j) * get_repro_value_i(i) for i in ores),
                    sense=plp.LpConstraintGE,
                    rhs=mineral_constraints[j],
                    name="Constraint_"+j))
            for j in minerals}

        # Set Objective
        objective = plp.lpSum(ore_qty_vars[i] for i in ores)

        # for minimization
        opt_model.sense = plp.LpMinimize
        opt_model.setObjective(objective)

        # solving with CBC
        opt_model.solve()

        # Get result from solver 
        opt_df = pd.DataFrame.from_dict(ore_qty_vars, orient="index", columns = ["variable_object"])        
        opt_df["Value"] = opt_df["variable_object"].apply(lambda item: item.varValue)
        opt_df = opt_df.drop(columns=['variable_object'], axis=1)
        opt_df.index.name = "Ore Type"
        return opt_df