import random
import pandas as pd
import pulp as plp

ore_base = pd.read_csv('ore.csv').fillna(0)
repro_ore = {ore: 0.874 for ore in ore_base['Ore Type']} # Test repro %, replace later

ores = ore_base['Ore Type']
minerals = ore_base.columns[1:]
get_min_j_from_ore_i_names  = lambda i, j: ore_base[ore_base['Ore Type']==i][j].item()

# Setup Model
opt_model = plp.LpProblem(name="MIP Model")

# Set Decision Variables
ore_qty_vars  = {(i): plp.LpVariable(cat=plp.LpInteger, lowBound=0, upBound=10000000, name="Variable_"+i) for i in ore_base['Ore Type']}

# Set Constraints
constraints = {j : opt_model.addConstraint(
plp.LpConstraint(
             e=plp.lpSum(ore_qty_vars[i] * get_min_j_from_ore_i_names(i,j) * repro_ore[i] for i in ores),
             sense=plp.LpConstraintGE,
             rhs=100000,
             name="Constraint_"+j))
       for j in minerals}

# Set Objective
objective = plp.lpSum(ore_qty_vars[i] for i in ores)

# for minimization
opt_model.sense = plp.LpMinimize
opt_model.setObjective(objective)

# solving with CBC
opt_model.solve()

opt_df = pd.DataFrame.from_dict(ore_qty_vars, orient="index", 
                                columns = ["variable_object"])

# PuLP
opt_df["solution_value"] = opt_df["variable_object"].apply(lambda item: item.varValue)
opt_df.to_csv("./optimization_solution.csv")