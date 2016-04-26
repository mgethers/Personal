def CV_datasets(data, folds = 10,random_state=10):
    nrow = len(data)
    sample_size = float(int(nrow/folds))
    used = []
    CV_frames = []
    new_data = data
    for i in range(folds-1):
        current_data = new_data
        current_set = current_data.sample(n=sample_size,random_state=random_state).sort()
        CV_frames.append(current_set)
        used.append(current_set.index)
        new_data = new_data.drop(used[i])
    CV_frames.append(new_data)
    return CV_frames;

    def Xtrain_extract(cv_datasets,outcome):
    folds = len(cv_datasets)
    xtrain_list = []
    for i in range(folds):
        current_set = cv_datasets[i]
        xtrain = current_set.drop(outcome,axis=1)
        xtrain_list.append(xtrain)
    return xtrain_list

    def ytrain_extract(cv_datasets,outcome):
    folds = len(cv_datasets)
    ytrain_list = []
    for i in range(folds):
        current_set = cv_datasets[i]
        ytrain = current_set[[outcome]].ix[:,0]
        ytrain_list.append(ytrain)
    return ytrain_list

    def trainingsets(train_list):
    folds = len(train_list)
    sets = []
    for i in range(folds):
        current_set = train_list[:i] + train_list[i+1:]
        sets.append(pd.concat(current_set))
    return sets;
    
    def log_reg_cv(outcome, predictors, data, folds, random_state=10): # outcome = string, predictors = list
    outcome_and_predictors = [outcome] + predictors
    dataset = data[outcome_and_predictors]
    train_cv = CV_datasets(dataset,folds,random_state)
    Xtrain_cv = Xtrain_extract(train_cv,outcome)
    ytrain_cv = ytrain_extract(train_cv,outcome)
    Xtrain_sets = trainingsets(Xtrain_cv)
    ytrain_sets = trainingsets(ytrain_cv)
    accuracy = []
    for i in range(folds):
        print i
        Xtest = Xtrain_cv[i]
        ytest = ytrain_cv[i]
        Xtrain = Xtrain_sets[i]
        ytrain = ytrain_sets[i]
        mod = linear_model.LogisticRegression()
        mod.fit(Xtrain,ytrain)
        accuracy.append(mod.score(Xtest,ytest))
    return accuracy;
