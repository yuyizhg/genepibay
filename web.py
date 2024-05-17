from flask import Flask, request, render_template_string
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor

app = Flask(__name__)

# HTML form template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Run Jupyter Notebook</title>
</head>
<body>
    <h1>Enter Your Variable</h1>
    <form method="post">
        <input type="text" name="variable" placeholder="Enter your variable here">
        <input type="submit">
    </form>
    {% if output %}
        <h2>Output:</h2>
        <div>{{ output|safe }}</div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    output = None
    if request.method == 'POST':
        user_input = request.form['variable']
        output = run_notebook(user_input)
        return render_template_string(HTML_TEMPLATE, output=output)
    return render_template_string(HTML_TEMPLATE, output=output)

def run_notebook(user_input):
    # Load the notebook
    ## change notebook file name properly
    with open("simple.ipynb", "r") as f:
        nb = nbformat.read(f, as_version=4)

    # Update the notebook: Here you need to find the correct cell and variable to update
    # For example, assuming the first cell contains the variable
    code_cell = nb['cells'][0]
    code_cell['source'] = f"your_variable = '{user_input}'"

    # Execute the notebook
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ## change `output` to the local dir properly
    ep.preprocess(nb, {'metadata': {'path': 'output/'}})

    # Convert the executed notebook to HTML
    html_exporter = HTMLExporter()
    html_exporter.exclude_input = True  # Set to False if you want to include input cells in the output
    (body, resources) = html_exporter.from_notebook_node(nb)

    return body

if __name__ == '__main__':
    app.run(debug=True)
