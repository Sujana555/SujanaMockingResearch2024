
import nltk
import re
import numpy as np
import pandas as pd
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import spacy
import matplotlib.pyplot as plt
import csv
from nltk.corpus import stopwords

# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

# Suppress warnings - optional
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Stop words
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])


# Import Dataset
csv_file_path = "updatedMockingDatasetWithoutCodes.csv"
df = pd.read_csv(csv_file_path)

# Print column names to debug issues
print("Column names:", df.columns)

# Check if the 'questionId' column exists
if 'questionId' in df.columns:
    # Process data: Combine question body and title into a single column
    df['questionBody'] = df['questionBody'].astype(str).fillna('')
    df['questionTitle'] = df['questionTitle'].astype(str).fillna('')
    df['combinedText'] = df['questionBody'] + ' ' + df['questionTitle']

    # Create a dictionary to store combined Text and questionId
    tempQuesDataset = {
        "questionId": df["questionId"].tolist(),
        "combinedText": df["combinedText"].tolist()
    }

    # Convert dictionary to DataFrame
    temp_df = pd.DataFrame(tempQuesDataset)

    # Define the file path where you want to save the CSV
    output_csv_file_path = "tempQuesDataset.csv"

    # Save DataFrame to CSV file
    temp_df.to_csv(output_csv_file_path, index=False)

    print(f"Data saved to {output_csv_file_path}.")
else:
    print("The 'questionId' column does not exist in the DataFrame.")

# Convert 'combinedText' column to a list of dictionaries
data = df[["combinedText"]].to_dict(orient='records')

# Function to clean text: remove emails, new lines, and single quotes
def preprocess_text(text):
    if text:
        text = re.sub(r'\S*@\S*\s?', '', text)  # Remove emails
        text = re.sub(r'\s+', ' ', text)  # Replace new lines and extra spaces
        text = re.sub(r"'", "", text)  # Remove single quotes
    return text

# Apply text preprocessing to the data
for item in data:
    item['combinedText'] = preprocess_text(item['combinedText'])

# Function to tokenize and clean up text
def sent_to_words(sentences):
    for sentence in sentences:
        if sentence:  # Check if sentence is not None or empty
            yield gensim.utils.simple_preprocess(str(sentence), deacc=True)

# Tokenize the data
data_words = list(sent_to_words([item['combinedText'] for item in data]))
print("Data words (sample):", data_words[:1])

# Create Bigram and Trigram Models
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
trigram = gensim.models.Phrases(bigram[data_words], threshold=100)
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)
print(trigram_mod[bigram_mod[data_words[0]]])

# Functions to remove stopwords, make bigrams, and lemmatize text
def remove_stopwords(texts):
    return [[word for word in doc if word not in stop_words] for doc in texts if doc]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts if doc]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts if doc]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    texts_out = []
    for sent in texts:
        if sent:
            doc = nlp(" ".join(sent))
            texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

# Process text: remove stopwords, make bigrams, and lemmatize
data_words_nostops = remove_stopwords(data_words)
data_words_bigrams = make_bigrams(data_words_nostops)
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
print(data_lemmatized[:1])

# Create dictionary and corpus for LDA model
id2word = corpora.Dictionary(data_lemmatized)
corpus = [id2word.doc2bow(text) for text in data_lemmatized]
print(corpus[:1])

# Set up LDA Mallet model
mallet_path = '/home/student/suhisi/Desktop/Mallet-202108/bin/mallet'
ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=10, id2word=id2word)
print(ldamallet.show_topics(formatted=False))

# Calculate coherence score for the model
coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
coherence_ldamallet = coherence_model_ldamallet.get_coherence()
print('\nCoherence Score: ', coherence_ldamallet)

# Function to compute coherence values for various numbers of topics
def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=2):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics
    start : Starting number of topics
    step : Step size for number of topics

    Returns:
    -------
    num_topics_range : List of numbers of topics
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    num_topics_range = range(start, limit, step)  # Range of topics to evaluate

    for num_topics in num_topics_range:
        try:
            print(f"Training LDA model with {num_topics} topics...")
            model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=dictionary)
            coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
            coherence_value = coherencemodel.get_coherence()
            coherence_values.append(coherence_value)
            print(f"Coherence score for {num_topics} topics: {coherence_value}")
        except Exception as e:
            print(f"Error for {num_topics} topics: {e}")
            coherence_values.append(None)  # Handle errors

    return num_topics_range, coherence_values

# Compute coherence values
num_topics_range, coherence_values = compute_coherence_values(dictionary=id2word, corpus=corpus, texts=data_lemmatized, start=2, limit=50, step=6)

