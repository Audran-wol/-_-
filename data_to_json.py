import pandas as pd

# Read the CSV file
with open('data.csv', 'r') as file:
    data = file.read().split('\\n\\nSubmission of new documents')
    print(data)

# Prepare a list to store the data
data_list = []

# Iterate over the data
for block in data[1:]:  # Skip the first block as it's likely to be empty
    lines = block.split('\\n')
    if len(lines) >= 3:
        data_dict = {
            'date': lines[0].strip(),
            'court_details': lines[1].strip(),
            'company_name_location': lines[2].strip()
        }
        data_list.append(data_dict)

# Convert the list to a DataFrame
df = pd.DataFrame(data_list)

# Write the DataFrame to a JSON file
df.to_json('data.json', orient='records')
