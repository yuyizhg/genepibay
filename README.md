# Bayesian Network for Genetic Epilepsy Diagnostic
Utilizing data extracted from OMIM, this project employs Bayesian Network modeling to enhance the diagnostic process for genetic epilepsy syndromes.

## Overview
This project is designed to streamline the diagnostic process for genetic epilepsy syndromes by leveraging data extracted from the Online Mendelian Inheritance in Man (OMIM) database. By using Bayesian Network modeling, we aim to provide a probabilistic framework that can assist clinicians in diagnosing these complex syndromes.

## Project Structure

### Data Preparation
The initial step involves extracting relevant data from the OMIM database. This is accomplished using the `clinical2.py` script.

- Script: `clinical2.py`
- Output: `seizure_epilepsy.json` (a JSON file containing the extracted data)


### Data Preprocessing and Model Building
After obtaining the raw data, the next step is to preprocess this data and build the Bayesian Network model. This process is detailed in the Jupyter notebook `Bayesian Network for Genetic Epilepsy Diagnostic.py`.

- Notebook: `Bayesian Network for Genetic Epilepsy Diagnostic.py`
- Purpose: Preprocess data and construct the Bayesian Network model


### Web Application
To provide an interface for interacting with the model, a web application is built using the `web.py` script. This allows users to input clinical data and receive diagnostic predictions based on the Bayesian Network model.

- Script: `web.py`
- Functionality: Web application for model interaction

## How to Run
### env setup
Make sure python is properly installed. Then a virtual env can be set up with the following commands:

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### run scripts

```shell
pwd
## Make sure this is under the genepibay directory

# data preparation
python clinical2.py
## This may take a minute or two to run, and upon completion will generate a seizure_epilepsy.json file

# data preprocessing and model building
python BayesianNetwork4GeneticEpilepsyDiagnostic.py 
## This will take longer time, about 5 minutes.

# web application
python web.py
```
