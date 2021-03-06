'''
Author: Abdel-Jaouad Aberkane (5783909), Utrecht University
Part of master's thesis "Exploring Ethics in Requirements Engineering", 
section 7: Automatically Identifying Ethical Issues

This script explores features extraction in requirements engineering aiming to raise ethical awareness
about the ethical implications of software. This script goes hand in hand with the user_stories.csv in the
/data folder.

The script is based on the following sources:
# https://towardsdatascience.com/multi-label-text-classification-with-scikit-learn-30714b7819c5
# https://www.analyticsvidhya.com/blog/2018/02/the-different-methods-deal-text-data-predictive-python/
# https://stackoverflow.com/questions/36572221/how-to-find-ngram-frequency-of-a-column-in-a-pandas-dataframe
'''

import re
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV 
from sklearn.metrics import confusion_matrix, recall_score, accuracy_score, precision_score

from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.lancaster import LancasterStemmer

from textblob import TextBlob, Word

stop_words = set(stopwords.words('english'))
ls = LancasterStemmer()
ps = PorterStemmer()

# substitute abbreviated words
def clean_text(text):
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'scuse", " excuse ", text)
    text = re.sub('\W', ' ', text)
    text = re.sub('[!@#$()[],]', '', text)
    text = text.strip(' ')
    return text

# Quantitative analysis of the data set
def reqs_per_label(df):
    # EXPLORE DATASET
    df_toxic = df.drop(['user_story'], axis=1)
    counts = []
    categories = list(df_toxic.columns.values)

    for i in categories:
        counts.append((i, df_toxic[i].sum()))

    df_stats = pd.DataFrame(counts, columns=['category', 'number_of_requirements'])
    # number of comments in each category
    print df_stats

    # number of comments in each category
    df_stats.plot(x='category', y='number_of_requirements', kind='bar', legend=False, grid=True, figsize=(8, 5))
    plt.title("Number of requirements per category")
    plt.ylabel('# of Occurrences', fontsize=12)
    plt.xlabel('category', fontsize=12)
    plt.show()


# Quantitative analysis of the data set: #labelled requirements
def req_distribution_label(df):
    # number of comments that are labeled
    print('Percentage of requirements that are not labelled:')
    print(len(df[(df['teaching_ethics']==0) & (df['responsibility']==0) & (df['privacy']==0) & (df['coe']== 0) & (df['ip']==0) & (df['edm']==0) & (df['security']==0) & (df['informed_consent']==0) & (df['autonomy']==0) & (df['quality']==0) & (df['piracy']==0) & (df['virtual_harm']==0)]) / float(len(df)))


# Quantitative analysis of the data set: number of words in reqs
def req_distribution_words(df):
    lens = df.user_story.str.len()
    lens.hist(bins = np.arange(0,5000,50))


# Quantitative analysis of the data set: identifying empty columns
def empty_reqs(df):
    print('Number of missing requirement:')
    df['user_story'].isnull().sum()


# Multinomial bayes classifier
def MNB_cl(X_train, X_test, train, test, categories):
    # Define a pipeline combining a text feature extractor with multi lable classifier
    NB_pipeline = Pipeline([
                    ('tfidf', TfidfVectorizer(stop_words=stop_words)),
                    ('clf', OneVsRestClassifier(MultinomialNB(
                        fit_prior=True, class_prior=None))),
                ])
    for category in categories:
        if(category == 'user_story'):
            continue
        print('... Processing {}'.format(category))
        # train the model using X_dtm & y
        NB_pipeline.fit(X_train, train[category])
        # compute the testing accuracy
        prediction = NB_pipeline.predict(X_test)

        cm = confusion_matrix(test[category], prediction)
        print(cm)
        print('Test accuracy is {}'.format(accuracy_score(test[category], prediction)))
        print('Recall is {}'.format(recall_score(test[category], prediction, average='macro')))
        print('Precision is {}'.format(precision_score(test[category], prediction, average='micro')))
        print("\n")


# Supported vector classifier
def SVC_cl(X_train, X_test, train, test):
    SVC_pipeline = Pipeline([
                ('tfidf', TfidfVectorizer(stop_words=stop_words)),
                ('clf', OneVsRestClassifier(LinearSVC(), n_jobs=1)),
            ])
    for category in categories:
        print('... Processing {}'.format(category))
        # train the model using X_dtm & y
        SVC_pipeline.fit(X_train, train[category])
        # compute the testing accuracy
        prediction = SVC_pipeline.predict(X_test)
        print('Test accuracy is {}'.format(accuracy_score(test[category], prediction)))


