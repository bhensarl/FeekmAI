# yfpy/main.py
from data_loader import load_weekly_data
from data_processor import extract_data
import pandas as pd


def main():
    season_number = "2023"
    week_number = '1'  # Example week number
    weekly_data = load_weekly_data(season_number, week_number)
    cumulative_data = {}  # Load or initialize as needed
    all_data = pd.DataFrame()  # Load or initialize as needed

    extracted_data = extract_data(weekly_data, cumulative_data, all_data)
    print(extracted_data)


if __name__ == "__main__":
    main()
