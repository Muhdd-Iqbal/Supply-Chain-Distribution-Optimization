import sys
import os
import pandas as pd 

sys.path.append(os.path.abspath(".."))

#from data import DataLoader
from sql_utils import sqlData
from optimization import CostTransportation
from sensitivity_cost import SensitivityCost

#Run if have not exported the csv file
#loader = DataLoader()
#loader.load_data()

loader_sql = sqlData()
cost_and_demand, wh_data = loader_sql.load_sql_data()
df = pd.merge(cost_and_demand,wh_data[['warehouse','current_supply_unit']],how='left', on='warehouse')

def RunModel1():

    loader = CostTransportation(df, wh_data)
    status_cost, minimum_cost, result_df_opt1 = loader.optimization()
    
    return status_cost, minimum_cost, result_df_opt1

def RunModel2():
    
    status_cost, minimum_cost, result_df_opt1 = RunModel1()
    
    min_qty = 200 #Business Requirement

    loader = SensitivityCost(df, wh_data, minimum_cost, min_qty = min_qty)
    status_sensitivity, adjustment_cost, percentage, result_df_opt2 = loader.optimization()
    return min_qty, status_sensitivity, adjustment_cost, percentage, result_df_opt2

if __name__ == "__main__":
    status_cost, minimum_cost, result_df_opt1 = RunModel1()
    min_qty, status_sensitivity, adjustment_cost, percentage, result_df_opt2 = RunModel2()
    
    print(f"Minimum Cost {minimum_cost}")
    print(f"Adding a minimum distribution constraint of {min_qty} units per route increases total transportation cost to {adjustment_cost:,.3f}, an increase of {percentage:.0%}")
    

