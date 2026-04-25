import pandas as pd
import numpy as np
from ortools.sat.python import cp_model
from tqdm import tqdm
from optimizer import SantaOptimizer
import sys

class SantaNuclearSolver:
    def __init__(self, family_data_path, initial_submission_path):
        print("Initializing Nuclear Solver (Integrated Accounting MIP)...")
        self.opt = SantaOptimizer(family_data_path)
        self.family_data = self.opt.family_data
        self.n_people = self.opt.n_people
        self.choices = self.opt.choices
        self.pref_costs = self.opt.pref_costs
        self.penalty_matrix = self.opt.penalty_matrix
        
        sa_sub = pd.read_csv(initial_submission_path)
        self.initial_assignment = sa_sub['assigned_day'].values
        
        # Precompute per-day family candidates
        self.day_to_families = {d: [f for f in range(5000) if d in self.choices[f]] for d in range(1, 101)}

    def solve(self, time_limit=300):
        model = cp_model.CpModel()
        
        # 1. Decision Variables: assignments (Top 10 choices)
        x = {}
        for f in range(5000):
            for d in self.choices[f]:
                x[(f, d)] = model.NewBoolVar(f'x_{f}_{d}')
        
        for f in range(5000):
            model.Add(sum(x[(f, d)] for d in self.choices[f]) == 1)
            
        # 2. Occupancy Variables: n[d] in [125, 300]
        n = [model.NewIntVar(125, 300, f'n_{d}') for d in range(101)] 
        # day 0 is unused, but index 1-100 are active.
        # However, accounting depends on n[d] and n[d+1].
        # Competition says n[101] = n[100].
        
        for d in range(1, 101):
            day_f = self.day_to_families[d]
            model.Add(n[d] == sum(x[(f, d)] * int(self.n_people[f]) for f in day_f))
            
        # 3. Accounting Cost Variables: acc_cost[d]
        # We need to map (n[d], n[d+1]) to cost.
        # Since CP-SAT is integer, we scale cost by 100 or 1000 for precision if needed?
        # Actually, the penalty can be high. Let's use scale 100 (2 decimal places).
        
        acc_cost = [model.NewIntVar(0, 100000000, f'acc_{d}') for d in range(1, 101)]
        
        # Precompute table for (ni, nj, cost)
        # Cost is scaled by 100
        penalty_table = []
        for i in range(176):
            for j in range(176):
                cost_scaled = int(round(self.penalty_matrix[i, j] * 100))
                penalty_table.append((i + 125, j + 125, cost_scaled))
                
        for d in range(1, 100):
            model.AddAllowedAssignments([n[d], n[d+1], acc_cost[d]], penalty_table)
            
        # n[101] = n[100] logic
        # For d=100, cost is f(n[100], n[100])
        penalty_table_diag = []
        for i in range(176):
            cost_scaled = int(round(self.penalty_matrix[i, i] * 100))
            penalty_table_diag.append((i + 125, cost_scaled))
        model.AddAllowedAssignments([n[100], acc_cost[100]], penalty_table_diag)

        # 4. Objective: minimize (scaled_pref + scaled_acc)
        # Pref cost is already integer, so scale by 100
        pref_cost_total = sum(x[(f, d)] * int(self.pref_costs[f, d]) for f in range(5000) for d in self.choices[f])
        
        model.Minimize(pref_cost_total * 100 + sum(acc_cost))
        
        # 5. Warm start from best assignment
        for f in range(5000):
            d = self.initial_assignment[f]
            if d in self.choices[f]:
                model.AddHint(x[(f, d)], 1)
        
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit
        solver.parameters.num_search_workers = 8 # Parallel processing
        
        print(f"Starting solve (Limit: {time_limit}s)...")
        status = solver.Solve(model)
        
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print(f"Found Solution! Status: {solver.StatusName(status)}")
            final_ass = np.zeros(5000, dtype=int)
            for f in range(5000):
                for d in self.choices[f]:
                    if solver.Value(x[(f, d)]):
                        final_ass[f] = d
                        break
            
            # Compute real cost
            p = sum(self.pref_costs[f, final_ass[f]] for f in range(5000))
            occ = np.zeros(102)
            for f in range(5000): occ[final_ass[f]] += self.n_people[f]
            occ[101] = occ[100]
            
            acc = 0
            for d in range(1, 101):
                ni, nj = int(occ[d]), int(occ[d+1])
                acc += self.penalty_matrix[ni-125, nj-125]
            
            print(f"Final | Total: {p+acc:,.2f} (Pref: {p:,.0f}, Acc: {acc:,.2f})")
            pd.DataFrame({"family_id": range(5000), "assigned_day": final_ass}).to_csv("nuclear_submission.csv", index=False)
            return final_ass
        else:
            print("No solution found.")
            return None

if __name__ == "__main__":
    solver = SantaNuclearSolver("data/family_data.csv", "lns_optimized_submission.csv")
    solver.solve(time_limit=600) # Give 10 minutes for the master solve
