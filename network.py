import pandas as pd
from simpledbf import Dbf5

# read the link dbf to a csv and export
def dbflinks_to_csv(dbf_file, csv_file):
    # Read the DBF file
    dbf = Dbf5(dbf_file)
    df = dbf.to_dataframe()

    #process link information

    # Write to CSV file
    df.to_csv(csv_file, index=False)


def dbfnodes_to_csv(dbf_file, csv_file):
    # Read the DBF file
    dbf = Dbf5(dbf_file)
    df = dbf.to_dataframe()

    # process the node information

    # Write to CSV file
    df.to_csv(csv_file, index=False)


if __name__ == "__main__":
    
    # read in highway network and write out csv file
    input_dbf = 'highway.dbf'  # Replace with your DBF file path
    output_csv = 'links.csv'  # Replace with your desired CSV file path

    dbflinks_to_csv(input_dbf, output_csv)
    print(f"Converted links '{input_dbf}' to '{output_csv}' successfully.")

    # read in nodes and write out CSV file
    inputn_dbf = 'nodes.dbf'  # Replace with your DBF file path
    outputn_csv = 'nodes.csv'  # Replace with your desired CSV file path

    dbfnodes_to_csv(inputn_dbf, outputn_csv)
    print(f"Converted nodes '{inputn_dbf}' to '{outputn_csv}' successfully.")

import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('links.csv')

# Define the columns you want to keep
new_order = ['ID', 'RTE_NAME', 'A', 'B', 'DIR', 'DISTANCE', 'FACTYPE', 'CAP_R', 'FFSPEED_R', 'LANES', 'BIKE_FAC']  # Replace with your desired columns

# Drop columns that are not in the new order
df = df[new_order]

# Save the modified DataFrame back to the same CSV file
df.to_csv('links.csv', index=False)

import pandas as pd

# Step 1: Read the CSV file
df = pd.read_csv('links.csv')

# Step 2: Rename the columns
# For example, if you want to rename 'old_name1' to 'new_name1' and 'old_name2' to 'new_name2':
df.rename(columns={'ID': 'link_id', 'RTE_NAME': 'name', 'A': 'from_node_id', 'B': 'to_node_id', 'DIR': 'directed', 'DISTANCE': 'length', 'FACTYPE': 'facility_type', 'CAP_R': 'capacity', 'FFSPEED_R': 'free_speed', 'LANES': 'lanes', 'BIKE_FAC': 'bike_facility'}, inplace=True)

# Step 3: Save the modified DataFrame back to a CSV file
df.to_csv('links.csv', index=False)

import pandas as pd

# Step 1: Read the CSV file
df = pd.read_csv('nodes.csv')

# Step 2: Rename the columns
# For example, if you want to rename 'old_name1' to 'new_name1' and 'old_name2' to 'new_name2':
df.rename(columns={'N': 'node_id', 'X': 'x_coord', 'Y': 'y_coord'}, inplace=True)

# Step 3: Save the modified DataFrame back to a CSV file
df.to_csv('nodes.csv', index=False)
