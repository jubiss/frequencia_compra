import os.path
import pandas as pd
def save_csv(dataframe, filepath_name, save=False):
    if save:
        if os.path.exists(filepath_name):
            overwrite = input(f"File {filepath_name.split('/')[-1]} Exist overwrite the file? [S/N]")
            if overwrite == "S":
                dataframe.to_csv(filepath_name, index=False)
            else:
                return
        else:
            dataframe.to_csv(filepath_name, index=False)

def read_sql_file(sql_path):
    with open(sql_path, 'r') as sql_file:
        query = sql_file.read()
    return query

def append_column_names(dataframe, sufix_text=None, prefix_text=None):
    columns = []
    for column in dataframe.columns:
        columns.append(f'{prefix_text}_{column}_{sufix_text}')
    dataframe.columns = columns
    return dataframe

def many_to_one(df, index_columns):
    many_one_index = 'index'
    index_values = list(zip(*[df[col] for col in index_columns]))
    df[many_one_index] = pd.factorize(index_values)[0]
    many_to_one_relation = df[index_columns]
    many_to_one_relation[many_one_index] = df[many_one_index]
    df = df.drop(columns=index_columns)
    df = df.set_index(many_one_index)
    return df, many_to_one_relation


def calculate_grouped_error_metrics(grouped_data, value_column, metric='StdDev', confidence_level=0.95, bootstrap_iterations=1000):
    import numpy as np
    import scipy.stats as stats
    """
    Example Usage:
    grouped_data = df.groupby(by='garages')

    error_metrics = ['CI',]
    value_column = 'value'

    for metric in error_metrics:
        result = calculate_grouped_error_metrics(grouped_data, group_column='garages', value_column=value_column, metric=metric)
        print(f"{metric}: {result}")"""
    

    results = {}
    
    for group, data in grouped_data:
        values = data[value_column]
        
        if metric == 'StdDev':
            results[group] = np.std(values)
        
        elif metric == 'StdErr':
            results[group] = np.std(values) / np.sqrt(len(values))
        
        elif metric == 'CI':
            mean = np.mean(values)
            std_error = np.std(values) / np.sqrt(len(values))
            t_critical = stats.t.ppf((1 + confidence_level) / 2, df=len(values) - 1)
            results[group] = (mean - t_critical * std_error, mean + t_critical * std_error)
        
        elif metric == 'Percentiles':
            results[group] = np.percentile(values, [25, 50, 75])
        
        elif metric == 'Bootstrap Intervals':
            bootstrap_means = []
            for _ in range(bootstrap_iterations):
                bootstrap_sample = np.random.choice(values, size=len(values), replace=True)
                bootstrap_means.append(np.mean(bootstrap_sample))
            
            confidence_interval = np.percentile(bootstrap_means, [100 * (1 - confidence_level) / 2, 100 * (1 + confidence_level) / 2])
            results[group] = (confidence_interval[0], confidence_interval[1])
        
        elif metric == 'MAD':
            results[group] = np.median(np.abs(values - np.median(values)))
        
        else:
            raise ValueError("Invalid metric choice")
    
    return results
