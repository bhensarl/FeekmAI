# yfpy/main.py
from data_loader import load_weekly_data
from data_processor import extract_data
import pandas as pd

# Combined dictionary for both game IDs and league IDs by year
combined_ids = {
    2018: {"game_id": 380, "league_id": "67583"},  # NFL - 2018
    2019: {"game_id": 390, "league_id": "43068"},  # NFL - 2019
    2020: {"game_id": 399, "league_id": "643103"},  # NFL - 2020
    2021: {"game_id": 406, "league_id": "333658"},  # NFL - 2021
    2022: {"game_id": 414, "league_id": "74941"},   # NFL - 2022
    2023: {"game_id": 423, "league_id": "219013"},  # NFL - 2023
}


def main():
    # Set Pandas display options
    pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.max_colwidth', None)  # Show full width of columns

    season_number = "2022"
    cumulative_data = {}  # Initialize as needed
    all_data = pd.DataFrame()  # Initialize as needed

    # Loop through all weeks (assuming 18 weeks for the NFL season)
    for week_number in range(1, 17):
        week_str = str(week_number)
        print(f"Processing Week {week_str}...")

        try:
            weekly_data = load_weekly_data(season_number, week_str)
            print(weekly_data)
            extracted_data = extract_data(weekly_data, cumulative_data, all_data)
            
            # Check if extracted_data is a DataFrame
            if isinstance(extracted_data, pd.DataFrame):
                df = extracted_data
            else:
                raise TypeError("extracted_data must be a Pandas DataFrame")
            
            # Append or concatenate the DataFrame to all_data
            all_data = pd.concat([all_data, df], ignore_index=True)

        except Exception as e:
            print(f"An error occurred while processing Week {week_str}: {e}")
            continue  # Skip to the next week if there's an error

    # Print DataFrame
    print("Extracted Data:")
    print(all_data)

    # Save DataFrame to CSV
    all_data.to_csv('extracted_data.csv', index=False)
    print("Data saved to 'extracted_data.csv'")


if __name__ == "__main__":
    main()
