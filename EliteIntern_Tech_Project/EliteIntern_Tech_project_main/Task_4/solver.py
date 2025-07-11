from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value
import matplotlib.pyplot as plt
import numpy as np
import os

def solve_lp(machine_names, product_names, time_matrix, machine_time, stock, demand):
    prob = LpProblem("Production Optimization", LpMaximize)
    products = [LpVariable(f"x{i}", lowBound=0) for i in range(len(product_names))]

    # Objective
    prob += lpSum(products), "Total_Production"

    # Constraints
    for j, machine in enumerate(machine_names):
        prob += lpSum(time_matrix[i][j] * products[i] for i in range(len(product_names))) <= machine_time[j] * 60

    for i in range(len(product_names)):
        prob += products[i] >= demand[i] - stock[i]

    prob.solve()
    solution = {product_names[i]: value(products[i]) for i in range(len(products))}

    # Plot 1 - Bar Chart
    fig1, ax1 = plt.subplots()
    ax1.bar(solution.keys(), solution.values(), color='green')
    ax1.set_ylabel('Units to Produce')
    ax1.set_title('Optimal Product Quantities')
    fig1.savefig('static/solution_plot.png')

    # Plot 2 - Constraints and Objective (only for 2 products)
    fig2, ax2 = plt.subplots()
    if len(product_names) == 2:
        x_vals = np.linspace(0, max(demand)*2, 200)
        for j in range(len(machine_names)):
            a = time_matrix[0][j]
            b = time_matrix[1][j]
            rhs = machine_time[j]*60
            y_vals = (rhs - a*x_vals)/b
            ax2.plot(x_vals, y_vals, label=f"{machine_names[j]}")

        # Add constraints from demand-stock
        ax2.axvline(demand[0] - stock[0], color='gray', linestyle='--', label=f"Min {product_names[0]}")
        ax2.axhline(demand[1] - stock[1], color='gray', linestyle='--', label=f"Min {product_names[1]}")

        ax2.set_xlim(left=0)
        ax2.set_ylim(bottom=0)
        ax2.set_xlabel(product_names[0])
        ax2.set_ylabel(product_names[1])
        ax2.legend()
        ax2.set_title("Constraint Region")
        fig2.savefig('static/equation_plot.png')
    else:
        fig2.clf()

    return solution, 'static/solution_plot.png', 'static/equation_plot.png'