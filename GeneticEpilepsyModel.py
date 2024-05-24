
# 1. Import preperation
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




def initialize_model():
    # Define the path to your JSON file in your local environment
    json_file_path = 'seizure_epilepsy.json'
    # Read JSON data
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    # Convert JSON data to DataFrame
    df = pd.DataFrame(data)



    # 2. Data preprocessing
    # Drop duplicated records
    df1 = df.drop_duplicates(subset=['mimNumber']).reset_index(drop=True)
    # Remove mimNumber column
    df2 = df1[['preferredTitle', 'clinicalSynopsis']]
    #print(df2)

    # One-hot encoding
    # Splitting the strings in 'clinicalSynopsis' into individual labels and creating a new DataFrame
    expanded_df= df2['clinicalSynopsis'].apply(pd.Series).stack().reset_index(level=1, drop=True).to_frame('label')
    # One-hot encoding the labels
    one_hot_encoded = pd.get_dummies(expanded_df, prefix='', prefix_sep='')
    #print(one_hot_encoded)

    # Group by index and sum up rows with the same index
    summed_up_rows = one_hot_encoded.groupby(one_hot_encoded.index).sum()
    # Concatenating the one-hot encoded DataFrame with the 'preferredTitle' column
    df3 = pd.concat([df2['preferredTitle'], summed_up_rows], axis=1)
    # Remove "'" symbol from column names
    df3.columns = df3.columns.str.replace("'", "")
    #print(df3)

    # Remove records with null value in clinicalSynopsis
    df4 = df3.dropna(subset=['Ballooned neurons with autofluorescent fine granular material']).reset_index(drop=True)
    #print(df4)

    # # Check for duplicated column names
    # duplicated_columns = df4.columns[df4.columns.duplicated()]
    # if len(duplicated_columns) > 0:
    #     print("Duplicate column names found:", duplicated_columns)
    # else:
    #     print("No duplicate column names found.")


    # Deal with duplicated columns
    # Get duplicated column names
    duplicated_columns = df4.columns[df4.columns.duplicated()]
    # Create a DataFrame to store the summed values
    summed_df = pd.DataFrame(columns=duplicated_columns)
    # Sum up values for each duplicated column
    for column in duplicated_columns:
        summed_df[column] = df4.groupby(level=0, axis=1).sum()[column]
    # Drop the duplicated columns from the original DataFrame
    df4_cleaned = df4.drop(columns=duplicated_columns)
    # Concatenate the original DataFrame and the DataFrame with summed values
    df5 = pd.concat([df4_cleaned, summed_df], axis=1)
    #print(df5)


    # Copy the dataframe
    df6 = df5.iloc[:, 1:]
    # Replace values other than 0 and 1 with 1 in all columns
    df6 = df6.where((df6 == 0) | (df6 == 1), 1)
    # Concatenating the adjusted DataFrame with the 'preferredTitle' column
    df6 = pd.concat([df5['preferredTitle'], df6], axis=1)
    #print(df6)




    # 3. Model building
    # 3.1 Build the Bayesian Network
    # Define the structure of the Bayesian Network model
    structure = [("preferredTitle", symptom) for symptom in df6.columns[1:]]
    # Create Bayesian Network model
    model = BayesianNetwork()
    for edge in structure:
        model.add_edge(*edge)
    #print("Number of edges: {}".format(len(model.edges())))
    #print("Number of nodes: {}".format(len(model.nodes())))

    # 3.2 Learn the model parameters from the data
    # Estimate parameters using Bayesian Estimator
    model.fit(df6, estimator=BayesianEstimator)

    # Create VariableElimination
    ve = VariableElimination(model)

    return ve, df6.columns[1:].tolist()