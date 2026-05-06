import matplotlib.pyplot as plt
import pandas as pd

def read_json_to_dataframe(input_file):
    """
    Read the data from a JSON file into a pandas dataframe. 
    Clean the data by removing any rows where the duration is missing.

    Args:
        input_file (file or str): The file object or the path to the JSON file.

    Returns:
        eva_df (pd.DataFrame): The cleaned data as a dataframe structure
    """
    print(f"Reading JSON file {input_file}")

    # Read in the EVA data with pandas
    eva_df = pd.read_json(input_file, convert_dates=['date'], encoding='ascii')
    eva_df['eva'] = eva_df['eva'].astype(float) # Set the mission number to a float in the pandas df
    eva_df.dropna(axis=0, subset=['duration', 'date'], inplace=True) # Clean data by removing rows where duration is empty

    return eva_df

def write_dataframe_to_csv(df, output_file):
    """
    Write the data from a pandas dataframe, to a CSV file

    Args:
        df (pd.DataFrame): The data as a dataframe structure
        output_file (file or str): The file object or the path to the CSV file to be written.
    """
    print(f'Saving to CSV {output_file}')

    # Write EVA data to csv file 
    df.to_csv(output_file, index=False, encoding='utf-8') 

def plot_time_spent_in_space(df):
    """
    Calculate the cumulative time spent in space as a function of time. Then plot the data as time spent in space on the y axis, and the date on the x axis

    Args:
        df (pd.dataFrame): The data to be processed and plotted
    """
    print(f'Plotting cumulative time spent in space and save to {graph_file}')
 
    # Calculate cumulative time spent in space
    df.sort_values('date', inplace=True) # Sort EVA missions in df by date
    df['duration_hours'] = df['duration'].str.split(":").apply(lambda x: int(x[0]) + int(x[1])/60) # Extract each mission duration and convert to hours (float)
    df['cumulative_time'] = df['duration_hours'].cumsum() # Cumulatively sum and write each mission duration through time

    # Create plot of cumulative time spent in space through time
    plt.plot(eva_data['date'], eva_data['cumulative_time'], 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.grid(alpha=0.2)
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()

# Data source: https://data.nasa.gov/resource/eva.json (with modifications)
input_file = open('./eva-data.json', 'r', encoding='ascii')
output_file = open('./eva_data_analysis.csv', 'w', encoding='utf-8')
graph_file = './cumulative_eva_figure.png'

print("--START--")

# Read the data from JSON file
eva_data = read_json_to_dataframe(input_file)

# Convert and export data to CSV file
write_dataframe_to_csv(eva_data, output_file)

# Calculate the time spent in space as a function of time and create a plot of the data
plot_time_spent_in_space(eva_data)

print("--END--")