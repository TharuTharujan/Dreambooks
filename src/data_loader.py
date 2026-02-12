import pandas as pd
from typing import Optional
from .interfaces import IDataLoader

# SOLID Principle: Single Responsibility Principle (SRP)
# CSVDataLoader has one reason to change: the logic for loading and cleaning CSV data.
# SOLID Principle: Liskov Substitution Principle (LSP)
# CSVDataLoader can replace IDataLoader without affecting the correctness of the program.
class CSVDataLoader(IDataLoader):
    """
    Concrete implementation of IDataLoader for CSV files.
    Responsible for loading and basic cleaning of the data.
    """
    def __init__(self, limit: int = 5000):
        self.limit = limit

    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Loads data from a CSV file.
        Limits the rows to self.limit.
        Performs basic cleaning.
        """
        try:
            # Load only the first 'limit' rows
            df = pd.read_csv(file_path, nrows=self.limit)
            
            # Basic cleaning:
            # 1. Clean column names (strip whitespace)
            df.columns = df.columns.str.strip()
            
            # 2. Handle missing values (strategies can vary, here we might fill or drop critical ones)
            # For now, we will just ensure critical columns are strings
            if 'publication date' in df.columns:
                df['publication date'] = pd.to_numeric(df['publication date'], errors='coerce')
                
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {file_path} was not found.")
        except Exception as e:
            raise Exception(f"Error loading data: {e}")
