import os
import json
from typing import Dict, List, Optional, Union, cast


from sklearn.model_selection import  train_test_split

import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

import pandas as pd

import warnings
warnings.filterwarnings('ignore')



def basic_clean(string):
    '''
    This function takes in a string and
    returns the string normalized.
    '''

    string = unicodedata.normalize('NFKD', string)\
             .encode('ascii', 'ignore')\
             .decode('utf-8', 'ignore')
    string = re.sub(r"[^a-z0-9'\s]", '', string).lower()
    string = re.sub(r'[^\w\s]', '', string).lower()
    return string

def tokenize(string):
    '''
    This function takes in a string and
    returns a tokenized string.
    '''
    # Create tokenizer.
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    # Use tokenizer
    string = tokenizer.tokenize(string, return_str=True)
    
    return string

def stem(string):
    '''
    This function takes in a string and
    returns a string with words stemmed.
    '''
    # Create porter stemmer.
    ps = nltk.porter.PorterStemmer()
    
    # Use the stemmer to stem each word in the list of words we created by using split.
    stems = [ps.stem(word) for word in string.split()]
    
    # Join our lists of words into a string again and assign to a variable.
    string = ' '.join(stems)
    
    return string


def lemmatize(string):
    '''
    This function takes in string for and
    returns a string with words lemmatized.
    '''
    # Create the lemmatizer.
    wnl = nltk.stem.WordNetLemmatizer()
    
    # Use the lemmatizer on each word in the list of words we created by using split.
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    
    # This will Join our list of words into a string again and assign to a variable.
    string = ' '.join(lemmas)
    
    return string




def remove_stopwords(string, extra_words = [], exclude_words = []):
    '''
    This function takes in a string, optional extra_words and exclude_words parameters
    with default empty lists and returns a string.
    '''
    # Create stopword_list.
    stopword_list = stopwords.words('english')
    
    # Remove 'exclude_words' from stopword_list.
    stopword_list = set(stopword_list) - set(exclude_words)
    
    # Add in 'extra_words' to stopword_list.
    stopword_list = stopword_list.union(set(extra_words))
    
    # Split words in string.
    words = string.split()
    
    # Create a list of words from string with stopwords removed.
    filtered_words = [word for word in words if word not in stopword_list]
    
    # Join words in the list back into strings and assign to a variable.
    string_without_stopwords = ' '.join(filtered_words)
    
    return string_without_stopwords
    
    
    
    
def prep_nlp_data(df, nlp ,extra_words=[], exclude_words=[]):
    '''This function take in a df and the string name for a text column with 
    option to pass lists for extra_words and exclude_words and
    returns a df with the repo, language, readme_content, and new columns which are the 
    original columns which have been cleaned, tokenized, lemmatized and had the stopwords     removed. Also renames column repo as repo_name
    '''
    
    
    df[nlp + '_' + "cleaned"] = df[nlp].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(lemmatize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)

    return df


def get_sentiment_score(string, position=None):
    sia = SentimentIntensityAnalyzer()
    if position == 'positive':
        return sia.polarity_scores(string)['pos']
    elif position == 'negative':
        return sia.polarity_scores(string)['neg']
    elif position == 'neautral':
        return sia.polarity_scores(string)['neu']
    elif position == 'compound':
        return sia.polarity_scores(string)['compound']
    else:
        return sia.polarity_scores(string)
    

def prep_review_data(df):
    #drop duplicates
    df = df.drop_duplicates(keep='first')
    #split date of stay into 2 columns, month of stay and year of stay
    df[['month_of_stay', 'year_of_stay']] = df.date_of_stay.str.strip().str.split(' ', n = 1, expand=True)
    df = df.drop(columns='date_of_stay')
    #function does a basic clean, utilizing NFDK unicode and utf-8, tokenizes and lammentizes words. removes stop words, keeping negative stop words for sentiment analysis. 
    df = prep_nlp_data(df, 'review', extra_words =['wa'] , exclude_words=["haven't", "won't", "mightn't", 'not',"doesn't","needn't","shouldn't", 'no','none', "weren't", "couldn't","wasn't","wouldn't", "don't", "isn't","aren't","mustn't", "couldn't",])
    #Message Length and wordcounts for each read me
    df['message_length'] = df.review_cleaned.apply(len)
    df['word_count'] =  df.review_cleaned.str.split().apply(len)
    #Add sentiments as their own columns for each review
    df['positive_sentiment'] = df.review_cleaned.apply(get_sentiment_score, position='positive')
    df['negative_sentiment'] =  df.review_cleaned.apply(get_sentiment_score, position='negative')
    df['neatral_sentiment'] = df.review_cleaned.apply(get_sentiment_score, position='neautral')

    
    
    return df

def remove_outliers(df):
    postive_when_neg  = (df.positive_sentiment  >= .450) & (df.review_rating == 1)
    negative_when_pos = (df.negative_sentiment  >= .450) & (df.review_rating == 5)
    drop1=(df[postive_when_neg] == True).index.to_list()
    drop2=(df[negative_when_pos]== True).index.to_list()
    df = df.drop(drop1)
    df = df.drop(drop2)
    df = df.reset_index().drop(columns='index')
    
    return df


def split_for_model(df, target):
    '''
    This function take in the readme data acquired
    performs a split and stratifies language_cleaned column.
    Returns train, validate, and test dfs.
    '''
    train_validate, test = train_test_split(df, test_size=.2, 
                                        random_state=245, 
                                        stratify=df[target])
    train, validate = train_test_split(train_validate, test_size=.3, 
                                   random_state=245, 
                                   stratify=train_validate[target])
    print('{},{},{}'.format(train.shape,validate.shape,test.shape))
    return train, validate, test

