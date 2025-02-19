import pandas as pd


link_file = 'app/userdata/Alternate_link_files/only_defalt_links.csv'

df_link = pd.read_csv(link_file)

# Update all values in the 7th column (index 6) to "default"
df_link.iloc[:, 6] = "other"

# Save the updated DataFrame back to the same file
df_link.to_csv(link_file, index=False)

print(f"Updated CSV saved to {link_file}")

''' 
#Renumbering

df_link.iloc[:, 0] = range(1, len(df_link) + 1)

# Save the updated DataFrame to a new CSV file
df_link.to_csv(link_file, index=False)
print(f"Renumbered CSV saved to {link_file}")
'''


    
 

    