from haversine import haversine
import pandas as pd
import numpy as np

missing_temp_in_charlotte_df = charlotte_df[charlotte_df['Temperature(F)'].isna()]

for index, each_missing_entry in missing_temp_in_charlotte_df.iterrows():
    charlotte_df['Distance'] = charlotte_df.apply(lambda row: haversine((each_missing_entry['Start_Lat'], each_missing_entry['Start_Lng']), (row['Start_Lat'], row['Start_Lng'])), axis=1)
    
    nearby_entries = charlotte_df[charlotte_df['Distance'] <= 5]

    missing_date = pd.to_datetime(each_missing_entry['Start_Time']).date()

    three_day_entries = nearby_entries[pd.to_datetime(nearby_entries['Start_Time']).apply(lambda x: abs((x.date() - missing_date).days) <= 1)]

    if not three_day_entries.empty:
        average_temp = three_day_entries['Temperature(F)'].mean()
        charlotte_df.loc[index, 'Temperature(F)'] = average_temp