import pandas as pd

# Load the CSV file
input_csv = 'allQuestions.csv'
output_csv = 'RandomlyChosen500Questions.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(input_csv)

# Randomly select 500 rows
df_sampled = df.sample(n=500, random_state=42)

# Save the sampled rows to a new CSV file
df_sampled.to_csv(output_csv, index=False)

print(f"Randomly selected 500 rows have been saved to {output_csv}")
