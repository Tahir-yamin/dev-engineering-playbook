# Optimization Solvers: Gurobi vs. CPLEX vs. CBC (PuLP)

The Kaggle notebook you referenced mentions three primary solvers. For the **Santa Workshop 2019** problem, the choice of solver determines whether you can reach the global optimum (68,888) or get stuck in a sub-optimal local minimum.

## 1. Gurobi & CPLEX (The "High-End" Choice)
*   **Performance**: These are the industry standard for Mixed Integer Programming (MIP). They use advanced heuristics and cutting planes that are significantly faster than open-source alternatives.
*   **Competition Reality**: Every single top-tier solution for this competition used Gurobi. 
*   **Why they matter here**: With **3.6 million variables**, the "Presolve" phase in Gurobi can prune 90% of the redundant constraints before the solver even starts. Open-source solvers often crash or run out of memory during this phase.

## 2. CBC (The "Open Source" Choice) via PuLP
*   **Performance**: CBC is solid for problems with < 10,000 variables, but for the Santa problem, it is "dangerously slow."
*   **PuLP Integration**: PuLP allows you to write the model in Python and export it to an `.lp` file that CBC reads.
*   **Strategy**: If using CBC, you **cannot** solve the full problem. You must use **Small Neighborhood Search**:
    1.  Fix 99% of the schedule.
    2.  Use CBC to optimize only 1% (e.g., 50 families).
    3.  Iterate.

## 3. The "Modern" Alternative: Google OR-Tools (CP-SAT)
While not listed in your specific text, **CP-SAT** is the modern successor for this problem type.
*   **Constraint Programming**: Instead of treating everything as a linear inequality ($Ax \le b$), CP-SAT treats it as a logic puzzle.
*   **Table Constraints**: You can use `AddAllowedAssignments` to handle the accounting penalty matrix directly without the 3.6M binary variables.

---

## 🛠️ Tahir's Lab Setup:
I have imported the official dataset into your workspace. You can now use the `cost_calculator.py` to benchmark any ideas.

### Recommended Next Step: 
Since you have **Torch** and **Sympy** installed, we can explore **Symbolic Optimization** to see if we can simplify the accounting penalty logic further before passing it to a solver.
