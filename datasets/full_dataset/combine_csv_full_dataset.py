import os
import pandas as pd

# Directory containing the CSV files
folder_path = r"D:\dataset_preprocessing\datasets\full_dataset"

# Find all CSV files
csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".csv")]

# List to store the dataframes
dataframes = []