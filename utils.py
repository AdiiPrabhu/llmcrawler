import json
import pandas as pd

def save_data(data, output_file):
    if output_file.endswith(".csv"):
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
    elif output_file.endswith(".json"):
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
