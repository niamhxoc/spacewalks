import matplotlib.pyplot as plt
import pandas as pd
import sys
import seaborn as sns

def main(input_file, output_file, graph_file):
    print("--START--")

    # Read the data from JSON file
    eva_data = read_json_to_dataframe(input_file)

    # Convert and export data to CSV file
    write_dataframe_to_csv(eva_data, output_file)

    # Calculate the time spent in space as a function of time and create a plot of the data
    plot_time_spent_in_space(eva_data,graph_file)

    print("--END--")

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

def plot_time_spent_in_space(df,graph_file):
    """
    Calculate the cumulative time spent in space as a function of time. Then plot the data as time spent in space on the y axis, and the date on the x axis

    Args:
        df (pd.dataFrame): The data to be processed and plotted
    """
    print(f'Plotting cumulative time spent in space and save to {graph_file}')
 
    # Calculate cumulative time spent in space
    df.sort_values('date', inplace=True) # Sort EVA missions in df by date
    df = add_duration_hours(df)
    df['cumulative_time'] = df['duration_hours'].cumsum() # Cumulatively sum and write each mission duration through time

    # Create plot of cumulative time spent in space through time
    sns.set_theme()
    sns.lineplot(data=df, x="date", y="cumulative_time", marker='.')
    #plt.plot(df['date'], df['cumulative_time'], 'ko-')
    plt.xlabel('Year')
    plt.ylabel('Total time spent in space to date (hours)')
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()

def text_to_duration(duration):
    """
    Convert a text format duration "HH:MM" to duration in hours

    Args:
        duration (str): The text format duration

    Returns:
        duration_hours (float): The duration in hours
    """
    hours, minutes = duration.split(":")
    duration_hours = int(hours) + int(minutes)/6  # there is an intentional bug on this line (should divide by 60 not 6)
    return duration_hours


def add_duration_hours(df):
    """
    Add duration in hours (duration_hours) variable to the dataset

    Args:
        df (pd.DataFrame): The input dataframe.

    Returns:
        df_copy (pd.DataFrame): A copy of df with the new duration_hours variable added
    """
    df_copy = df.copy()
    df_copy["duration_hours"] = df_copy["duration"].apply(
        text_to_duration
    )
    return df_copy


# Main code
if __name__=="__main__":

    if len(sys.argv) < 3:
        input_file = open('data/eva-data.json', 'r', encoding='ascii')
        output_file = open('results/eva_data_analysis.csv', 'w', encoding='utf-8')
        print('Using default input and output filenames.')
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        print('Using custom input and output filenames.')

    graph_file = 'results/cumulative_eva_figure.png'
    main(input_file,output_file,graph_file)