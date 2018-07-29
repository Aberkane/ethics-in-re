from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

tvec = TfidfVectorizer(stop_words=None, max_features=100000, ngram_range=(1, 3))
lr = LogisticRegression()

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import precision_score, recall_score, f1_score

from collections import Counter
from sklearn.datasets import make_classification

def lr_cv(splits, X, Y, pipeline, average_method):
    SMOTE_pipeline = make_pipeline(tvec, SMOTE(random_state=777),lr)

    tv = TfidfVectorizer(stop_words=None, max_features=100000)
    testing_tfidf = tv.fit_transform(testing_text)
    smt = SMOTE(random_state=777, k_neighbors=1)
	X_SMOTE, y_SMOTE = smt.fit_sample(testing_tfidf, testing_target)
	pd.DataFrame(X_SMOTE.todense(), columns=tv.get_feature_names())


    lr_cv(5, df.clean_text, df.sentiment, SMOTE_pipeline, 'macro')

    data_x = df[['user_story']].as_matrix()
    #data_x_tfidf = tv.fit_transform(data_x)

    data_y = df.drop(['user_story'], axis=1).as_matrix()
    #data_y_0 = np.array(column(data_y,0))
    #data_y_1 = np.array(column(data_y,1))
    #data_y_2 = np.array(column(data_y,2))

    #tv = TfidfVectorizer(stop_words=stop_words)
    #data_x_list = [x[0].strip() for x in data_x.tolist()]
    #x_tfidf = tv.fit_transform(data_x_list)

    #smt = SMOTE(random_state=42)
    #X_SMOTE0, y_SMOTE0 = smt.fit_sample(x_tfidf, data_y_0)
    #X_SMOTE1, y_SMOTE1 = smt.fit_sample(x_tfidf, data_y_1)
    #X_SMOTE2, y_SMOTE2 = smt.fit_sample(x_tfidf, data_y_2)
    # y weer tot matrix samenvoegen, maar wat doen we met x

    SMOTE_pipeline = make_pipeline(tvec, SMOTE(random_state=777),lr)




    stratified_split = StratifiedShuffleSplit(n_splits=2, test_size=0.33)
    for train_index, test_index in stratified_split.split(data_x, data_y):
        x_train, x_test = data_x[train_index], data_x[test_index]
        y_train, y_test = data_y[train_index], data_y[test_index]

    # transform matrix of plots into lists to pass to a TfidfVectorizer
    train_x = [x[0].strip() for x in x_train.tolist()]
    test_x = [x[0].strip() for x in x_test.tolist()]

    mnb(train_x, test_x, y_train, y_test, categories)
    lsvc(train_x, test_x, y_train, y_test, categories)
    lr(train_x, test_x, y_train, y_test, categories)


    #data_y_t = np.array(column(data_y,0))



    X, y = make_classification(n_classes=2, class_sep=2,
    weights=[0.1, 0.9], n_informative=3, n_redundant=1, flip_y=0,
    n_features=20, n_clusters_per_class=1, n_samples=1000, random_state=10)
    print('Original dataset shape {}'.format(Counter(y)))

    sm = SMOTE(random_state=42)
    X_res, y_res = sm.fit_sample(X, y)
    print('Resampled dataset shape {}'.format(Counter(y_res)))


    testy = np.array(column(y_train,0))

    tv = TfidfVectorizer(stop_words=stop_words)
    testing_tfidf = tv.fit_transform(train_x)

    ros = RandomOverSampler(random_state=777)
    X_ROS, y_ROS = ros.fit_sample(testing_tfidf, testy)
    pd.DataFrame(testing_tfidf.todense(), columns=tv.get_feature_names())




















    kfold = StratifiedKFold(n_splits=splits, shuffle=True, random_state=777)
    accuracy = []
    precision = []
    recall = []
    f1 = []
    for train, test in kfold.split(X, Y):
        lr_fit = pipeline.fit(X[train], Y[train])
        prediction = lr_fit.predict(X[test])
        scores = lr_fit.score(X[test],Y[test])
        
        accuracy.append(scores * 100)
        precision.append(precision_score(Y[test], prediction, average=average_method)*100)
        print('              negative    neutral     positive')
        print('precision:',precision_score(Y[test], prediction, average=None))
        recall.append(recall_score(Y[test], prediction, average=average_method)*100)
        print('recall:   ',recall_score(Y[test], prediction, average=None))
        f1.append(f1_score(Y[test], prediction, average=average_method)*100)
        print('f1 score: ',f1_score(Y[test], prediction, average=None))
        print('-'*50)

    print("accuracy: %.2f%% (+/- %.2f%%)" % (np.mean(accuracy), np.std(accuracy)))
    print("precision: %.2f%% (+/- %.2f%%)" % (np.mean(precision), np.std(precision)))
    print("recall: %.2f%% (+/- %.2f%%)" % (np.mean(recall), np.std(recall)))
    print("f1 score: %.2f%% (+/- %.2f%%)" % (np.mean(f1), np.std(f1)))
