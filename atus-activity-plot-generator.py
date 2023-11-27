import pandas as pd
import numpy as np
import yaml as yml
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

# Specify the path to the YAML file
config_yaml_file_path = 'config.atus.yml'

# Open and read the YAML file
with open(config_yaml_file_path, 'r') as file:
    config_yaml_data = yml.safe_load(file)

working_directory = config_yaml_data["Working_Directory"]
data_dir = config_yaml_data["Data_Directory"]
year = config_yaml_data["Year"]
dataset_type = config_yaml_data["Dataset_Type"]
dataset_dir = f"{data_dir}/{year}/atus{dataset_type}_{year}/atus{dataset_type}_{year}.dat"
print(f"Retreiving Dataset From: {dataset_dir}")

# Load data
atus_df = pd.read_csv(dataset_dir)

# Convert time strings to datetime
base_date = f'{year}-01-01'
atus_df['TUSTARTTIM'] = pd.to_datetime(base_date + ' ' + atus_df['TUSTARTTIM'])
atus_df['TUSTOPTIME'] = pd.to_datetime(base_date + ' ' + atus_df['TUSTOPTIME'])

# Define Start time, Stop time, and Range array between the two
start_time = pd.to_datetime(f'{base_date}T04:00')
print(f"Start Time: {start_time}")
stop_time = start_time + pd.Timedelta(days=1)
print(f"Stop Time: {stop_time}")
atus_time_range = np.arange(start_time, stop_time, dtype='datetime64[m]')

# Adjust dates for times past midnight
atus_df.loc[atus_df['TUSTARTTIM'].dt.time < start_time.time(), 'TUSTARTTIM'] += pd.Timedelta(days=1)
atus_df.loc[atus_df['TUSTARTTIM'] > atus_df['TUSTOPTIME'], 'TUSTOPTIME'] += pd.Timedelta(days=1)

# Specify the path to the YAML file
activity_yaml_file_path = f'activity.{year}.atus.yml'

# Open and read the YAML file
with open(activity_yaml_file_path, 'r') as file:
    all_tier_codes = yml.safe_load(file)

### Generate all Tier 2 plots
### IN PROGRESS ###

'''for tier_1_codes in all_tier_codes.values():
    for tier_2_codes in tier_1_codes.values():'''
        
# Define all unique codes of selected tier
selected_tier = 'TUTIER1CODE'
all_selected_tier_activity_codes = atus_df[selected_tier].unique()
print(all_selected_tier_activity_codes)

# Dictionary where totals will be stored
total_persons_by_activity = {'Time': atus_time_range}
specific_activities_df = atus_df[atus_df[selected_tier].isin(all_selected_tier_activity_codes)]

# Checking the structure of the filtered DataFrame
#print(specific_activities_df)

# Looping through each activity 
for activity in all_selected_tier_activity_codes:
    
    # Filter the DataFrame for the current activity
    activity_df = specific_activities_df[specific_activities_df[selected_tier] == activity]
    
    # Create a mask for each row indicating where it falls in the time range
    mask = (total_persons_by_activity['Time'] >= activity_df['TUSTARTTIM'].values[:, None]) & \
           (total_persons_by_activity['Time'] < activity_df['TUSTOPTIME'].values[:, None])

    # Sum across the mask to get the count for each minute
    total_persons_by_activity[f'{tier_1_codes[activity]}'] = mask.sum(axis=0)