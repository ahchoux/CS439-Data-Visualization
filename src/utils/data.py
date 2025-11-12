# functions for loading and manipulating data
import kagglehub
import pandas as pd

def load_bike_crash_data() -> pd.DataFrame:
    """
    Downloads the latest version of the bike crash dataset from Kaggle.

    Returns:
        pd.DataFrame: The loaded bike crash data as a DataFrame.
    """
    path = kagglehub.dataset_download("adityadesai13/11000-bike-crash-data")
    df = pd.read_csv(path)
    return df   