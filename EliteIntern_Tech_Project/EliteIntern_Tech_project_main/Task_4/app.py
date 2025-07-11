from flask import Flask, render_template, request
from solver import solve_lp
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        machine_names = request.form.getlist('machine_name')
        product_names = request.form.getlist('product_name')
        stock = list(map(int, request.form.getlist('stock')))
        demand = list(map(int, request.form.getlist('demand')))
        machine_time = [float(t) if t else 0 for t in request.form.getlist('machine_time')]

        time_matrix = []
        for i in range(len(product_names)):
            row = []
            for j in range(len(machine_names)):
                val = request.form.get(f'prod_{i}_mach_{j}', '0')
                row.append(float(val) if val else 0.0)
            time_matrix.append(row)

        solution, graph_path, eq_graph_path = solve_lp(machine_names, product_names, time_matrix, machine_time, stock, demand)

        table_data = {
            'Machines': machine_names,
            'Products': product_names,
            'Stock': stock,
            'Demand': demand,
            'Available Time': machine_time,
            'Time Matrix': time_matrix
        }

        return render_template('index.html', solution=solution, table_data=table_data,
                               graph_path=graph_path, eq_graph_path=eq_graph_path)

    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.mkdir('static')
    app.run(debug=True)