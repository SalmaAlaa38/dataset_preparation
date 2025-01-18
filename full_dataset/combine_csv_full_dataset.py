import os
import pandas as pd
from functools import reduce

# Directory containing the CSV files
folder_path = r"D:\dataset_preprocessing\full_dataset"

# Find all CSV files
csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".csv")]

# List to store the dataframes
dataframes = []

for file in csv_files:
    df = pd.read_csv(file)
    if 'recipe_id' in df.columns:  # Ensure the file has the 'recipe_id' column
        dataframes.append(df)
    else:
        print(f"Skipping file {file} because it doesn't have a 'recipe_id' column.")


merged = reduce(lambda left, right: pd.merge(left, right, on="recipe_id", how="outer", suffixes=('', '_dup')), dataframes)

# Define binary columns and fill missing values with 0
binary_columns = ['dairy_free', 'gluten_free',
                  '30_mins', 'breakfast', 'cookies', 'cottage_cheese', 'desserts',
                  'dinner', 'lunch', 'meal_prep', 'sauces_seasoning', 'sides_appetizers',
                  '4th_july','christmas','cinco_de_mayo','easter','fathers_day',
                  'labor_day','memorial_day','mothers_day','tagged_recipes_by_holiday','thanksgiving','valentienes_day',
                  'beef','chicken','pork','recipe_turkey','seafood',
                  'fall','pumpkin','spring','summer','winter'
]

for col in binary_columns:
    if col in merged.columns:
        merged[col] = merged[col].fillna(0).astype(int)

for col in merged.columns:
    if col.endswith('_dup'):
        if col in merged.columns:  # Check if the column exists
            merged.drop(columns=col, inplace=True)
        else:
            print(f"Column {col} not found in merged dataframe.")

merged['recipe_id'] = merged['recipe_id'].astype(int)

merged.to_csv("full_recipes_dataset.csv", index=False)

print(merged.head())
print(merged.info())