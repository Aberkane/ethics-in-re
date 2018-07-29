from sklearn.model_selection import GridSearchCV 
from sklearn.metrics import classification_report

def gridSearch(pipeline, parameters, train_x, test_x, y_train, y_test, categories):
    grid_search_tune = GridSearchCV(
        pipeline, parameters, cv=2, n_jobs=2, verbose=3)
    grid_search_tune.fit(train_x, y_train)

    print
    print("Best parameters set:")
    print grid_search_tune.best_estimator_.steps
    print

    # measuring performance on test set
    print "Applying best classifier on test data:"
    best_clf = grid_search_tune.best_estimator_
    predictions = best_clf.predict(test_x)

    print classification_report(y_test, predictions, target_names=categories)