# Linear regression
def LR_cl(X_train, X_test, train, test):
    LogReg_pipeline = Pipeline([
                ('tfidf', TfidfVectorizer(stop_words=stop_words)),
                ('clf', OneVsRestClassifier(LogisticRegression(solver='sag'), n_jobs=1)),
            ])
    for category in categories:
        print('... Processing {}'.format(category))
        # train the model using X_dtm & y
        LogReg_pipeline.fit(X_train, train[category])
        # compute the testing accuracy
        prediction = LogReg_pipeline.predict(X_test)
        print('Accuracy is {}'.format(accuracy_score(test[category], prediction)))


# Pipeline of the MNB
def init_pipeline(df):
    # Split the data to train and test sets
    #categories = ['teaching_ethics', 'responsibility', 'privacy', 'coe', 'ip', 'edm', 'security', 'informed_consent', 'autonomy', 'quality', 'piracy', 'virtual_harm']
    
    categories = list(df.columns.values)
    train, test = train_test_split(df, random_state=42, test_size=0.33, shuffle=True)
    X_train = train.user_story
    X_test = test.user_story
    #print(X_train.shape)
    #print(X_test.shape)

    MNB_cl(X_train, X_test, train, test, categories)


# Convert all values of dataframe to integers
def df_float2int(df):
    df[['teaching_ethics', 'responsibility', 'privacy', 'coe', 'ip', 'edm', 'security', 'informed_consent', 'autonomy', 'quality', 'piracy', 'virtual_harm']] = df[['teaching_ethics', 'responsibility', 'privacy', 'coe', 'ip', 'edm', 'security', 'informed_consent', 'autonomy', 'quality', 'piracy', 'virtual_harm']].astype('int')
    return df

# Basic processing: average word length
def average_word_length_s(sentence):
    words = sentence.split()
    return (sum(len(word) for word in words)/len(words))  

# Basic processing: number of words
def number_of_words(df):
    print("# WORD COUNT")
    word_count_res_1 = df.loc[df['responsibility'] == 1]['user_story'].apply(lambda x: len(str(x).split(" ")))
    word_count_res_0 = df.loc[df['responsibility'] == 0]['user_story'].apply(lambda x: len(str(x).split(" ")))
    print("Responsibility - mean labelled: {0}, mean unlabelled: {1}".format(word_count_res_1.mean(), word_count_res_0.mean()))

    word_count_pri_1 = df.loc[df['privacy'] == 1]['user_story'].apply(lambda x: len(str(x).split(" ")))
    word_count_pri_0 = df.loc[df['privacy'] == 0]['user_story'].apply(lambda x: len(str(x).split(" ")))
    print("Privacy - mean labelled: {0}, mean unlabelled: {1}".format(word_count_pri_1.mean(), word_count_pri_0.mean()))

    word_count_sec_1 = df.loc[df['security'] == 1]['user_story'].apply(lambda x: len(str(x).split(" ")))
    word_count_sec_0 = df.loc[df['security'] == 0]['user_story'].apply(lambda x: len(str(x).split(" ")))
    print("Security - mean labelled: {0}, mean unlabelled: {1}".format( word_count_sec_1.mean(), word_count_sec_0.mean()))
    #df[['user_story','word_count']].head()
    print "\n"


# Basic processing: number of characters in labelled and unlabelled reqs
def number_of_chars(df):
    print("# CHAR COUNT")
    #df['char_count'] = df['user_story'].str.len() ## this also includes spaces
    #df[['user_story','char_count']].head()

    char_count_res_1 = df.loc[df['responsibility'] == 1]['user_story'].str.len()
    char_count_res_0 = df.loc[df['responsibility'] == 0]['user_story'].str.len()
    print("Responsibility - mean labelled: {0}, mean unlabelled: {1}".format(char_count_res_1.mean(), char_count_res_0.mean()))

    char_count_pri_1 = df.loc[df['privacy'] == 1]['user_story'].str.len()
    char_count_pri_0 = df.loc[df['privacy'] == 0]['user_story'].str.len()
    print("Privacy - mean labelled: {0}, mean unlabelled: {1}".format(char_count_pri_1.mean(), char_count_pri_0.mean()))

    char_count_sec_1 = df.loc[df['security'] == 1]['user_story'].str.len()
    char_count_sec_0 = df.loc[df['security'] == 0]['user_story'].str.len()
    print("Security - mean labelled: {0}, mean unlabelled: {1}".format(char_count_sec_1.mean(), char_count_sec_0.mean()))
    print "\n"


