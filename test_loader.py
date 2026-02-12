import sys
import os
sys.path.append(os.getcwd())

from src.data_loader import CSVDataLoader

def test_loader():
    csv_path = "c:/Users/LENOVO/Documents/APDP/Dataset Books.csv"
    loader = CSVDataLoader(limit=100)
    try:
        df = loader.load_data(csv_path)
        print("Data loaded successfully!")
        print(f"Columns: {df.columns.tolist()}")
        print(f"Rows: {len(df)}")
        print(df.head())
    except Exception as e:
        print(f"Failed to load data: {e}")

if __name__ == "__main__":
    test_loader()
