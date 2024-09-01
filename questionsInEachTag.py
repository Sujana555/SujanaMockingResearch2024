import pandas as pd


def getTagsList(tags):
    if not isinstance(tags, str):  # Check if tags is a string
        return []

    firstBracket = tags.find("<")
    secondBracket = tags.find(">")
    tagsList = []
    count = tags.count("><") + 1
    i = 0

    while i < count:
        tagsList.append(tags[firstBracket + 1:secondBracket])
        firstBracket = tags.find("<", firstBracket + 1)
        secondBracket = tags.find(">", secondBracket + 1)
        i += 1

    return tagsList


def calculatingQuestionInEachTag(questionList):
    seenQuestionId = set()
    tagAndQuestionCountDict = {}

    listOfAllMockingTags = ["pytest-mock", "mockito", "jmock", "easymock", "mockk", "nock",
                            "unittest.mock", "moq", "nsubstitute", "fakeiteasy", "justmock",
                            "fakeit", "mockery", "gomock", "mockk", "cuckoo", "mockingbird", "googlemock"]

    for row in questionList:
        if row["questionId"] not in seenQuestionId:
            seenQuestionId.add(row["questionId"])
            questionTags = row["questionTags"]
            tagsList = getTagsList(questionTags)
            for tag in tagsList:
                tag_lower = tag.lower()
                if tag_lower in listOfAllMockingTags:
                    if tag_lower in tagAndQuestionCountDict:
                        tagAndQuestionCountDict[tag_lower] += 1
                    else:
                        tagAndQuestionCountDict[tag_lower] = 1

    return tagAndQuestionCountDict


# Load the CSV file into a DataFrame
question_df = pd.read_csv("allQuestions.csv")

# Convert the DataFrame into a list of dictionaries
questionList = question_df.to_dict(orient="records")

# Calculate the question count for each tag
tagsAndQuestionList = calculatingQuestionInEachTag(questionList)

# Print the results
for item in tagsAndQuestionList:
    print(item, ":", tagsAndQuestionList[item])