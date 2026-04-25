# Implementation Plan: Santa Workshop Optimization Study

## Overview
This project aims to analyze the 2019 Kaggle "Santa's Workshop Tour" competition, specifically focusing on the winning MIP (Mixed Integer Programming) strategy by Felix Willamowski. We will explore potential improvements using modern solvers (Google OR-Tools CP-SAT) and alternative modeling techniques.

---

## Phase 1: Deep Analysis & Mathematical Foundations
### Goal: Deconstruct the winning strategy and the "Accounting Penalty" challenge.

- **Tasks**:
  - [x] Research the exact linearization of the non-linear accounting penalty.
  - [x] Determine the number of variables and constraints (3.6M variables, Shortest Path on Graph).
  - [x] Document Gurobi strategy vs. Open-source alternatives.

---

## Phase 2: Modernization & Improvement Proposal
### Goal: Identify what can be improved 5 years later (2024+).

- **Potential Improvements**:
  - **Solver Swap**: Transition from pure MIP to **CP-SAT**. CP-SAT's `AddAllowedAssignments` is statistically superior for "Transition Matrix" problems.
  - **Differentiable Layers**: Implementing a "Neural Warm-start" using PyTorch.
  - **Resilience Modeling**: Viewing the Accounting Penalty as a "System Stability" metric for Digital Twins.

---

## Phase 3: Prototype Implementation (Small Scale)
### Goal: Build a functional solver for a reduced version of the problem.

- **Tasks**:
  - [x] Create project structure in `Learning/Operations-Research/santa-workshop-study`.
  - [x] Implement synthetic data generator (`generate_data.py`).
  - [ ] Implement CP-SAT model (Pending `ortools` installation).
  - [ ] Benchmark against Greedy.

---

## Phase 4: PhD Research Bridge
### Goal: Align this study with Digital Twin and Logistics research goals.

- **Tasks**:
  - [ ] Document "Logistics Resilience" mapping.
  - [ ] Finalize "Optimal Workshop Scheduling" paper draft/notes.
