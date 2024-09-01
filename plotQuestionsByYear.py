import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def convert_date(date):
    try:
        # Attempt to convert without specifying a format
        date_stamp = pd.to_datetime(date, errors='coerce')

        if pd.isna(date_stamp):
            return None  # Return None if conversion fails
        return date_stamp.strftime("%m/%d/%Y %H:%M")
    except Exception as e:
        print(f"Error converting date {date}: {e}")
        return None  # Return None on any exception


def plot_questions_per_yr(data_robot: pd.DataFrame, output_file: str) -> dict:
    year_count_dict = get_year_counts(data_robot)
    plot_data(year_count_dict)

    yearly_counts = list(year_count_dict.values())
    total_robot_questions = sum(yearly_counts)
    add_annotations(year_count_dict, total_robot_questions)

    plt.tight_layout(pad=3.0)

    # Save the plot as a PDF file
    plt.savefig(output_file, format='pdf', bbox_inches='tight')
    plt.show()

    return year_count_dict


def get_year_counts(data_robot: pd.DataFrame) -> dict:
    question_ids_seen = set()
    year_count_dict = {}

    for index, row in data_robot.iterrows():
        year_count_dict = process_row(row, question_ids_seen, year_count_dict)

    return year_count_dict


def process_row(row: pd.Series, question_ids_seen: set, year_count_dict: dict) -> dict:
    question_id = row["questionId"]
    question_creation_date = row["questionCreationDate"]

    if question_id not in question_ids_seen:
        try:
            date_stamp = pd.to_datetime(question_creation_date, format="%m/%d/%Y %H:%M")
        except:
            try:
                date_stamp = pd.to_datetime(question_creation_date, format="%Y-%m-%d %H:%M:%S")
            except:
                base_date = datetime(1899, 12, 30)
                date_stamp = base_date + timedelta(days=float(question_creation_date))

        if pd.isna(date_stamp):  # Check for NaT after conversion
            return year_count_dict  # Skip if date is NaT

        year = date_stamp.year

        if year in year_count_dict:
            year_count_dict[year] += 1
        else:
            year_count_dict[year] = 1

        question_ids_seen.add(question_id)

    return year_count_dict


def add_annotations(year_count_dict: dict, total_robot_questions: int) -> None:
    for year, count in year_count_dict.items():
        plt.text(year, count, str(count), ha='center', va='bottom', fontsize=12)

    x_coord_total = max(year_count_dict.keys())
    y_coord_total = max(year_count_dict.values())
    plt.text(x_coord_total, y_coord_total, f'Total: {total_robot_questions}', ha='left', fontsize=12, weight='bold')


def plot_data(year_count_dict: dict) -> None:
    plt.figure(figsize=(12, 8))
    plt.bar(year_count_dict.keys(), year_count_dict.values(), label="Mocking questions on Stack Overflow by year")
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Number of mocking questions asked", fontsize=14)
    plt.title("Mocking Questions on Stack Overflow by Year", fontsize=16)
    plt.xticks(list(year_count_dict.keys()), rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=12)


# Load the CSV file
file_path = 'All_Mocking_Question_Data.csv'
data = pd.read_csv(file_path)

# Apply the conversion function to the 'questionCreationDate' column
data['questionCreationDate'] = data['questionCreationDate'].apply(convert_date)

# Call the function and specify the output PDF file name
output_pdf_file = 'mocking_questions_per_year.pdf'
plot_questions_per_yr(data, output_pdf_file)
