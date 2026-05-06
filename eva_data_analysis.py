import matplotlib.pyplot as plt
import pandas as pd

# Data source: https://data.nasa.gov/resource/eva.json (with modifications)
input_file = open('./eva-data.json', 'r', encoding='ascii')
output_file = open('./eva_data_analysis.csv', 'w', encoding='utf-8')
graph_file = './cumulative_eva_figure.png'

# Read in the EVA data with pandas
eva_df = pd.read_json(input_file, convert_dates=['date'], encoding='ascii')
eva_df['eva'] = eva_df['eva'].astype(float) # Set the missiun number to a float in the pandas df
eva_df.dropna(axis=0, subset=['duration', 'date'], inplace=True)

# Write EVA data to csv file 
eva_df.to_csv(output_file, index=False, encoding='utf-8') 

# Calculate cumulative time spent in space
eva_df.sort_values('date', inplace=True) # Sort EVA missions in df by date
eva_df['duration_hours'] = eva_df['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60) # Extract each mission duration and convert to hours (float)
eva_df['cumulative_time'] = eva_df['duration_hours'].cumsum() # Cumulatively sum and write each mission duration through time

# Create plot of cumulative time spent in space through time
plt.plot(eva_df['date'], eva_df['cumulative_time'], 'ko-')
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(graph_file)
plt.show()