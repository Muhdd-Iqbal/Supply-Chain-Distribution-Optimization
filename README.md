# Supply Chain Distribution Optimization 🚚📊

A mathematical optimization project using Python and PuLP to simulate and minimize transportation costs and optimize quantity allocation from warehouses to destination cities (multi-warehouse distribution networks).

The project focuses on minimizing transportation costs while considering operational constraints such as warehouse capacities, routing policies, and demand allocation.

---

# 📖 Project Overview

In supply chain operations, distribution decisions are often driven by historical patterns and manual planning. In practice, many managerial decisions also prioritize delivery speed to maintain customer satisfaction.

This project demonstrates how mathematical optimization can improve logistics efficiency and significantly reduce transportation costs through data-driven allocation strategies.

Key objectives:

* Minimize total transportation cost
* Optimize warehouse-to-city allocation
* Compare optimized vs baseline distribution strategies
* Analyze the impact of operational constraints

---

# 🧠 Optimization Approach

The model was built using:

* Python
* PuLP (Linear Programming)
* Pandas
* NumPy
* NetworkX
* Plotly
* Matplotlib
* Faker (synthetic dataset generation)

Optimization techniques:

* Linear Programming (LP)
* Sensitivity Analysis
* Constraint-based optimization

---

# 📊 Features

✅ Multi-warehouse distribution simulation
✅ Transportation cost minimization
✅ Warehouse capacity constraints
✅ Route allocation optimization
✅ Sensitivity analysis scenarios
✅ Geographic visualization
✅ Network graph visualization

---

# 📁 Project Structure

```bash
├── data/
│   ├── customer_master.csv
│   ├── orders.csv
│   ├── shiping_matrix.csv
│   ├── warehouse_master.csv
│   ├── warehouse_supply.csv
│
├── notebooks/
│   ├── visualization.ipynb
│
├── src/
│   ├── data.py
│   ├── main.py
│   ├── sql_utils.py
│   ├── optimization.py
│   ├── sensitivity_cost.py
│   ├── requirements.txt
│ 
├── README.md
```

---

# ⚙️ Business Scenarios Tested

## 1. Baseline Scenario

* Single warehouse distribution
* Equal distribution strategy

## 2. Optimized Scenario

* Multi-warehouse optimized allocation

## 3. Sensitivity Analysis

* Minimum allocation constraints
* Fairness/risk-spreading simulation

---

# 📈 Results

Key findings:

* Up to ~80% reduction in transportation costs using optimized allocation compared to baseline strategies
* Sensitivity analysis showed a ~77% increase in logistics costs when enforcing a minimum allocation constraint of 200 units for every warehouse-to-city route.
* Even with additional constraints, the optimized model still outperformed baseline distribution strategies

---

# 🌍 Visualizations

The project includes:

* Cost comparison tables
<img width="396" height="219" alt="tabel comparisonn cost" src="https://github.com/user-attachments/assets/1393b6d5-603b-47e8-8f2b-8961d9ffe07c" />

* Cost comparison in bar chart
  <img width="1006" height="701" alt="barchat newwww" src="https://github.com/user-attachments/assets/f7f24efc-66b6-40c1-b57c-c3ed2eee1742" />

  
* Warehouse-to-city network graphs
 <img width="1182" height="659" alt="network newww" src="https://github.com/user-attachments/assets/d7d8357d-f169-45a4-9940-509e2faf0cab" />

* Geographic routing maps
<img width="908" height="500" alt="newplot geo" src="https://github.com/user-attachments/assets/1f093cf9-a9a8-4ae5-a57f-4eaa487963bb" />


---

# 🚀 How to Run

## Clone repository

```bash
git clone <your-repository-link>
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run notebook

```bash
jupyter notebook
```

---

# 📌 Notes

* All datasets are simulated/synthetic for demonstration purposes.
* This project is intended for educational and portfolio use.

---

# 👨‍💻 Author

Muhammad Iqbal

LinkedIn: https://www.linkedin.com/in/muhammad-iqbal-878189162/

