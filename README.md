# Bayesian Network for Genetic Epilepsy Prediction
Utilizing data extracted from OMIM, this project employs Bayesian Network modeling to enhance the diagnostic process for genetic epilepsy syndromes.

## Overview
This project is designed to streamline the diagnostic process for genetic epilepsy syndromes by leveraging data extracted from the Online Mendelian Inheritance in Man (OMIM) database. By using Bayesian Network modeling, we aim to provide a probabilistic framework that can assist clinicians in diagnosing these complex syndromes.

## Project Structure

### Data Preparation
The initial step involves extracting relevant data from the OMIM database. This is accomplished using the `clinical2.py` script.

- Script: `clinical2.py`
- Output: `seizure_epilepsy.json` (a JSON file containing the extracted data)


### Data Preprocessing and Model Building
After obtaining the raw data, the next step is to preprocess this data and build the Bayesian Network model. This process is detailed in the Jupyter notebook `FinalProject_BayesianNetwork_1.2.ipynb`.

- Notebook: `FinalProject_BayesianNetwork_1.2.ipynb`
- Purpose: Preprocess data and construct the Bayesian Network model


### Web Application
To provide an interface for interacting with the model, a web application is built using the `web.py` script. This allows users to input clinical data and receive diagnostic predictions based on the Bayesian Network model.

- Script: `web.py`
- Functionality: Web application for model interaction