# Basic processing: average word length in labelled and unlabelled reqs
def average_word_length(df):
    print("# AVERAGE WORD LENGTH")
    word_length_res_1 = df.loc[df['responsibility'] == 1]['user_story'].apply(lambda x: average_word_length_s(x))
    word_length_res_0 = df.loc[df['responsibility'] == 0]['user_story'].apply(lambda x: average_word_length_s(x))
    print("Responsibility - mean labelled: {0}, mean unlabelled: {1}".format(word_length_res_1.mean(), word_length_res_0.mean()))

    word_length_pri_1 = df.loc[df['privacy'] == 1]['user_story'].apply(lambda x: average_word_length_s(x))
    word_length_pri_0 = df.loc[df['privacy'] == 0]['user_story'].apply(lambda x: average_word_length_s(x))
    print("Privacy - mean labelled: {0}, mean unlabelled: {1}".format(word_length_res_1.mean(), word_length_res_0.mean()))

    word_length_sec_1 = df.loc[df['security'] == 1]['user_story'].apply(lambda x: average_word_length_s(x))
    word_length_sec_0 = df.loc[df['security'] == 0]['user_story'].apply(lambda x: average_word_length_s(x))
    print("Security - mean labelled: {0}, mean unlabelled: {1}".format(word_length_sec_1.mean(), word_length_sec_0.mean()))
    print "\n"


# Basic processing: number of stopwords in labelled and unlabelled reqs
def number_of_stopwords(df):
    print("# STOPWORDS COUNT")
    stopwords_count_res_1 = df.loc[df['responsibility'] == 1]['user_story'].apply(lambda x: len([x for x in x.split() if x in stop_words]))
    stopwords_count_res_0 = df.loc[df['responsibility'] == 0]['user_story'].apply(lambda x: len([x for x in x.split() if x in stop_words]))
    print("Responsibility - mean labelled: {0}, mean unlabelled: {1}".format(stopwords_count_res_1.mean(), stopwords_count_res_0.mean()))

    stopwords_count_pri_1 = df.loc[df['privacy'] == 1]['user_story'].apply(lambda x: len([x for x in x.split() if x in stop_words]))
    stopwords_count_pri_0 = df.loc[df['privacy'] == 0]['user_story'].apply(lambda x: len([x for x in x.split() if x in stop_words]))
    print("Privacy - mean labelled: {0}, mean unlabelled: {1}".format(stopwords_count_pri_1.mean(), stopwords_count_pri_0.mean()))

    stopwords_count_sec_1 = df.loc[df['security'] == 1]['user_story'].apply(lambda x: len([x for x in x.split() if x in stop_words]))
    stopwords_count_sec_0 = df.loc[df['security'] == 0]['user_story'].apply(lambda x: len([x for x in x.split() if x in stop_words]))
    print("Security - mean labelled: {0}, mean unlabelled: {1}".format(stopwords_count_sec_1.mean(), stopwords_count_sec_0.mean()))
    print "\n"


# Preprocessing for bigram computation
def bigram_column(us):
    word_vectorizer = CountVectorizer(ngram_range=(2,2), analyzer='word')
    sparse_matrix = word_vectorizer.fit_transform(us)
    frequencies = sum(sparse_matrix).toarray()[0]
    return pd.DataFrame(frequencies, index=word_vectorizer.get_feature_names(), columns=['frequency'])


# Basic processing: bigrams of labelled and unlabelled reqs
def get_bigrams(df):
    print("# BIGRAM COUNT")
    us_res_1 = df.loc[df['responsibility'] == 1]['user_story']
    us_res_0 = df.loc[df['responsibility'] == 0]['user_story']

    us_pri_1 = df.loc[df['privacy'] == 1]['user_story']
    us_pri_0 = df.loc[df['privacy'] == 0]['user_story']

    us_sec_1 = df.loc[df['security'] == 1]['user_story']
    us_sec_0 = df.loc[df['security'] == 0]['user_story']

    us_res_1_bi = bigram_column(us_res_1)
    us_res_0_bi = bigram_column(us_res_0)

    us_pri_1_bi = bigram_column(us_pri_1)
    us_pri_1_bi = bigram_column(us_pri_0)

    us_sec_1_bi = bigram_column(us_sec_1)
    us_sec_1_bi = bigram_column(us_sec_0)


    print bigram_column(us_res_1).sort_values(by='frequency', ascending=0).head(10)
    print bigram_column(us_res_0).sort_values(by='frequency', ascending=0).head(10)

    print bigram_column(us_pri_1).sort_values(by='frequency', ascending=0).head(10)
    print bigram_column(us_pri_0).sort_values(by='frequency', ascending=0).head(10)

    print bigram_column(us_sec_1).sort_values(by='frequency', ascending=0).head(10)
    print bigram_column(us_sec_0).sort_values(by='frequency', ascending=0).head(10)

    print "\n"


