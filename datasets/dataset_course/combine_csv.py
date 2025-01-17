import pandas as pd

# File paths
file_paths = {
    "30_mins": "recipe_30_mins.csv",
    "breakfast": "recipe_breakfast.csv",
    "cookies": "recipe_cookies.csv",
    "cottage_cheese": "recipe_cottage_cheese.csv",
    "desserts": "recipe_desserts.csv",
    "dinner": "recipe_dinner.csv",
    "lunch": "recipe_lunch.csv",
    "meal_prep": "recipe_meal_prep.csv",
    "sauces_seasoning": "recipe_sauces_seasoning.csv",
    "sides_appetizers": "recipe_sides_appetizers.csv"

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

    # Append the tagged dataset to the list
    tagged_datasets.append(data)

# Combine all datasets into one
combined_data = pd.concat(tagged_datasets, ignore_index=True)

# Save combined dataset
combined_data.to_csv("tagged_recipes_by_course.csv", index=False)

# Inspect combined data
print(combined_data.head())


# List of columns to aggregate (binary_tags)
binary_columns = ["30_mins","breakfast","cookies","cottage_cheese","desserts",
                        "dinner","lunch","meal_prep","sauces_seasoning","sides_appetizers"]
tagged_combined_data = combined_data.groupby("recipe_id", as_index=False).agg(
    {
        **{col: 'max' for col in binary_columns},
        **{col: 'first' for col in combined_data.columns if col not in binary_columns + ["recipe_id"]}
    }
)

# Save the combined dataset
tagged_combined_data.to_csv("combined_tagged_recipes_by_course.csv", index=False)