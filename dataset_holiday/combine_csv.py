import os
import pandas as pd

# Directory containing the CSV files
folder_path = r"D:\dataset_preprocessing\datasets\dataset_holiday"

# Dynamically generate file paths dictionary
file_paths = {
    os.path.splitext(file)[0]: os.path.join(folder_path, file)
    for file in os.listdir(folder_path) if file.endswith(".csv")
}

# Empty list to store dataframes
tagged_datasets = []

# Process each dataset
for category, path in file_paths.items():
    # Load dataset
    data = pd.read_csv(path)

    # Add binary columns for all categories
    for cat in file_paths.keys():
        data[cat] = 1 if cat == category else 0

    # Append the tagged datasets the list
    tagged_datasets.append(data)

# Combine all the datasets into one
combined_data = pd.concat(tagged_datasets, ignore_index=True)

# Save combined dataset
combined_data.to_csv("tagged_recipes_by_holiday.csv", index=False)

# List of columns to aggregate (binary_tags)
binary_columns = list(file_paths.keys())

# Group by 'recipe_id' and aggregate
tagged_combined_data = combined_data.groupby("recipe_id", as_index=False).agg(
    {
        **{col: 'max' for col in binary_columns},
        **{col: 'first' for col in combined_data.columns if col not in binary_columns + ["recipe_id"]}
    }
)

# Save the combined dataset
tagged_combined_data.to_csv("combined_tagged_recipes_by_holiday.csv", index=False)

# Inspect combined dataset
print(f"Processed {len(file_paths)} datasets.")
print(tagged_combined_data.head())