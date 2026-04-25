import pandas as pd
import numpy as np
from ortools.linear_solver import pywraplp
from tqdm import tqdm
from optimizer import SantaOptimizer
import sys

class MIPSearch:
    def __init__(self, family_data_path, initial_submission_path):
        self.opt = SantaOptimizer(family_data_path)
        self.family_data = self.opt.family_data
        self.n_people = self.opt.n_people
        self.choices = self.opt.choices
        self.pref_costs = self.opt.pref_costs
        self.penalty_matrix = self.opt.penalty_matrix

        sa_sub = pd.read_csv(initial_submission_path)
        self.best_assignment = sa_sub['assigned_day'].values
        self.best_occupancy = np.zeros(102, dtype=np.float64)
        for f in range(5000):
            d = self.best_assignment[f]
            self.best_occupancy[d] += self.n_people[f]
        self.best_occupancy[101] = self.best_occupancy[100]
        self.target_profile = self.best_occupancy[1:101].copy()
        
        p, a, v = self.opt.get_total_cost(self.best_assignment, self.best_occupancy)
        self.current_best_total = p + a + v
        print(f"Loaded Baseline: {self.current_best_total:,.0f}")
        
        # Build optimized solver once
        self.solver = pywraplp.Solver.CreateSolver('GLOP')
        self.x = {}
        for f in range(5000):
            # We use Top 10 + current + a few neighbors to keep GLOP fast but flexible
            valid_days = set(self.choices[f])
            valid_days.add(self.best_assignment[f])
            # Add neighbors for more flexibility
            for d in list(valid_days):
                if d > 1: valid_days.add(d-1)
                if d < 100: valid_days.add(d+1)
            
            for d in valid_days:
                self.x[(f,d)] = self.solver.NumVar(0.0, 1.0, f'x_{f}_{d}')
        
        for f in range(5000):
            f_days = [d for d in range(1, 101) if (f,d) in self.x]
            self.solver.Add(self.solver.Sum([self.x[(f, d)] for d in f_days]) == 1.0)
            
        self.occ_constraints = []
        for d in range(1, 101):
            day_f = [f for f in range(5000) if (f,d) in self.x]
            c = self.solver.Add(self.solver.Sum([self.x[(f, d)] * self.n_people[f] for f in day_f]) >= 125)
            self.occ_constraints.append(c)

        self.objective = self.solver.Objective()
        for (f,d), var in self.x.items():
            self.objective.SetCoefficient(var, float(self.pref_costs[f, d]))
        self.objective.SetMinimization()

    def _solve_assignment(self, profile, slack=1):
        for d in range(1, 101):
            val = profile[d-1]
            self.occ_constraints[d-1].SetBounds(val - slack, val + slack)
            
        status = self.solver.Solve()
        if status in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
            new_ass = np.zeros(5000, dtype=int)
            occ = np.zeros(102, dtype=np.float64)
            for f in range(5000):
                found = False
                # Sort days in x[(f,d)] by solution value
                f_days = [d for d in range(1, 101) if (f,d) in self.x]
                best_d = -1; best_v = -1
                for d in f_days:
                    v = self.x[(f, d)].solution_value()
                    if v > best_v:
                        best_v = v; best_d = d
                new_ass[f] = best_d
                occ[best_d] += self.n_people[f]
            occ[101] = occ[100]
            return new_ass, occ
        return None, None

    def refine(self, iterations=20000, T_start=50.0, T_end=0.1):
        # Higher T_start to escape plateau
        current_profile = self.target_profile.copy()
        current_total = self.current_best_total
        best_profile = current_profile.copy()
        best_assignment = self.best_assignment.copy()
        best_total = current_total

        cooling = (T_end / T_start) ** (1.0 / iterations)
        T = T_start

        print(f"Starting SA Search (T_start={T_start})...")
        for i in tqdm(range(iterations), desc="MIP SA"):
            d1, d2 = np.random.randint(1, 101, 2)
            if d1 == d2: continue
            
            # More aggressive shifts
            shift = np.random.randint(1, 6)
            if current_profile[d1-1] - shift < 125 or current_profile[d2-1] + shift > 300:
                continue
                
            new_profile = current_profile.copy()
            new_profile[d1-1] -= shift
            new_profile[d2-1] += shift

            ass, occ = self._solve_assignment(new_profile, slack=1)
            if ass is None: continue
            
            p, a, v = self.opt.get_total_cost(ass, occ)
            new_total = p + a + v
            
            delta = new_total - current_total
            if delta < 0 or np.random.rand() < np.exp(-delta / T):
                current_profile = new_profile
                current_total = new_total
                if new_total < best_total:
                    best_total = new_total
                    best_profile = new_profile.copy()
                    best_assignment = ass.copy()
                    tqdm.write(f"Iter {i:5d}: New Best {best_total:,.0f} | T: {T:.2f}")
                    sys.stdout.flush()
            T *= cooling

        pd.DataFrame({"family_id": range(5000), "assigned_day": best_assignment}).to_csv("final_optimal_submission.csv", index=False)
        return best_assignment, best_total

if __name__ == "__main__":
    # Start from the best LNS result
    mip = MIPSearch("data/family_data.csv", "lns_optimized_submission.csv")
    mip.refine(iterations=10000, T_start=50.0)
