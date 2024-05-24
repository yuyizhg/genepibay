from flask import Flask, request, render_template_string
import subprocess
import pandas as pd
import json
import sys
import pgmpy
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import BayesianEstimator
from pgmpy.inference import VariableElimination
# import networkx as nx
# import matplotlib.pyplot as plt
# import seaborn as sns

from GeneticEpilepsyModel import initialize_model


app = Flask(__name__)
ve = None
options = []



# HTML template with a form and a multiple selection box
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multiple Selection Form</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/css/select2.min.css" rel="stylesheet" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.13/js/select2.min.js"></script>
    <script>
        $(document).ready(function() {
            $('#user_inputs').select2();
        });
    </script>
</head>
<body>
    <h1>Select your inputs</h1>
    <form method="post">
        <label for="user_inputs">Choose multiple options:</label>
        <select id="user_inputs" name="user_inputs" multiple="multiple" style="width: 300px;">
            {% for option in options %}
                <option value="{{ option }}">{{ option }}</option>
            {% endfor %}
        </select>
        <button type="submit">Submit</button>
    </form>
    {% if output %}
        <h2>Output:</h2>
        <pre>{{ output }}</pre>
    {% endif %}
</body>
</html>
'''



# 3.3 Query the network without evidence
def to_str_top_k_results(factor, k=10, tablefmt="grid"):
    from pgmpy.extern import tabulate
    # Create a list of all rows
    all_rows = list(zip(factor.state_names[factor.variables[0]], factor.values))
    # Sort by values and create a table
    top_k = sorted(all_rows, key=lambda tup: tup[1])[::-1][:k]
    table = tabulate(top_k, headers = ['dx','p(dx)'], tablefmt=tablefmt)
    return table



@app.route('/', methods=['GET', 'POST'])
def index():
    global ve
    output = None
    if request.method == 'POST':
        user_inputs = request.form.getlist('user_inputs')
        # Use the model object if needed
        print(f"Using model: {ve}")
        evidence = {inp: 1.0 for inp in user_inputs}
        query_result = ve.query(variables=['preferredTitle'], evidence=evidence)
        # Check results
        output = to_str_top_k_results(query_result)
    return render_template_string(html_template, output=output, options=options)



if __name__ == '__main__':
    print('Starting webapp, initializing model...')
    ve, options = initialize_model() 
    print('Model built in http://127.0.0.1:5000/')
    app.run(debug=True)