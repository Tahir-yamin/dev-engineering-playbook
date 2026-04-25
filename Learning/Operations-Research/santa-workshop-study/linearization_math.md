# The Math behind Winning: Linearizing the Accounting Penalty

In the 2019 Santa Workshop Tour, the "Accounting Penalty" was the primary bottleneck. Most competitors tried heuristics, but the winners used **Mixed Integer Programming (MIP)** by linearizing the non-linear penalty.

## 1. The Non-Linear Problem
The penalty function $P(d, d+1)$ for day $d$ and day $d+1$ with occupancies $N_d$ and $N_{d+1}$ is:
$$ P(N_d, N_{d+1}) = \frac{N_d - 125}{400} \cdot N_d^{\left(0.5 + \frac{|N_d - N_{d+1}|}{50}\right)} $$

This is non-linear and non-convex because of the $|N_d - N_{d+1}|$ in the exponent. Standard solvers cannot handle this directly.

---

## 2. The Linearization Hack (Integer Discretization)
Since $125 \le N_d \le 300$, there are only **176** possible integer values for $N_d$ per day.

We can define a binary variable:
$x_{i, j, d} = 1$ if Day $d$ has occupancy $i$ AND Day $d+1$ has occupancy $j$.

### The Pre-calculated Cost
For every pair $(i, j)$ in the range $[125, 300]$, we pre-calculate:
$$ C_{i, j} = \frac{i - 125}{400} \cdot i^{\left(0.5 + \frac{|i - j|}{50}\right)} $$

This results in a matrix of $176 \times 176 = 30,976$ possible costs.

### The Objective Function (Linear)
The total accounting penalty becomes:
$$ \text{Total Penalty} = \sum_{d=1}^{99} \sum_{i=125}^{300} \sum_{j=125}^{300} C_{i, j} \cdot x_{i, j, d} $$

Since $C_{i, j}$ is a constant and $x_{i, j, d}$ is binary, this objective is now **linear**.

---

## 3. The Network Constraints (The "Flow")
To make this work, we need "Continuity" constraints. If we pick pair $(i, j)$ for day $d$, then for day $d+1$, we **must** pick a pair starting with $j$, like $(j, k)$.

$$ \sum_{i=125}^{300} x_{i, j, d} = \sum_{k=125}^{300} x_{j, k, d+1} \quad \forall j \in [125, 300], d \in [1, 98] $$

This is equivalent to finding the **Shortest Path** on a layered graph where each layer is a "Day" and each node is an "Occupancy State".

---

## 🚀 How to Improve this Today?
1.  **Column Generation**: Instead of adding all 3M variables, start with a few "good" paths and add variables dynamically.
2.  **Constraint Programming (CP)**: Modern solvers like **Google OR-Tools CP-SAT** can handle the "Transition" logic using `AddAllowedAssignments` without exploding the variable count.
3.  **Neural Optimization**: Use a Transformer to predict the sequence of $N_d$ (the "occupancy vector") and use that as a seed for the solver.
