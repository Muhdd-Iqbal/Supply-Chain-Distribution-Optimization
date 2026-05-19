from pulp import * 
import pandas as pd

class SensitivityCost:
    def __init__(self, df, wh_data, min_cost, min_qty):
        self.model_data = df 
        self.warehouse_data = wh_data 
        self.minimum_cost = min_cost
        self.minimum_qty = min_qty
    
    
    def optimization(self):
        
        warehouse =( self.model_data[~self.model_data['warehouse'].str.contains('Demand',na=False)]['warehouse'].unique().tolist() )
        cities= [col for col in self.model_data.columns if col != 'warehouse' and col != 'current_supply_unit']
        cost=(self.model_data.query("warehouse!='Warehouse'").set_index("warehouse"))

        supply = (self.warehouse_data.set_index('warehouse')['current_supply_unit'].to_dict())

        demand = (self.model_data.iloc[-1].drop('warehouse').to_dict())

        list_result = []
        for p in range(1,200,1): #looping percentage
            percent = p/100

            model=LpProblem(
                "Sensitivity_Transportation_Cost",
                LpMinimize
            )

            s=LpVariable.dicts("qty_adjustment",(warehouse,cities),lowBound=0,cat='integer')
            
            model +=  lpSum(cost.loc[w,c] * s[w][c] for w in warehouse for c in cities)

            for w in warehouse:
                model += (lpSum(s[w][c] for c in cities) <= supply[w])

            for c in cities:
                model += (lpSum(s[w][c] for w in warehouse) == demand[c])

            for w in warehouse:
                for c in cities:
                    model += (s[w][c] >= self.minimum_qty)

            model += lpSum(cost.loc[w,c] * s[w][c] for w in warehouse for c in cities) <= (1+percent) * self.minimum_cost
            model.solve(PULP_CBC_CMD(msg=False))

            if model.status == 1:
                list_result.append(percent)
                break
            
        status, adjustment_cost, percentage = LpStatus[model.status], value(model.objective), list_result[0]
        
        results=[]
        
        for w in warehouse:
            for c in cities:
                qty=value(
                    s[w][c]
                )
                results.append({
                        "warehouse":w,
                        "city":c,
                        "qty":qty
                    })
        result_df=pd.DataFrame(results)
        
        return status, adjustment_cost, percentage, result_df


