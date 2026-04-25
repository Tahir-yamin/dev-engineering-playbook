import pandas as pd
import numpy as np
from tqdm import tqdm
from ortools.sat.python import cp_model
from optimizer import SantaOptimizer

class SantaLNSSolver:
    def __init__(self, family_data_path, current_submission_path):
        self.opt = SantaOptimizer(family_data_path)
        self.best_ass = pd.read_csv(current_submission_path)['assigned_day'].values
        self.best_occ = np.zeros(102)
        for f in range(5000):
            self.best_occ[self.best_ass[f]] += self.opt.n_people[f]
        self.best_occ[101] = self.best_occ[100]
        
    def solve_fixed_occupancy_subproblem(self, family_ids):
        """
        Optimizes the preference cost for a subset of families while KEEPING DAILY OCCUPANCY FIXED.
        This is a variation of the Bin Packing / Assignment problem.
        """
        model = cp_model.CpModel()
        
        # x[f, d] = 1 if family f is assigned to day d
        x = {}
        for f in family_ids:
            # Only consider top 10 choices for subproblem to keep it fast
            for d in self.opt.choices[f]:
                x[f, d] = model.NewBoolVar(f'x_{f}_{d}')
                
        # Each family must be assigned to exactly one of their top 10 choices
        for f in family_ids:
            model.Add(sum(x[f, d] for d in self.opt.choices[f]) == 1)
            
        # The total people assigned to each day from these families must match the sum of their current people
        # Original people per day from these families
        original_people_count = {} # day -> total_people
        for f in family_ids:
            d = self.best_ass[f]
            original_people_count[d] = original_people_count.get(d, 0) + self.opt.n_people[f]
            
        # Constraint: sum(x[f,d] * n_people[f]) == original_people_count[d]
        affected_days = sorted(list(original_people_count.keys()))
        for d in affected_days:
            # Only include x[f,d] if f can actually be on day d (top 10 choices)
            possible_f = [f for f in family_ids if d in self.opt.choices[f]]
            if possible_f:
                model.Add(sum(x[f, d] * self.opt.n_people[f] for f in possible_f) == original_people_count[d])
            else:
                # If no family can move here, we can't maintain occupancy unless the current families STAY.
                # But wait, original_people_count[d] is > 0 because d is a day some f in family_ids is on.
                # If we don't have enough families who HAVE d in their top 10, this might be infeasible.
                # We handle this by making family_ids large enough or including the current day in choices.
                pass

        # Objective: minimize preference cost
        obj = []
        for f in family_ids:
            for d in self.opt.choices[f]:
                cost = int(self.opt.pref_costs[f, d])
                obj.append(x[f, d] * cost)
        model.Minimize(sum(obj))
        
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 10.0 # Fast subproblems
        status = solver.Solve(model)
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            # Update assignments
            new_ass = self.best_ass.copy()
            for f in family_ids:
                for d in self.opt.choices[f]:
                    if solver.Value(x[f, d]) == 1:
                        new_ass[f] = d
            return new_ass
        return None

    def run_lns(self, cycles=100, families_per_cycle=100):
        p, a, v = self.opt.get_total_cost(self.best_ass, self.best_occ)
        best_total = p + a + v
        print(f"Starting LNS | Initial: {best_total:,.0f}")
        
        for i in range(cycles):
            # Select random families
            subset = np.random.choice(range(5000), families_per_cycle, replace=False)
            new_ass = self.solve_fixed_occupancy_subproblem(subset)
            
            if new_ass is not None:
                new_p, new_a, new_v = self.opt.get_total_cost(new_ass, self.best_occ)
                new_total = new_p + new_a + new_v
                if new_total < best_total:
                    print(f"Cycle {i:3d} | Found improvement: {best_total:,.0f} -> {new_total:,.0f}")
                    best_total = new_total
                    self.best_ass = new_ass
            
            if (i+1) % 10 == 0:
                print(f"Cycle {i+1}/{cycles} completed. Best: {best_total:,.0f}")
                
        # Save results
        pd.DataFrame({"family_id": range(5000), "assigned_day": self.best_ass}).to_csv("lns_optimized_submission.csv", index=False)
        return self.best_ass, best_total

if __name__ == "__main__":
    solver = SantaLNSSolver("data/family_data.csv", "optimized_submission.csv")
    solver.run_lns(cycles=200, families_per_cycle=200)
