from src.cli import CLI
import os

if __name__ == "__main__":
    # Assuming the csv is in the same directory as system.py
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Dataset Books.csv")
    app = CLI(csv_path)
    app.run()


