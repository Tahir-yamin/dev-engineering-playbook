import pandas as pd
import numpy as np
from ortools.sat.python import cp_model
from tqdm import tqdm
from optimizer import SantaOptimizer
import sys

class SantaGoldSolver:
    def __init__(self, family_data_path, initial_submission_path):
        print("Initializing Solver...")
        self.opt = SantaOptimizer(family_data_path)
        self.family_data = self.opt.family_data
        self.n_people = self.opt.n_people
        self.choices = self.opt.choices
        self.pref_costs = self.opt.pref_costs
        
        sa_sub = pd.read_csv(initial_submission_path)
        self.best_assignment = sa_sub['assigned_day'].values
        self.best_occupancy = np.zeros(102)
        for f in range(5000):
            self.best_occupancy[self.best_assignment[f]] += self.opt.n_people[f]
        self.best_occupancy[101] = self.best_occupancy[100]
        
        p, a, v = self.opt.get_total_cost(self.best_assignment, self.best_occupancy)
        self.best_total = p + a + v
        self.best_profile = self.best_occupancy[1:101].copy()
        
        # Precompute per-day family candidates for speed
        self.day_to_families = {d: [f for f in range(5000) if d in self.choices[f]] for d in range(1, 101)}
        
        print(f"Initial Score: {self.best_total:,.2f}")

    def solve_assignment(self, profile, slack=0, time_limit=3):
        model = cp_model.CpModel()
        assign = {}
        for f in range(5000):
            for d in self.choices[f]:
                assign[(f, d)] = model.NewBoolVar(f'x_{f}_{d}')
        
        for f in range(5000):
            model.Add(sum(assign[(f, d)] for d in self.choices[f]) == 1)
            
        for d in range(1, 101):
            lb = int(max(125, profile[d-1] - slack))
            ub = int(min(300, profile[d-1] + slack))
            
            day_families = self.day_to_families[d]
            if not day_families and lb > 0: return None, None
            
            model.AddLinearConstraint(
                sum(assign[(f, d)] * int(self.n_people[f]) for f in day_families), 
                lb, ub
            )
            
        obj_vars = []
        for f in range(5000):
            for d in self.choices[f]:
                obj_vars.append(assign[(f, d)] * int(self.pref_costs[f, d]))
        model.Minimize(sum(obj_vars))
        
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit
        # Warm start
        for f in range(5000):
            d = self.best_assignment[f]
            if d in self.choices[f]:
                model.AddHint(assign[(f, d)], 1)
                
        status = solver.Solve(model)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            new_ass = self.best_assignment.copy()
            new_occ = np.zeros(102)
            for f in range(5000):
                for d in self.choices[f]:
                    if solver.Value(assign[(f, d)]):
                        new_ass[f] = d
                        new_occ[d] += self.n_people[f]
                        break
            new_occ[101] = new_occ[100]
            return new_ass, new_occ
        return None, None

    def run_search(self, iterations=500):
        print(f"Running profile-search for {iterations} iterations...")
        sys.stdout.flush()
        
        for i in range(iterations):
            d1, d2 = np.random.randint(1, 101, 2)
            if d1 == d2: continue
            
            shift = np.random.randint(1, 4)
            new_profile = self.best_profile.copy()
            if new_profile[d1-1] - shift < 125 or new_profile[d2-1] + shift > 300:
                continue
            
            new_profile[d1-1] -= shift
            new_profile[d2-1] += shift
            
            ass, occ = self.solve_assignment(new_profile, slack=0)
            if ass is not None:
                p, a, v = self.opt.get_total_cost(ass, occ)
                new_total = p + a + v
                if new_total < self.best_total:
                    print(f"Iter {i:3d}: Score improved! {self.best_total:,.2f} -> {new_total:,.2f}")
                    self.best_total = new_total
                    self.best_assignment = ass
                    self.best_profile = new_profile
                    sys.stdout.flush()
            
            if (i+1) % 10 == 0:
                print(f"Iter {i+1}: Current best {self.best_total:,.2f}")
                sys.stdout.flush()

        pd.DataFrame({"family_id": range(5000), "assigned_day": self.best_assignment}).to_csv("gold_optimized_submission.csv", index=False)
        return self.best_assignment, self.best_total

if __name__ == "__main__":
    solver = SantaGoldSolver("data/family_data.csv", "lns_optimized_submission.csv")
    solver.run_search(iterations=500)
