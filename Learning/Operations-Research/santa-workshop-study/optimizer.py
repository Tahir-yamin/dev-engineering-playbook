import numpy as np
from tqdm import tqdm
import csv

class SantaOptimizer:
    def __init__(self, family_data_path):
        with open(family_data_path, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            families = []
            for row in reader:
                families.append([int(x) for x in row])
        families = np.array(families)
        # First column is family_id (which is 0 to 4999), 
        # choices are columns 1-10, n_people is column 11
        self.choices = families[:, 1:11]
        self.n_people = families[:, 11]

        # ---------- precompute preference costs ----------
        self.pref_costs = np.full((5000, 101), 500 + 36 * self.n_people[:, None] + 398 * self.n_people[:, None])
        for f in range(5000):
            n = self.n_people[f]
            self.pref_costs[f, self.choices[f, 0]] = 0
            self.pref_costs[f, self.choices[f, 1]] = 50
            self.pref_costs[f, self.choices[f, 2]] = 50 + 9 * n
            self.pref_costs[f, self.choices[f, 3]] = 100 + 9 * n
            self.pref_costs[f, self.choices[f, 4]] = 200 + 9 * n
            self.pref_costs[f, self.choices[f, 5]] = 200 + 18 * n
            self.pref_costs[f, self.choices[f, 6]] = 300 + 18 * n
            self.pref_costs[f, self.choices[f, 7]] = 300 + 36 * n
            self.pref_costs[f, self.choices[f, 8]] = 400 + 36 * n
            self.pref_costs[f, self.choices[f, 9]] = 500 + 36 * n + 199 * n

        # ---------- precompute accounting penalty matrix ----------
        self.penalty_matrix = np.zeros((176, 176))
        for i in range(176):
            for j in range(176):
                ni = i + 125
                nj = j + 125
                diff = abs(ni - nj)
                self.penalty_matrix[i, j] = (ni - 125.0) / 400.0 * (ni ** (0.5 + diff / 50.0))

    def _day_accounting(self, day, occupancy):
        if day < 1 or day > 100: return 0.0
        n_curr = occupancy[day]
        n_next = occupancy[day+1]
        if 125 <= n_curr <= 300 and 125 <= n_next <= 300:
            return self.penalty_matrix[int(n_curr - 125), int(n_next - 125)]
        else:
            diff = abs(n_curr - n_next)
            return max(0.0, (n_curr - 125.0) / 400.0 * (n_curr ** (0.5 + diff / 50.0)))

    def get_accounting_cost(self, occupancy):
        total = 0.0
        for d in range(100, 0, -1):
            total += self._day_accounting(d, occupancy)
        return total

    def get_total_cost(self, assignment, occupancy):
        pref_cost = sum(self.pref_costs[f, assignment[f]] for f in range(5000))
        acc_cost = self.get_accounting_cost(occupancy)
        violations = 0
        for d in range(1, 101):
            if occupancy[d] < 125: violations += (125 - occupancy[d]) * 1_000_000_000
            elif occupancy[d] > 300: violations += (occupancy[d] - 300) * 1_000_000_000
        return pref_cost, acc_cost, violations

    def greedy_init(self):
        assignment = np.zeros(5000, dtype=int)
        occupancy = np.zeros(102)
        order = np.argsort(-self.n_people)
        for f in tqdm(order, desc="Greedy init"):
            assigned = False
            for c in range(10):
                day = self.choices[f, c]
                if occupancy[day] + self.n_people[f] <= 300:
                    assignment[f] = day
                    occupancy[day] += self.n_people[f]
                    assigned = True
                    break
            if not assigned:
                day = np.argmin(occupancy[1:101]) + 1
                assignment[f] = day
                occupancy[day] += self.n_people[f]
        occupancy[101] = occupancy[100]
        return assignment, occupancy

    def local_search(self, assignment, occupancy, iterations=100000):
        ass = assignment.copy(); occ = occupancy.copy()
        pref, acc, viol = self.get_total_cost(ass, occ)
        current_total = pref + acc + viol
        for _ in tqdm(range(iterations), desc="Local search"):
            f = np.random.randint(5000); old_day = ass[f]; new_day = np.random.choice(self.choices[f])
            if old_day == new_day: continue
            n_f = self.n_people[f]; pref_delta = self.pref_costs[f, new_day] - self.pref_costs[f, old_day]
            affected = {old_day, old_day-1, new_day, new_day-1}
            affected_set = {d for d in affected if 1 <= d <= 100}
            old_acc = sum(self._day_accounting(d, occ) for d in affected_set)
            
            def single_day_viol(d, o):
                if d < 1 or d > 100: return 0
                if o[d] < 125: return (125 - o[d]) * 1_000_000_000
                elif o[d] > 300: return (o[d] - 300) * 1_000_000_000
                return 0
            
            old_viol = single_day_viol(old_day, occ) + single_day_viol(new_day, occ)
            occ[old_day] -= n_f; occ[new_day] += n_f; occ[101] = occ[100]
            acc_delta = sum(self._day_accounting(d, occ) for d in affected_set) - old_acc
            viol_delta = single_day_viol(old_day, occ) + single_day_viol(new_day, occ) - old_viol
            
            if pref_delta + acc_delta + viol_delta < 0:
                ass[f] = new_day; pref += pref_delta; acc += acc_delta; current_total += (pref_delta + acc_delta + viol_delta)
            else:
                occ[old_day] += n_f; occ[new_day] -= n_f; occ[101] = occ[100]
        return ass, occ

    def simulated_annealing(self, assignment, occupancy, iterations=500000, T_start=50.0, T_end=0.1):
        ass = assignment.copy(); occ = occupancy.copy()
        pref, acc, viol = self.get_total_cost(ass, occ)
        current_total = pref + acc + viol; best_total = current_total
        best_ass = ass.copy(); best_occ = occ.copy()
        cooling_rate = (T_end / T_start) ** (1.0 / iterations); T = T_start
        
        def get_viol(d_list, o):
            v = 0
            for d in d_list:
                if d < 1 or d > 100: continue
                if o[d] < 125: v += (125 - o[d]) * 1_000_000_000
                elif o[d] > 300: v += (o[d] - 300) * 1_000_000_000
            return v

        for i in tqdm(range(iterations), desc="Simulated annealing"):
            move_type = np.random.rand()
            if move_type < 0.3: # Swap
                f1 = np.random.randint(5000); f2 = np.random.randint(5000); d1, d2 = ass[f1], ass[f2]
                if d1 == d2: continue
                n1, n2 = self.n_people[f1], self.n_people[f2]
                pref_delta = (self.pref_costs[f1, d2] - self.pref_costs[f1, d1]) + (self.pref_costs[f2, d1] - self.pref_costs[f2, d2])
                affected = {d1, d1-1, d2, d2-1}; affected_set = {d for d in affected if 1 <= d <= 100}
                old_acc = sum(self._day_accounting(d, occ) for d in affected_set); old_viol = get_viol({d1, d2}, occ)
                occ[d1] += (n2 - n1); occ[d2] += (n1 - n2); occ[101] = occ[100]
                acc_delta = sum(self._day_accounting(d, occ) for d in affected_set) - old_acc
                viol_delta = get_viol({d1, d2}, occ) - old_viol
                total_delta = pref_delta + acc_delta + viol_delta
            else: # Move
                f = np.random.randint(5000); old_day = ass[f]
                new_day = np.random.choice(self.choices[f]) if move_type < 0.9 else np.random.randint(1, 101)
                if old_day == new_day: continue
                n_f = self.n_people[f]; pref_delta = self.pref_costs[f, new_day] - self.pref_costs[f, old_day]
                affected = {old_day, old_day-1, new_day, new_day-1}; affected_set = {d for d in affected if 1 <= d <= 100}
                old_acc = sum(self._day_accounting(d, occ) for d in affected_set); old_viol = get_viol({old_day, new_day}, occ)
                occ[old_day] -= n_f; occ[new_day] += n_f; occ[101] = occ[100]
                acc_delta = sum(self._day_accounting(d, occ) for d in affected_set) - old_acc
                viol_delta = get_viol({old_day, new_day}, occ) - old_viol
                total_delta = pref_delta + acc_delta + viol_delta

            if total_delta < 0 or np.random.rand() < np.exp(-total_delta / T):
                if move_type < 0.3: ass[f1], ass[f2] = d2, d1
                else: ass[f] = new_day
                pref += pref_delta; acc += acc_delta; current_total += total_delta
                if current_total < best_total:
                    best_total = current_total; best_ass = ass.copy(); best_occ = occ.copy()
            else:
                if move_type < 0.3: occ[d1] += (n1 - n2); occ[d2] += (n2 - n1)
                else: occ[old_day] += n_f; occ[new_day] -= n_f
                occ[101] = occ[100]
            T *= cooling_rate
            if i % 200000 == 0: tqdm.write(f"Iter {i:6d} | T: {T:.2f} | Best: {best_total:,.0f}")
        return best_ass, best_occ

if __name__ == "__main__":
    opt = SantaOptimizer("data/family_data.csv")
    ass, occ = opt.greedy_init()
    ass, occ = opt.local_search(ass, occ, iterations=200000)
    ass, occ = opt.simulated_annealing(ass, occ, iterations=1000000, T_start=50.0, T_end=0.01)
    p, a, v = opt.get_total_cost(ass, occ)
    print(f"Final | Total: {p+a+v:,.0f} (Pref: {p:,.0f}, Acc: {a:,.0f}, Viol: {v:,.0f})")
    with open("optimized_submission.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["family_id", "assigned_day"])
        for i, d in enumerate(ass):
            writer.writerow([i, d])
