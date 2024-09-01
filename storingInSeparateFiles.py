import csv

def readCsvFile(fileName):
    try:
        with open(fileName, mode='r', encoding='utf-8') as file:
            csvFile = csv.DictReader(file)
            return list(csvFile)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {fileName} not found.")
    except Exception as e:
        raise e

def storeQuestions(baseFile):
    questionsList = []
    seenQuestionsIds = set()
    for row in baseFile:
        if row['questionId'] not in seenQuestionsIds:
            questionsList.append({
                'questionId': row['questionId'],
                'questionTitle': row['questionTitle'],
                'questionTags': row['Tags'],
                'questionBody': row['questionBody'],
                'questionVotes': row['questionScore'],
                'questionViewCount': row['questionViewCount'],
                'questionCreationDate': row['questionCreationDate'],
                'favoriteCount': row['questionFavoriteCount'],
                'answerCount': row['AnswerCount'],
                "questionCommentCount": row["questionCommentCount"]
            })
            seenQuestionsIds.add(row['questionId'])
    return questionsList

def storeAnswers(baseFile):
    answerList = []
    seenAnswerIds = set()
    for row in baseFile:
        if row["answerId"] and row['answerId'] not in seenAnswerIds:
            seenAnswerIds.add(row['answerId'])
            answerList.append({
                'questionId': row['questionId'],
                'answerCount': row['AnswerCount'],
                'answerId': row['answerId'],
                'answerUserId': row['answerUserId'],
                'answerBody': row['answerBody'],
                'answerVotes': row['answerScore'],
                "answerCommentCount": row["answerCommentCount"],
            })
    return answerList

def storeComments(baseFile):
    commentList = []
    seenCommentIds = set()
    for row in baseFile:
        if row["commentId"] and row['commentId'] not in seenCommentIds:
            seenCommentIds.add(row['commentId'])
            commentList.append({
                'questionId': row['questionId'],
                'answerId': row['answerId'],
                'commentId': row['commentId'],
                'commentText': row['commentText']
            })
    return commentList

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

# try:
#     baseFile = readCsvFile("Mocking_DataSet.csv")
#     if not baseFile:
#         print("The base file is empty or could not be read.")
#     else:
#         questionList = storeQuestions(baseFile)
#         answerList = storeAnswers(baseFile)
#         commentList = storeComments(baseFile)
#
#         saveDataToCsv(questionList, "questionList.csv")
#         saveDataToCsv(answerList, "answerList.csv")
#         saveDataToCsv(commentList, "commentList.csv")
# except Exception as e:
#     print(f"An error occurred: {e}")

baseFile = readCsvFile("MockingDataset(Main).csv")

questionList = storeQuestions(baseFile)
answerList = storeAnswers(baseFile)
commentList = storeComments(baseFile)

saveDataToCsv(questionList, "allQuestions.csv")
saveDataToCsv(answerList, "allAnswers.csv")
saveDataToCsv(commentList, "allComments.csv")
