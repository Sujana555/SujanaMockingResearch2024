import pandas as pd
import csv
import re


def removeCodes(data):
    updatedMockingList = []

    for index, row in data.iterrows():
        question_body = row["questionBody"]  # Get the questionBody for cleaning

        # Check if question_body is NaN or not a string, if so, set it to an empty string
        if pd.isna(question_body):
            question_body = ""
        else:
            question_body = str(question_body)  # Convert to string to ensure it has the replace method

        # Remove content between <pre><code> and </code></pre>

        question_body = re.sub(r'<pre><code>.*?</code></pre>', '', question_body, flags=re.DOTALL)

        question_body = re.sub(r'<code>.*?</code>', '', question_body, flags=re.DOTALL)
        # Remove content between <ul> and </ul>
        question_body = re.sub(r'<ul>.*?</ul>', '', question_body, flags=re.DOTALL)

        # Remove content between <a> and </a>, allowing for any attributes in the <a> tag
        question_body = re.sub(r'<a.*?>.*?</a>', '', question_body, flags=re.DOTALL)

        # Append the cleaned data to the updatedMockingList
        updatedMockingList.append({
            "questionId": row["questionId"],
            "questionTitle": row["questionTitle"],
            "questionTags": row["questionTags"],  # Assuming you want to keep the original tags
            "questionBody": question_body.strip(),  # Cleaned questionBody
            # "questionVotes": row["questionVotes"],
            # "questionViewCount": row["questionViewCount"],
            # "questionCreationDate": row["questionCreationDate"],
            # "favoriteCount": row["favoriteCount"],
            # "answerCount": row["answerCount"],  # Assuming this exists in your data
            # "answerId": row["answerId"],  # Placeholder if you need to add answer data later
            # "answerUserId": row["answerUserId"],
            # "answerBody": row["answerBody"],
            # "answerVotes": row["answerScore"],
            # "commentId": row["commentId"],  # Placeholder for comment data
            # "commentText": row["commentText"]
        })

    return updatedMockingList


# Load the CSV file with dtype specification (adjust based on your CSV structure)
file_path = 'allQuestions.csv'
data = pd.read_csv(file_path, dtype=str)  # Load all data as strings to prevent DtypeWarning

# Strip leading/trailing spaces from column names
data.columns = data.columns.str.strip()

# Check if 'questionBody' exists after stripping spaces
if 'questionBody' not in data.columns:
    print("Error: 'questionBody' column not found.")
else:
    # Remove code blocks from the data
    cleaned_data = removeCodes(data)
    # Save cleaned data to CSV (add your save function here)


def saveDataToCsv(data, filename):
    if not data:
        print("Data list is empty. Nothing to write to CSV.")
        return

    keys = data[0].keys()  # Assuming data is not empty, get keys from the first dictionary
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            for entry in data:
                writer.writerow(entry)
        print(f"Data successfully saved to {filename}")
    except IOError as e:
        print(f"An I/O error occurred: {e}")


# Load the CSV file
file_path = 'allQuestions.csv'
data = pd.read_csv(file_path)

# Strip leading/trailing spaces from column names
data.columns = data.columns.str.strip()

# Check if 'questionBody' exists after stripping spaces
if 'questionBody' not in data.columns:
    print("Error: 'questionBody' column not found.")
else:
    # Remove code blocks from the data
    cleaned_data = removeCodes(data)
    # Save the cleaned data to CSV
    saveDataToCsv(cleaned_data, "updatedMockingDatasetWithoutCodes.csv")