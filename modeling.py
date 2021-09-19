from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.dummy import DummyClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
import prepare

from sklearn.feature_extraction.text import TfidfVectorizer

import pandas as pd
import numpy as np
from sklearn.metrics import classification_report,confusion_matrix,recall_score, precision_score, accuracy_score
import warnings
warnings.filterwarnings('ignore')


def xy_split(X, y):
    '''
    This function take in the data acquired and 
    performs a split and stratifies target variable column.
    Returns train, validate, and test dfs.
    '''
    X_train_validate, X_test, y_train_validate, y_test = train_test_split(X, y, test_size=.2, 
                                                                          random_state=254, 
                                                                          stratify = y)
    X_train, X_validate, y_train, y_validate = train_test_split(X_train_validate, y_train_validate, test_size=.3,random_state=254,stratify= y_train_validate)
    return X_train, X_validate, y_train, y_validate, X_test, y_test


def get_baseline(df):
    print('{:.5f}%'.format(round(len(df[df.review_rating == 5])/df.review_rating.value_counts().sum(),5) *100))


def train_validate_results(model, X_train, y_train, X_validate, y_validate, details=False):

    '''
    this function prints the accuracy, recall and precision of the model passed in
    if details = True, it will display the classification report and the confusion matrices for train and validate dataframes
    
    '''
    model.fit(X_train, y_train)
    t_pred = model.predict(X_train)
    v_pred = model.predict(X_validate)
    print('Train model Accuracy: {:.5f} %  | Validate model accuracy: {:.5f} % '.format(accuracy_score(y_train, t_pred) * 100, accuracy_score(y_validate, v_pred) * 100))
    print('Train model Recall: {:.5f} %    | Validate model Recall: {:.5f} %'.format(recall_score(y_train, t_pred, average='micro') * 100, recall_score(y_validate, v_pred, average='macro') * 100))
    print('Train model Precision: {:.5f} % | Validate model Precision: {:.5f} %'.format(precision_score(y_train, t_pred, average='micro') * 100, precision_score(y_validate, v_pred, average='macro') * 100))
    print('------------------------------------------------------------------------')
    if details == True:
        Col_labels = ['One', "Two", 'Three', "Four", 'Five']
        Row_labels = ['One', "Two", 'Three', "Four", 'Five']
        print('---------- More Details ------------')
        print('-----Train Classification report----')
        print(pd.DataFrame(classification_report(y_train, t_pred, output_dict =True)))
        print('------Validate Classification report-----')
        print(pd.DataFrame(classification_report(y_validate, v_pred, output_dict =True)))
        print('-----Train Confusion Matrix------')
        print(pd.DataFrame(confusion_matrix(t_pred, y_train), index=Row_labels, columns=Col_labels))
        print('-----Validation Confusion Matrix------')
        print(pd.DataFrame(confusion_matrix(v_pred, y_validate), index=Row_labels, columns=Col_labels))
        
def test_results(model, X_train, y_train,X_test, y_test, details=False):
    '''
    this function prints the accuracy, recall and precision of the model passed in
    if details = True, it will display the classification report and the confusion matrices for test dataframes
    
    '''
    model.fit(X_train, y_train)
    t_pred = model.predict(X_test)
    print('Test model Accuracy: {:.5f} %'.format(accuracy_score(y_test, t_pred) * 100))
    print('Test model Recall: {:.5f} % '.format(recall_score(y_test, t_pred,average='micro') * 100))
    print('Test model Precision: {:.5f} %'.format(precision_score(y_test, t_pred, average='micro') * 100)) 
    if details == True:
        Col_labels = ['Java', 'Javascript','R','Python']
        Row_labels = ['Java', 'Javascript','R','Python']
        print('---------- More Details ------------')
        print('-----Test Classification report----')
        print(pd.DataFrame(classification_report(y_test, t_pred, output_dict =True)))
        print('-----Test Confusion Matrix------')
        print(pd.DataFrame(confusion_matrix(t_pred, y_test), index=Row_labels, columns=Col_labels))
        
        
def predict_readme_contents(string,df):
    
    vector = TfidfVectorizer(stop_words = ['data','use'])
    X = vector.fit(df.readme_contents_cleaned)
    X = vector.transform(df.readme_contents_cleaned)
    y = df.language_cleaned
    
    X_train, X_validate, y_train, y_validate, X_test, y_test = xy_split(X, y)
    
    string = prepare.basic_clean(string)
    string = prepare.tokenize(string)
    string = prepare.lemmatize(string)
    string = prepare.remove_stopwords(string, exclude_words=['data','use'])
   
    dicto = {'c':string}
    string = pd.Series(dicto)
    answer = vector.transform(dicto)
    
    knn = KNeighborsClassifier(n_neighbors=(9))
    knn.fit(X_train, y_train)
    result = knn.predict(answer)
    
    return result