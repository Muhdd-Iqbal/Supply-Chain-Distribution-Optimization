import duckdb
import pandas as pd
import os
import sys 
from pathlib import Path

#sys.path.append(os.path.abspath(".."))

class sqlData:    
    def load_sql_data(self):
        
        BASE_DIR = Path(__file__).resolve().parent.parent
        
        orders_df = pd.read_csv(BASE_DIR / "data" / "orders.csv")
        shipping_df = pd.read_csv(BASE_DIR / "data" /  "shipping_matrix.csv")
        supply_df = pd.read_csv(BASE_DIR / "data" / "warehouse_supply.csv")
        warehouse_df = pd.read_csv(BASE_DIR / "data" /  "warehouse_master.csv")
        customer_df = pd.read_csv(BASE_DIR / "data" /  "customer_master.csv")

        shipping_cost_data = duckdb.sql('''
        select * from

        (select warehouse_id warehouse,
                destination_city,
                shipping_cost_rp
                from shipping_df)

                PIVOT (
            MAX(shipping_cost_rp)
            FOR destination_city IN (
            'Jakarta', 'Bekasi', 'Bogor', 'Depok', 'Tangerang', 'Serang', 'Bandung',
            'Cirebon', 'Semarang', 'Solo', 'Yogyakarta', 'Surabaya', 'Malang',
            'Kediri', 'Jember'
            )
        )

        ''').df()

        demand_data_agg = duckdb.sql('''
        select
        'Demand' warehouse,
            *
            from(
        select
            city,
            ROUND(AVG(monthly_demand),0) demand
        from(
        select
            city,
            date_trunc('month', DATE(order_date)) + INTERVAL 1 MONTH - INTERVAL 1 DAY AS month,
            SUM(qty)
            monthly_demand
        from orders_df
        group by 1,2)
        group by city)
        PIVOT(
        MAX(demand)
        FOR city IN
        (
            'Jakarta', 'Bekasi', 'Bogor', 'Depok', 'Tangerang', 'Serang', 'Bandung',
            'Cirebon', 'Semarang', 'Solo', 'Yogyakarta', 'Surabaya', 'Malang',
            'Kediri', 'Jember'
            )
            )
        order by 1
        ''').df()

        cost_and_demand = duckdb.sql('''
        select * from shipping_cost_data
        union all
        select * from demand_data_agg
        ''').df()

        warehouse_data = duckdb.sql('''
        select warehouse_id warehouse,
            capacity_unit,
            current_supply_unit
            from supply_df
        ''').df()

        return cost_and_demand, warehouse_data

