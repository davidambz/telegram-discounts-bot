import pandas as pd
from datetime import datetime, timedelta


csv_file = 'sent_products.csv'

try:
    data = pd.read_csv(csv_file)
    data['Data'] = pd.to_datetime(data['Data'])
    one_week_ago = datetime.now() - timedelta(days=7)
    data = data[data['Data'] > one_week_ago]
    data.to_csv(csv_file, index=False)

    print("Old lines successfully removed.")

except FileNotFoundError:
    print(f"The file {csv_file} was not found.")
except Exception as e:
        print(f"An error occurred: {e}")
