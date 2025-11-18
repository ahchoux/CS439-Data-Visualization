# function(s) for plotting bar chart
import pandas as pd 

from typing import Dict
    
def generate_bar_chart_data(df: pd.DataFrame, groups: list[str] | None, column: str) -> Dict[str, Dict[str, float]] | Dict[str, float]:
    '''Generate a dictionary representing counts for bar chart visualization. For a 
    column 'Severity' and grouping by 'Time_of_Day', the output will be like:

    {
        'Low': {'Morning': 10, 'Afternoon': 5, 'Evening': 8},
        'Medium': {'Morning': 7, 'Afternoon': 12, 'Evening': 6},
        'High': {'Morning': 3, 'Afternoon': 4, 'Evening': 9}
    }

    If there is no grouping, the output will be like:

    {
        'Low': 15,
        'Medium': 25,
        'High': 16
    }

    Args:
        df (pd.DataFrame): DataFrame containing bike crash data with all filters applied
        groups (list[str] | None): List of columns to group by (e.g., ["Time_of_Day"]). None for no grouping.
        column (str): Column name in the DataFrame to categorize (e.g., "Severity")

    Returns:
        Dict[str, Dict[str, float]] | Dict[str, float]: A dictionary where keys are category names and values are dictionaries mapping group names to counts.
        If no grouping is provided, returns a single dictionary of counts for each category.
    '''
    if groups is None or len(groups) == 0:
        counts = df[column].value_counts().to_dict()
        return counts
    else:
        grouped = df.groupby(groups + [column]).size().unstack(fill_value=0)
        grouped = grouped.reindex(sorted(grouped.columns), axis=1)
        return {col: grouped[col].to_dict() for col in grouped.columns}

if __name__ == "__main__":
    # Example usage
    data = {
        'Time_of_Day': ['Morning', 'Morning', 'Afternoon', 'Evening', 'Evening', 'Evening'],
        'Severity': ['Low', 'High', 'Medium', 'Low', 'Medium', 'High']
    }
    df = pd.DataFrame(data)
    groups = ['Time_of_Day']
    column = 'Severity'
    counts = generate_bar_chart_data(df, groups, column)
    for k,v in counts.items():
        for sub_k, sub_v in v.items():
            print(f"{k} - {sub_k}: {sub_v}")