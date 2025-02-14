import pandas as pd
from sklearn.model_selection import train_test_split

# Load the deduplicated dataset
deduplicated_file_path = r'scrap\PhapLuat_VietnamNet_deduplicated.xlsx'  # Update the path to your local file
deduplicated_df = pd.read_excel(deduplicated_file_path)

# Load the new dataset
new_dataset_path = r'scrap\PhapLuat_VNExpress_deduplicated.csv'  # Update the path to your local file
new_dataset_df = pd.read_csv(new_dataset_path)

# Drop the 'Link' column from the deduplicated dataset
deduplicated_df = deduplicated_df.drop(columns=['Link'])

# Merge the datasets
merged_df = pd.concat([deduplicated_df, new_dataset_df], ignore_index=True)

# Define split ratios
train_ratio = 0.7
test_ratio = 0.2
val_ratio = 0.1

# Split the dataset into train and temp (test + val)
train_df, temp_df = train_test_split(merged_df, test_size=(1 - train_ratio), random_state=42)

# Split the temp dataset into test and validation
test_df, val_df = train_test_split(temp_df, test_size=(val_ratio / (test_ratio + val_ratio)), random_state=42)

# Save the datasets
train_output_path = r'my_data\train.csv'
test_output_path = r'my_data\test.csv'
val_output_path = r'my_data\val.csv'

train_df.to_csv(train_output_path, index=False, encoding = 'utf-8-sig')
test_df.to_csv(test_output_path, index=False, encoding = 'utf-8-sig')
val_df.to_csv(val_output_path, index=False, encoding = 'utf-8-sig')

print(f"Train dataset saved to {train_output_path}")
print(f"Test dataset saved to {test_output_path}")
print(f"Validation dataset saved to {val_output_path}")

