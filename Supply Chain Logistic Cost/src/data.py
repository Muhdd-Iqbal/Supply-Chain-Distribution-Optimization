import pandas as pd
import random
from faker import Faker
from geopy.distance import geodesic
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(".."))


class DataLoader:
    def __init__(self, N_ORDER=50000, N_CUSTOMER=30000):
        self.N_ORDER = N_ORDER
        self.N_CUSTOMER = N_CUSTOMER

    def load_data(self):
        fake = Faker('id_ID')


    # CITY MASTER DATA(15 City in the Java)
    # =====================================================

        cities = {
            "Jakarta": {"lat": -6.2088, "lon": 106.8456, "weight": 18},
            "Bekasi": {"lat": -6.2383, "lon": 106.9756, "weight": 8},
            "Bogor": {"lat": -6.5950, "lon": 106.8166, "weight": 7},
            "Depok": {"lat": -6.4025, "lon": 106.7942, "weight": 7},
            "Tangerang": {"lat": -6.1783, "lon": 106.6319, "weight": 7},
            "Bandung": {"lat": -6.9175, "lon": 107.6191, "weight": 18},
            "Cirebon": {"lat": -6.7320, "lon": 108.5523, "weight": 6},
            "Semarang": {"lat": -6.9666, "lon": 110.4166, "weight": 14},
            "Solo": {"lat": -7.5755, "lon": 110.8243, "weight": 10},
            "Yogyakarta": {"lat": -7.7956, "lon": 110.3695, "weight": 12},
            "Surabaya": {"lat": -7.2575, "lon": 112.7521, "weight": 18},
            "Malang": {"lat": -7.9666, "lon": 112.6326, "weight": 10},
            "Kediri": {"lat": -7.8480, "lon": 112.0178, "weight": 5},
            "Jember": {"lat": -8.1724, "lon": 113.7005, "weight": 5},
            "Serang": {"lat": -6.1200, "lon": 106.1503, "weight": 5}
        }

        # PRODUCT MASTER
        # =====================================================

        products = {
            "SKU-A": {
                "category": "Powder",
                "price": 25000,
                "weight_kg": 0.5
            },
            "SKU-B": {
                "category": "Beverage",
                "price": 55000,
                "weight_kg": 1.2
            },
            "SKU-C": {
                "category": "Snack",
                "price": 15000,
                "weight_kg": 0.2
            },
            "SKU-D": {
                "category": "PersonalCare",
                "price": 85000,
                "weight_kg": 1.5
            }
        }

        # WAREHOUSE MASTER
        # =====================================================

        warehouse = {
            "WH-A": {
                "city": "Jakarta",
                "lat": -6.2000,
                "lon": 106.8166
            },
            "WH-B": {
                "city": "Semarang",
                "lat": -6.9666,
                "lon": 110.4166
            },
            "WH-C": {
                "city": "Surabaya",
                "lat": -7.2575,
                "lon": 112.7521
            }
        }

        # CUSTOMER MASTER
        # =====================================================

        customers = []

        for i in range(self.N_CUSTOMER):
            city = random.choices(
                list(cities.keys()),
                weights=[x["weight"] for x in cities.values()]
            )[0]

            center_lat = cities[city]["lat"]
            center_lon = cities[city]["lon"]

            # random coordinate around city center
            lat = center_lat + random.uniform(-0.05, 0.05)
            lon = center_lon + random.uniform(-0.05, 0.05)

            customers.append({
                "customer_id": f"CUST{i:05}",
                "city": city,
                "address": fake.street_address(),
                "latitude": round(lat, 6),
                "longitude": round(lon, 6)
            })

        customer_df = pd.DataFrame(customers)

        # SALES / ORDERS (Last 6 Month)
        # =====================================================

        rows = []

        start = datetime(2025, 11, 1)
        end = datetime(2026, 4, 30)

        days = (end - start).days

        for i in range(self.N_ORDER):
            customer = customer_df.sample(1).iloc[0]
            sku = random.choice(list(products.keys()))
            p = products[sku]
            order_date = start + timedelta(
                days=random.randint(0, days)
            )

            month = order_date.month

            # seasonality
            base_qty = random.randint(5, 25)
            if month in [3, 4]:
                multiplier = random.uniform(1.3, 1.8)
            elif month == 12:
                multiplier = random.uniform(1.1, 1.4)
            else:
                multiplier = random.uniform(0.9, 1.1)

            qty = max(1, int(base_qty * multiplier))
            sales = qty * p["price"]
            total_weight = qty * p["weight_kg"]

            rows.append({
                "order_id": f"ORD{i:06}",
                "order_date": order_date,
                "customer_id": customer["customer_id"],
                "city": customer["city"],
                "address": customer["address"],
                "customer_latitude": customer["latitude"],
                "customer_longitude": customer["longitude"],
                "sku": sku,
                "category": p["category"],
                "qty": qty,
                "unit_price_rp": p["price"],
                "sales_rp": sales,
                "weight_kg": round(total_weight, 2)
            })

        orders_df = pd.DataFrame(rows)

        # SHIPPING MATRIX
        # =====================================================

        shipping_rows = []
        for wh_id, wh in warehouse.items():
            for city_name, city in cities.items():
                distance = geodesic(
                    (wh["lat"], wh["lon"]),
                    (city["lat"], city["lon"])
                ).km

                # realistic transport cost
                fixed_cost = 5000
                cost_per_km = 650

                shipping_cost = (
                    fixed_cost +
                    (distance * cost_per_km)
                )

                shipping_rows.append({
                    "warehouse_id": wh_id,
                    "warehouse_city": wh["city"],
                    "warehouse_latitude": wh["lat"],
                    "warehouse_longitude": wh["lon"],
                    "destination_city": city_name,
                    "destination_latitude": city["lat"],
                    "destination_longitude": city["lon"],
                    "distance_km": round(distance, 2),
                    "fixed_cost_rp": fixed_cost,
                    "cost_per_km_rp": cost_per_km,
                    "shipping_cost_rp": round(shipping_cost)
                })

        shipping_df = pd.DataFrame(shipping_rows)

        # WAREHOUSE SUPPLY
        # =====================================================

        supply_df = pd.DataFrame({
            "warehouse_id": ["WH-A", "WH-B", "WH-C"],
            "warehouse_city": ["Jakarta", "Semarang", "Surabaya"],
            "capacity_unit": [250000, 180000, 150000],
            "current_supply_unit": [210000, 145000, 120000]
        })

        # WAREHOUSE MASTER
        # =====================================================

        warehouse_df = pd.DataFrame([
            {
                "warehouse_id": wh_id,
                "warehouse_city": wh["city"],
                "latitude": wh["lat"],
                "longitude": wh["lon"]
            }
            for wh_id, wh in warehouse.items()
        ])
        
        

        # EXPORT CSV
        # =====================================================

        orders_df.to_csv("data/orders.csv", index=False)
        shipping_df.to_csv("data/shipping_matrix.csv", index=False)
        supply_df.to_csv("data/warehouse_supply.csv", index=False)
        warehouse_df.to_csv("data/warehouse_master.csv", index=False)
        customer_df.to_csv("data/customer_master.csv", index=False)
        print("DONE GENERATING DATA")