# Basic processing: tfidf of labelled and unlabelled reqs
def get_tfidf_per_label(df, categories):
    print("# TFIDF PER LABEL")
    tfidf = TfidfVectorizer()

    for label_index in range(0, len(categories)):
        print "Label: " + categories[label_index]
        class1 = df.loc[df[categories[label_index]] == 1]['user_story']
        feature_matrix_c1 = tfidf.fit_transform(class1)
        weights = np.asarray(feature_matrix_c1.mean(axis=0)).ravel().tolist()
        weights_df = pd.DataFrame({'term': tfidf.get_feature_names(), 'weight': weights})
        print "class = 1"
        print weights_df.sort_values(by='weight', ascending=False).head(20)

        class0 = df.loc[df[categories[label_index]] == 0]['user_story']
        feature_matrix_c0 = tfidf.fit_transform(class0)
        weights = np.asarray(feature_matrix_c0.mean(axis=0)).ravel().tolist()
        weights_df = pd.DataFrame({'term': tfidf.get_feature_names(), 'weight': weights})
        print "class = 0"
        print weights_df.sort_values(by='weight', ascending=False).head(20)
        print "\n"


if __name__ == "__main__":
    # READ DATASET
    df = pd.read_csv("data/user_stories.csv", sep=';', encoding = "utf8")
    #df = pd.read_csv("data/user_stories_s.csv", sep=';', encoding = "utf8")


    df = df.fillna(0)

    # clean text
    df['user_story'] = df['user_story'].map(lambda com : clean_text(com))

    # text stemming
    #df['user_story'] = df['user_story'].map(lambda com : stem_text(com))    

    df = df_float2int(df)

    df = df.drop(['teaching_ethics', 'coe', 'ip', 'edm', 'autonomy', 'piracy', 'informed_consent', 'quality', 'virtual_harm'], axis=1)

    categories = list(df.columns.values)

    categories = categories[1:len(categories)]
    init_pipeline(df)
    #exit(0)

	
#### Basic feature extraction
    ## 1.1 Number of Words
    number_of_words(df)

    ## 1.2 Number of characters
    number_of_chars(df)

    ## 1.3 Average word length
    average_word_length(df)

    ## 1.4 Number of stopwords
    number_of_stopwords(df)

#### Basic pre-processing
    ## 2.1 Lower case
    df['user_story'] = df['user_story'].apply(lambda x: " ".join(x.lower() for x in x.split()))

    ## 2.2 Removing punctuation
    df['user_story'] = df['user_story'].str.replace('[^\w\s]','')

    ## 2.3 Removing stopwords
    df['user_story'] = df['user_story'].apply(lambda x: " ".join(x for x in x.split() if x not in stop_words))

    ## 2. Removing digits
    df['user_story'] = df['user_story'].apply(lambda x: ''.join([x for x in x if not x.isdigit()]))


    ## 2.4 Common word (removal)
    pd.Series(' '.join(df['user_story']).split()).value_counts()[:10]
    # uncommon words
    pd.Series(' '.join(df['user_story']).split()).value_counts()[-10:]

    ## 2.5 Tokenization

    ## 2.6 Stemming
    user_story_stemmed = df['user_story'].apply(lambda x: " ".join([ps.stem(word) for word in x.split()]))

    ## 2.7 Lemmatization
    user_story_lemmatized = df['user_story'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
    df['user_story'] = df['user_story'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

    # remove stopwords again since corpus is now lematized
    # first lemmatize the added stopwords
    stop_words.add(Word("user").lemmatize())
    stop_words.add(Word("want").lemmatize())
    stop_words.add(Word("able").lemmatize())
    stop_words.add(Word("would").lemmatize())
    stop_words.add(Word("like").lemmatize())
    stop_words.add(Word("need").lemmatize())

    # filter out stopwords
    df['user_story'] = df['user_story'].apply(lambda x: " ".join(x for x in x.split() if x not in stop_words))

#### Advanced text processing
    ## 3.1 Bigrams
    get_bigrams(df)

    ## 3.2 Inverse Document Frequency
    get_tfidf_per_label(df, categories)

    tfidf = TfidfVectorizer()
    #feature_matrix = tfidf.fit_transform(df['user_story'])
    #feature_matrix_full = tfidf.fit_transform(df)

    # all words in the tf-idf vocabulary 
    #features = tfidf.get_feature_names()

    #weights = np.asarray(feature_matrix.mean(axis=0)).ravel().tolist()
    #weights_df = pd.DataFrame({'term': tfidf.get_feature_names(), 'weight': weights})
    #weights_df.sort_values(by='weight', ascending=False).head(20)
