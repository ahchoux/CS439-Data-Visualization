# functions for loading and manipulating data
import kagglehub
import pandas as pd
import os

def load_bike_crash_data() -> pd.DataFrame:
    path = kagglehub.dataset_download("adityadesai13/11000-bike-crash-data")

    # Find the first CSV inside the downloaded directory
    for f in os.listdir(path):
        if f.endswith(".csv"):
            csv_path = os.path.join(path, f)
            break
    else:
        raise FileNotFoundError("No CSV file found in downloaded dataset")

    df = pd.read_csv(csv_path)
    return df