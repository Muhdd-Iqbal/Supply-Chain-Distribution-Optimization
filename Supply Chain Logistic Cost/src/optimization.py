import pandas as pd
from pulp import * 

class CostTransportation:
    def __init__(self, data, df_wh):
        self.model_data = data
        self.warehouse_data = df_wh
        
    def optimization(self):
        warehouse =( self.model_data[~self.model_data['warehouse'].str.contains('Demand',na=False)]['warehouse'].unique().tolist() )

        cities= [col for col in self.model_data.columns if col != 'warehouse' and col != 'current_supply_unit']

        cost=(self.model_data.query("warehouse!='Warehouse'").set_index("warehouse"))

        supply = (self.warehouse_data.set_index('warehouse')['current_supply_unit'].to_dict())

        demand = (self.model_data.iloc[-1].drop('warehouse').to_dict())

        model=LpProblem(
            "Transportation_Cost",
            LpMinimize
        )

        x=LpVariable.dicts("qty",(warehouse,cities),lowBound=0,cat='integer')

        #Objective Function
        model += lpSum(cost.loc[w,c] * x[w][c] for w in warehouse for c in cities)

        # supply constraint
        for w in warehouse:
            model += (lpSum(x[w][c] for c in cities) <= supply[w])
        
        #demand constraint
        for c in cities:
            model += (lpSum(x[w][c] for w in warehouse)== demand[c])

        model.solve()
        
        status, minimum_cost = LpStatus[model.status], value(model.objective)
        
        results=[]

        for w in warehouse:
            for c in cities:
                qty=value(
                    x[w][c]
                )
                results.append({
                        "warehouse":w,
                        "city":c,
                        "qty":qty
                    })
        result_df=pd.DataFrame(results)
        
        return status,minimum_cost,result_df

        
    