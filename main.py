# yfpy/main.py
from yfpy.data_loader import load_weekly_data
from yfpy.data_processor import extract_data
import pandas as pd


def main():
    week_number = '1'  # Example week number
    weekly_data = load_weekly_data(week_number)
    cumulative_data = {}  # Load or initialize as needed
    all_data = pd.DataFrame()  # Load or initialize as needed

    extracted_data = extract_data(weekly_data, cumulative_data, all_data)
    print(extracted_data)


if __name__ == "__main__":
    main()