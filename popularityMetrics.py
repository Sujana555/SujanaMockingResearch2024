import pandas as pd

def calculatePopularityAllMockingAnswers(allMockingData, allAnswerData):
    allMockingAnswerPopularityFactors = getMockingAnswersPopularityFactors(allMockingData)
    allAnswersPopularityFactors = getAllAnswersPopularityFactors(allAnswerData)
    normalizedAllMockingAnswerPopularityFactors = normalizePopularityFactors(allMockingAnswerPopularityFactors,
                                                                           allAnswersPopularityFactors)
    score = normalizedAllMockingAnswerPopularityFactors[0]
    commentCount = normalizedAllMockingAnswerPopularityFactors[1]
    popularity = (score + commentCount) / 2

    print(f'''All Mocking Answer Popularity Factors:  
    Score: {score:.2f}
    Comment Count: {commentCount:.2f}
    Popularity: {popularity:.2f}\n''')
    allScores = allAnswersPopularityFactors[0]
    allCommentCounts = allAnswersPopularityFactors[1]
    return allScores, allCommentCounts


def getMockingAnswersPopularityFactors(mockingData):
    score = calculatePopularityFactorAvg('answerScore', mockingData, 'answerId')
    commentCount = calculatePopularityFactorAvg('commentCount', mockingData, 'answerId')
    return score, commentCount


def getAllAnswersPopularityFactors(allAnswersData):
    score = calculatePopularityFactorAvg('Score', allAnswersData, 'Id')
    commentCount = calculatePopularityFactorAvg('CommentCount', allAnswersData, 'Id')
    return score, commentCount


def calculatePopularityAllMockingQuestions(allMockingData, allQuestionData):
    allMockingPopularityFactors = getMockingQuestionsPopularityFactors(allMockingData)
    allQuestionsPopularityFactors = getAllQuestionsPopularityFactors(allQuestionData)
    normalizedAllMockingPopularityFactors = normalizePopularityFactors(allMockingPopularityFactors,
                                                                     allQuestionsPopularityFactors)
    score = normalizedAllMockingPopularityFactors[0]
    answerCount = normalizedAllMockingPopularityFactors[1]
    commentCount = normalizedAllMockingPopularityFactors[2]
    viewCount = normalizedAllMockingPopularityFactors[3]
    popularity = (score + answerCount + commentCount + viewCount) / 4
    print(f''' All Mocking  Questions Popularity Factors:   
    Score: {score:.2f}
    Answer Count: {answerCount:.2f}
    Comment Count: {commentCount:.2f} 
    View Count: {viewCount:.2f}
    Popularity: {popularity:.2f}\n''')
    allScores = allQuestionsPopularityFactors[0]
    allAnswerCounts = allQuestionsPopularityFactors[1]
    allCommentCounts = allQuestionsPopularityFactors[2]
    allViewCounts = allQuestionsPopularityFactors[3]
    return allScores, allAnswerCounts, allCommentCounts, allViewCounts


def getMockingQuestionsPopularityFactors(mockingData):
    score = calculatePopularityFactorAvg('Score', mockingData, 'questionId')
    answerCount = calculatePopularityFactorAvg('answerCount', mockingData, 'questionId')
    commentCount = calculatePopularityFactorAvg('quesCommentCount', mockingData, 'questionId')
    viewCount = calculatePopularityFactorAvg('quesViewCount', mockingData, 'questionId')
    return score, answerCount, commentCount, viewCount


def getAllQuestionsPopularityFactors(allQuestionsData):
    score = calculatePopularityFactorAvg('Score', allQuestionsData, 'Id')
    answerCount = calculatePopularityFactorAvg('AnswerCount', allQuestionsData, 'Id')
    commentCount = calculatePopularityFactorAvg('CommentCount', allQuestionsData, 'Id')
    viewCount = calculatePopularityFactorAvg('viewCount', allQuestionsData, 'Id')
    return score, answerCount, commentCount, viewCount



def calculatePopularityFactorAvg(popularityFactor, dataframe, idLabel):
    popularityFactorTotal = 0
    questionIdsSeenSet = set()
    totalNumUniqueQuestions = 0
    for index, row in dataframe.iterrows():
        questionId = row[idLabel]
        if ((questionId is not None) and
                (questionId not in questionIdsSeenSet) and
                (not pd.isna(row[popularityFactor]))):
            popularityFactorCount = row[popularityFactor]
            popularityFactorTotal += popularityFactorCount
            totalNumUniqueQuestions += 1
            questionIdsSeenSet.add(questionId)
    # I don't think this is necessary, but I'm keeping it in case it is
    # because even if 0 questions are found, the popularity factor should be 0 so no division by 0 error
    if totalNumUniqueQuestions == 0:
        return 0
    # return the average popularity factor
    # This is NOT normalizing the factor, it is just the average
    return popularityFactorTotal / totalNumUniqueQuestions


def normalizePopularityFactors(popularityFactors, allPopularityFactors):
    normalizedPopularityFactors = []
    for i in range(len(popularityFactors)):
        normalizedPopularityFactors.append(normalizePopularityFactor(popularityFactors[i], allPopularityFactors[i]))
    return normalizedPopularityFactors


def normalizePopularityFactor(popularityFactor, allPopularityFactor):
    return popularityFactor / allPopularityFactor

allMockingQuestionDataset = pd.read_csv("All_Mocking_Question_Data.csv")
alMockingAnswerDataset = pd.read_csv("All_Mocking_Answer_Data.csv")
allQuestionData = pd.read_csv("AllStackOverflowQuestionDataset.csv")
allAnswerData = pd.read_csv("AllStackOverflowAnswerDataset.csv")
allPopularityFactorsQuestions = calculatePopularityAllMockingQuestions(allMockingQuestionDataset, allQuestionData)
allPopularityFactorsAnswers = calculatePopularityAllMockingAnswers(alMockingAnswerDataset, allAnswerData)