# Convert range to list to match coherence_values length
x = list(num_topics_range)

# Debugging output
print("x values:", x)
print("coherence values:", coherence_values)

# Ensure that the length of x matches the length of coherence_values
if len(x) != len(coherence_values):
    raise ValueError(f"Mismatch in dimensions: x has length {len(x)}, coherence_values has length {len(coherence_values)}")

# Plot coherence values
plt.figure(figsize=(10, 6))  # Set figure size
plt.plot(x, coherence_values, marker='o', linestyle='-', color='b')
plt.xlabel("Num Topics")
plt.ylabel("Coherence Score")
plt.title("Coherence Scores for Various Numbers of Topics")
plt.legend(["Coherence Values"], loc='best')

# Save the plot as PNG and PDF files
plt.savefig("coherence_plot_50.png")
plt.savefig("coherence_plot_50.pdf")

# Display the plot
plt.show()


# Function to format topics with their dominant sentences and keywords, including additional fields
def format_topics_sentences(ldamodel, corpus, texts, original_df):
    """
    Get the dominant topic, percent contribution, keywords, and original fields for each document.

    Parameters:
    ----------
    ldamodel : LDA model
    corpus : Gensim corpus
    texts : List of input texts
    original_df : Original DataFrame with 'questionId', 'questionTitle', and 'questionBody'

    Returns:
    -------
    sent_topics_df : DataFrame with dominant topic, percent contribution, topic keywords, questionId, questionTitle, questionBody, and combinedText
    """
    sent_topics_df = []

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # Dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])

                # Retrieve corresponding original fields
                question_id = original_df.iloc[i]['questionId']
                question_title = original_df.iloc[i]['questionTitle']
                question_body = original_df.iloc[i]['questionBody']

                sent_topics_df.append([
                    int(topic_num),
                    round(prop_topic, 4),
                    topic_keywords,
                    question_id,
                    question_title,
                    question_body,
                    texts[i]
                ])
            else:
                break

    # Convert list to DataFrame
    sent_topics_df = pd.DataFrame(sent_topics_df, columns=[
        'Dominant_Topic',
        'Perc_Contribution',
        'Topic_Keywords',
        'questionId',
        'questionTitle',
        'questionBody',
        'combinedText'
    ])
    return sent_topics_df


# Format topics and sentences
df_topic_sents_keywords = format_topics_sentences(
    ldamodel=ldamallet,
    corpus=corpus,
    texts=[item['combinedText'] for item in data],
    original_df=df
)

# Format DataFrame
df_dominant_topic = df_topic_sents_keywords.reset_index()
df_dominant_topic.columns = [
    'Document_No',
    'Dominant_Topic',
    'Topic_Perc_Contrib',
    'Keywords',
    'questionId',
    'questionTitle',
    'questionBody',
    'combinedText'
]

# Display the top 10 rows
print(df_dominant_topic.head(10))

# Group top 5 sentences under each topic
sent_topics_sorteddf_mallet = pd.DataFrame()
sent_topics_outdf_grpd = df_topic_sents_keywords.groupby('Dominant_Topic')

for i, grp in sent_topics_outdf_grpd:
    sent_topics_sorteddf_mallet = pd.concat([
        sent_topics_sorteddf_mallet,
        grp.sort_values(['Perc_Contribution'], ascending=[0]).head(5)
    ], axis=0)

# Reset Index and Format
sent_topics_sorteddf_mallet.reset_index(drop=True, inplace=True)
sent_topics_sorteddf_mallet.columns = [
    'Topic_Num',
    'Topic_Perc_Contrib',
    'Keywords',
    'questionId',
    'questionTitle',
    'questionBody',
    'combinedText'
]
print(sent_topics_sorteddf_mallet.head())


# Function to save topic-related questions to CSV files, including additional fields
def save_topic_questions(df_topic_sents_keywords):
    """
    Save questions related to each topic into separate CSV files with questionId, questionTitle, questionBody, and combinedText.

    Parameters:
    ----------
    df_topic_sents_keywords : DataFrame with dominant topic, questionId, questionTitle, questionBody, and combinedText information
    """
    # Group by dominant topic
    grouped_topics = df_topic_sents_keywords.groupby('Dominant_Topic')

    for topic_num, group in grouped_topics:
        file_name = f'topic_{topic_num}.csv'
        group[['questionId', 'questionTitle', 'questionBody', 'combinedText']].to_csv(file_name, index=False, header=[
            'questionId', 'questionTitle', 'questionBody', 'combinedText'
        ])
        print(f'Saved {len(group)} documents for Topic {topic_num} to {file_name}')


# Execute the saving function
save_topic_questions(df_topic_sents_keywords)