import numpy as np
from ortools.linear_solver import pywraplp
from tqdm import tqdm
from optimizer import SantaOptimizer
import sys
import csv

class MIPSearchGLOP:
    def __init__(self, family_data_path, initial_submission_path):
        self.opt = SantaOptimizer(family_data_path)
        self.n_people = self.opt.n_people
        self.choices = self.opt.choices
        self.pref_costs = self.opt.pref_costs
        self.penalty_matrix = self.opt.penalty_matrix

        # load SA base using csv instead of pandas
        self.best_assignment = np.zeros(5000, dtype=int)
        with open(initial_submission_path, 'r') as f:
            reader = csv.reader(f)
            next(reader) # skip header
            for row in reader:
                f_id = int(row[0])
                day = int(row[1])
                self.best_assignment[f_id] = day
                
        self.best_occupancy = np.zeros(102, dtype=np.float64)
        for f in range(5000):
            d = self.best_assignment[f]
            self.best_occupancy[d] += self.n_people[f]
        self.best_occupancy[101] = self.best_occupancy[100]
        self.target_profile = self.best_occupancy[1:101].copy()
        
        p, a, v = self.opt.get_total_cost(self.best_assignment, self.best_occupancy)
        self.current_best_total = p + a + v
        print(f"Loaded SA baseline: {self.current_best_total:,.0f}")
        sys.stdout.flush()
        
        print("Building GLOP model with 500,000 continuous variables...")
        sys.stdout.flush()
        self.solver = pywraplp.Solver.CreateSolver('GLOP')
        self.x = {}
        for f in range(5000):
            for d in range(1, 101):
                self.x[(f, d)] = self.solver.NumVar(0.0, 1.0, f'x_{f}_{d}')

        print("Adding family constraints...")
        sys.stdout.flush()
        for f in range(5000):
            self.solver.Add(self.solver.Sum([self.x[(f, d)] for d in range(1, 101)]) == 1.0)
            
        print("Adding occupancy constraints...")
        sys.stdout.flush()
        self.occ_constraints = []
        for d in range(1, 101):
            c = self.solver.Add(self.solver.Sum([self.x[(f, d)] * self.n_people[f] for f in range(5000)]) >= 125)
            self.occ_constraints.append(c)

        print("Setting objective...")
        sys.stdout.flush()
        self.objective = self.solver.Objective()
        for f in range(5000):
            for d in range(1, 101):
                self.objective.SetCoefficient(self.x[(f, d)], float(self.pref_costs[f, d]))
        self.objective.SetMinimization()
        print("Model built and ready.")
        sys.stdout.flush()

    def _solve_assignment_all_days(self, target_profile, max_deviation=0):
        for d in range(1, 101):
            L = max(125, int(target_profile[d-1]) - max_deviation)
            U = min(300, int(target_profile[d-1]) + max_deviation)
            self.occ_constraints[d-1].SetBounds(L, U)

        status = self.solver.Solve()
        if status != pywraplp.Solver.OPTIMAL and status != pywraplp.Solver.FEASIBLE:
            return None, None

        new_ass = np.zeros(5000, dtype=int)
        occ = np.zeros(102, dtype=np.float64)
        for f in range(5000):
            for d in range(1, 101):
                if self.x[(f, d)].solution_value() > 0.5:
                    new_ass[f] = d
                    occ[d] += self.n_people[f]
                    break
        occ[101] = occ[100]
        return new_ass, occ

    def refine_profiles(self, iterations=20000, T_start=5.0, T_end=0.001):
        current_profile = self.target_profile.copy()
        current_total = self.current_best_total
        best_profile = current_profile.copy()
        best_total = current_total
        best_assignment = self.best_assignment.copy()

        cooling_rate = (T_end / T_start) ** (1.0 / iterations)
        T = T_start

        for i in tqdm(range(iterations), desc="Profile SA"):
            d1, d2 = np.random.choice(np.arange(1, 101), 2, replace=False)
            if current_profile[d1-1] - 4 < 125 or current_profile[d2-1] + 4 > 300:
                continue
            shift = np.random.randint(1, 5)
            new_profile = current_profile.copy()
            new_profile[d1-1] -= shift
            new_profile[d2-1] += shift

            ass, occ = self._solve_assignment_all_days(new_profile, max_deviation=0)
            if ass is None:
                continue
            
            p, a, v = self.opt.get_total_cost(ass, occ)
            new_total = p + a

            delta = new_total - current_total
            if delta < 0 or np.random.rand() < np.exp(-delta / T):
                current_profile = new_profile
                current_total = new_total
                if new_total < best_total:
                    best_total = new_total
                    best_profile = new_profile.copy()
                    best_assignment = ass.copy()
                    tqdm.write(f"Iter {i}  T:{T:.3f}  Best:{best_total:,.0f}")
                    sys.stdout.flush()

            T *= cooling_rate

        ass_final, occ_final = self._solve_assignment_all_days(best_profile, max_deviation=1)
        if ass_final is not None:
            p, a, v = self.opt.get_total_cost(ass_final, occ_final)
            final_total = p + a
            if final_total < best_total:
                best_total = final_total
                best_assignment = ass_final

        return best_assignment, best_total

if __name__ == "__main__":
    mip = MIPSearchGLOP("data/family_data.csv", "lns_optimized_submission.csv")
    best_ass, best_total = mip.refine_profiles(iterations=20000)
    print(f"\n🏆 Final optimal cost: {best_total:,.0f}")
    
    with open("final_optimal_glop.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["family_id", "assigned_day"])
        for i, d in enumerate(best_ass):
            writer.writerow([i, d])
            
    print("Saved final_optimal_glop.csv")
