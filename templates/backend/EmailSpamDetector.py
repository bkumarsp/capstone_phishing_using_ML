#Author: Bharath 
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import os

# Training DataSet for email spam detection
def emailSpamDetector(spam_file=None, input_emailText="Sample Email Text"):
    if spam_file is None:
        print("CSV file not provided.")
        return -1

    # spamCSV = pd.read_csv(spam_file)
    spamCSV = spam_file

    # y === v1 = Label, z === v2 = EmailText
    y, z = spamCSV.get('v1'), spamCSV.get('v2')
    z_train, z_test, y_train, y_test = train_test_split(z, y, test_size=0.27) 

    # Train the model to classify the email as Ham/Spam.
    cv = CountVectorizer()
    features = cv.fit_transform(z_train)

    # Support vector classification : A linear classifier and regression model
    SVM_model = svm.SVC()
    SVM_model.fit(features, y_train)


    # Testing and scoring the model:
    features_test = cv.transform(z_test)
    modelScore = SVM_model.score(features_test, y_test) 

    test_object = {'v2': input_emailText}

    test = cv.transform(test_object)
    answer = SVM_model.predict(test)
    
    return modelScore, answer


def logisticRegression(spam_file=None, input_emailText="Sample Email Text"):
    if spam_file is None:
        print("CSV file not provided.")
        return -1

    # loading the data from csv file to a pandas Dataframe
    raw_mail_data = pd.read_csv('mail_data.csv')

    # replace the null values with a null string
    mail_data = raw_mail_data.where((pd.notnull(raw_mail_data)),'')
    
    # label spam mail as 0;  ham mail as 1;
    mail_data.loc[mail_data['Category'] == 'spam', 'Category',] = 0
    mail_data.loc[mail_data['Category'] == 'ham', 'Category',] = 1

    # separating the data as texts [X] and label [Y]
    X = mail_data['Message'] #text
    Y = mail_data['Category'] #label

    # Split the dataset into training and testing data
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=3)

    # transform the text data to feature vectors that can be used as input to the Logistic regression
    feature_extraction = TfidfVectorizer(min_df = 1, stop_words='english', lowercase='True')

    X_train_features = feature_extraction.fit_transform(X_train)
    X_test_features = feature_extraction.transform(X_test)

    # convert Y_train and Y_test values as integers
    Y_train = Y_train.astype('int')
    Y_test = Y_test.astype('int')

    # Training the model : LogisticRegression
    model = LogisticRegression()
    # training the Logistic Regression model with the training data
    model.fit(X_train_features, Y_train)

    #prediction on training data
    prediction_on_training_data = model.predict(X_train_features)
    accuracy_on_training_data = accuracy_score(Y_train, prediction_on_training_data)

    print('Accuracy of LR model : ', accuracy_on_training_data)

    #prediction on test data
    prediction_on_test_data = model.predict(X_test_features)
    score = accuracy_score(Y_test, prediction_on_test_data)
    print('Accuracy on test data : ', score)

    # input_mail = ["I've been searching for the right words to thank you for this breather. I promise i wont take your help for granted and will fulfil my promise. You have been wonderful and a blessing at all times"]
    input_mail = input_emailText
    # convert text to feature vectors
    input_data_features = feature_extraction.transform(input_mail)

    # making prediction
    prediction = model.predict(input_data_features)
   
    print("Score: ", score," Prediction: ", prediction)

    answer = ["Spam"]
    if (prediction[0]==1):
        answer = ["Ham"]
    else:
        answer = ["Spam"] 

    return score, answer 


# if __name__ == '__main__':
#     SpamScore = emailSpamDetector()