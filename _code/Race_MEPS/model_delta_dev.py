# Machine Learning Script

## Mahcine Learning Step 1: Data Processing of Predictors and Outcomes
step_1 = 'Machine Learning Step 1: Data Processing of Predictors and Outcomes'
method_1 = 'Various machine learning models were trained on a reference population and then used to predict values from a focus populaiton. The difference in predicted to actual values for the focus group then to reflects the impact of group identification. This is an adaptation of the Kitigawa-Oaxaca-Blinder method.'
group_1 = 'Non-Hispanic White (RACETH == 2)'
group_2 = 'Not Non-Hispanic White (RACETH != 2)' 
W = 'PERSON_ID'
Z = 'YEAR'

### Import Labels/Demographics (W) with Predictors (X) Outcomes (Y) and Shapes/Subgroups (Z)
df_WXYZ = pd.read_csv('_data//' + label_name + '//' + label_run + '//analytical_Q2.csv')

### Define Predictors from imported data (X)

### Create Outcome-Predictor pandas dataframe (XY)
df_XY = df_WXYZ.set_index([W, Z]) # Reset Index
df_XY['PAID_Zero'] = df_XY['PAID_TOTAL'].replace([np.inf, -np.inf, np.nan, 0], 0.01).astype(np.float64)
df_XY['PAID_log'] = np.log(df_XY['PAID_Zero']).astype(np.float64)
df_XY['ALWD_Zero'] = df_XY['ALWD_TOTAL'].replace([np.inf, -np.inf, np.nan, 0], 0.01).astype(np.float64)
df_XY['ALWD_log'] = np.log(df_XY['ALWD_Zero']).astype(np.float64)
df_XY = df_XY.loc[:, df_XY.loc[:, df_XY.columns.str.contains('AGE|RACE|SEX|SDOH|PAID|ALWD|ICD10|CONDITIONS|VISIT|HEALTH|PAID_log')].columns.to_list()]
df_XY['WHITE'] = np.where(df_XY['RACE'] == 2, 1, 0) # Create column based on conditions
df_XY = df_XY.drop(columns = ['VISITS_TOTAL', 'PAID_TOTAL', 'ALWD_TOTAL', 'ICD10_TOTAL'])
df_XY = df_XY.dropna()
df_XY.info() # Get class, memory, and column info: names, data types, obs.

### Save dataframe info for output
buffer = io.StringIO()
df_WXYZ.info(buf = buffer, show_counts = True)
info_WXYZ = buffer.getvalue()

### Create Outcome and predictor standard scaled numpy arrays for reference group (n_1, x_1, y_1)
df_XY_1 = df_XY[df_XY['RACE'] == 2]
n_1 = df_XY_1.index.to_numpy()

### Create Outcome and predictor standard scaled numpy arrays for focus group (n_2, x_2, y_2)
df_XY_2 = df_XY[df_XY['RACE'] == 1]
n_2 = df_XY_2.index.to_numpy()

### Linear Regression Baseline
model_0 = 'Linear Regression Model for All Groups'
X = ['WHITE', 'AGE', 'SEX', 'SDOH_FPL', 'CONDITIONS']
Y = ['PAID_log']
x = df_XY.filter(X).to_numpy()
y = df_XY.filter(Y).to_numpy()
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x, y) # Fit model
result_0 = pd.DataFrame(OLS.coef_, columns = X)
result_0

### Linear Regression Baseline
model_0 = 'Linear Regression Model for All Groups'
X = ['WHITE', 'AGE', 'SEX', 'SDOH_FPL', 'CONDITIONS']
Y = ['ALWD_log']
x = df_XY.filter(X).to_numpy()
y = df_XY.filter(Y).to_numpy()
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x, y) # Fit model
result_0 = pd.DataFrame(OLS.coef_, columns = X)
result_0

### Export to Summary File
text_md = open('_docs//' + label_name + '//' + label_run + '//summary.md', 'a')
text_md.write('### ' + 'Machine Learning Result Summary' + '\n')
text_md.write(method_1 + '<br>\n')
text_md.write('The following results used the scikit-learn and keras libraries for Python version ' + str(sys.version) + '\n')
text_md.write('\n')
text_md.write('#### ' + step_1 + '\n')
text_md.write('Source: ' + '_data//' + label_name + '//' +  label_run + '//analytical_Q2.csv' + '\n')
text_md.write('\n')
text_md.write('W (ID variables): ' + W + '<br>\n')
text_md.write('Z (Subgroup variables): ' + Z + '<br>\n')
text_md.write('\n')
text_md.write('Reference group: ' + group_1 + '<br>\n')
text_md.write('Focus group: ' + group_2 + '<br>\n')
text_md.write('\n')
text_md.write('\n')
text_md.write('<pre>')
text_md.write('\n')
text_md.write(info_WXYZ)
text_md.write('\n')
text_md.write('##### ' + model_0 + '\n')
text_md.write('\n')
text_md.write(str(result_0) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write('\n')
text_md.close() # Close file

## 'Learn Step 2: Decomposition Paid amounts Using Machine Learning Models'
step_2 = 'Learn Step 2: Decomposition Paid amount Using Machine Learning Models' 
method_1 = 'Model is trained on the reference group and predicts values for the focus group. The difference in predicted to actual values represents what is explained by group identififcation independent of the predictors.'

### Linear Regression
model_1 = 'Linear Regression using Demographics, Income, and Diagnosis (Total)'
label = 'OLS'

### Simplified Variables
X = ['AGE', 'SEX', 'CONDITIONS', 'SDOH_FPL']
Y = ['PAID_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x_1, y_1) # Fit model
result_1 = pd.DataFrame(OLS.coef_, columns = X)
y_1_hat = OLS.predict(x_1)
y_2_KOB = OLS.predict(x_2)
KOB_1 = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_1

### Random Forests
model_2 = 'Random Forests'
label = 'RandomForest'

### Social Determinants
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|SDOH')].columns.to_list()
Y = ['PAID_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result_2a = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
result_2a = result_2a.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = forest.predict(x_2)
y_1_hat = forest.predict(x_1)
KOB_2a = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_2a

### Diagnoses
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|ICD10')].columns.to_list()
Y = ['PAID_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result_2b = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
result_2b = result_2b.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = forest.predict(x_2)
y_1_hat = forest.predict(x_1)
KOB_2b = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_2b

### Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|VISIT')].columns.to_list()
Y = ['PAID_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result_2c = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
result_2c = result_2c.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = forest.predict(x_2)
y_1_hat = forest.predict(x_1)
KOB_2c = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_2c

### Gradient Boosting
model_3 = 'Gradient Boosting'
label = "XGBoost"

### Social Determinants
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|SDOH')].columns.to_list()
Y = ['PAID_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
boost = GradientBoostingRegressor(random_state = 0) # define selection parameters, in this case all features are selected. See Readme for more ifo
boost.fit(x_1, y_1) # This will take time
result_3a = pd.DataFrame({'Variables': X, 'Importances': boost.feature_importances_})
result_3a = result_3a.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = boost.predict(x_2)
y_1_hat = boost.predict(x_1)
KOB_3a = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_3a

### Diagnoses
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|ICD10')].columns.to_list()
Y = ['PAID_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
boost = GradientBoostingRegressor(random_state = 0) # define selection parameters, in this case all features are selected. See Readme for more ifo
boost.fit(x_1, y_1) # This will take time
result_3b = pd.DataFrame({'Variables': X, 'Importances': boost.feature_importances_})
result_3b = result_3b.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = boost.predict(x_2)
y_1_hat = boost.predict(x_1)
KOB_3b = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_3b

### Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|VISIT')].columns.to_list()
Y = ['PAID_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
boost = GradientBoostingRegressor(random_state = 0) # define selection parameters, in this case all features are selected. See Readme for more ifo
boost.fit(x_1, y_1) # This will take time
result_3c = pd.DataFrame({'Variables': X, 'Importances': boost.feature_importances_})
result_3c = result_3c.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = boost.predict(x_2)
y_1_hat = boost.predict(x_1)
KOB_3c = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_3c

### Ridge Regression
model_4 = 'Ridge Regression (with Cross Validation)'
label = "Ridge"

### Social Determinants
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|SDOH')].columns.to_list()
Y = ['PAID_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
ridge = RidgeCV(cv = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
ridge.fit(x_1, y_1) # This will take time
result_4a = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(ridge.coef_)})
result_4a = result_4a.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = ridge.predict(x_2)
y_1_hat = ridge.predict(x_1)
KOB_4a = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_4a

### Diagnoses
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|ICD10')].columns.to_list()
Y = ['PAID_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
ridge = RidgeCV(cv = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
ridge.fit(x_1, y_1) # This will take time
result_4b = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(ridge.coef_)})
result_4b = result_4b.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = ridge.predict(x_2)
y_1_hat = ridge.predict(x_1)
KOB_4b = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_4b

### Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|VISIT')].columns.to_list()
Y = ['PAID_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
ridge = RidgeCV(cv = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
ridge.fit(x_1, y_1) # This will take time
result_4c = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(ridge.coef_)})
result_4c = result_4c.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = ridge.predict(x_2)
y_1_hat = ridge.predict(x_1)
KOB_4c = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_4c

### Least absolute shrinkage and selection operator
model_5 = 'Least absolute shrinkage and selection operator'
label = "Lasso"

### Social Determinants
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|SDOH')].columns.to_list()
Y = ['PAID_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
lasso = LassoCV(cv = 5, random_state = 0) # define selection parameters, in this case all features are selected. See Readme for more ifo
lasso.fit(x_1, y_1) # This will take time
result_5a = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(lasso.coef_)})
result_5a = result_5a.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = lasso.predict(x_2)
y_1_hat = lasso.predict(x_1)
KOB_5a = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_5a

### Diagnoses
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|ICD10')].columns.to_list()
Y = ['PAID_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
lasso = RidgeCV(cv = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
lasso.fit(x_1, y_1) # This will take time
result_5b = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(lasso.coef_)})
result_5b = result_5b.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = lasso.predict(x_2)
y_1_hat = lasso.predict(x_1)
KOB_5b = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_5b

### Utilizaiton
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|VISIT')].columns.to_list()
Y = ['PAID_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
lasso = RidgeCV(cv = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
lasso.fit(x_1, y_1) # This will take time
result_5c = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(lasso.coef_)})
result_5c = result_5c.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = lasso.predict(x_2)
y_1_hat = lasso.predict(x_1)
KOB_5c = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_5c

### Neural Networks
model_6 = 'Multi-Layer Perceptron'
label = "MLP"

### Everything
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|SDOH|ICD10|VISIT|HEALTH|CONDITION')].columns.to_list()
Y = ['PAID_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()

#### Train MLP on reference group
N_input = x_1.shape[1] # Save number of columns as input dimension
N_nodes = round(N_input / 2) # Number of input dimensions divided by two for nodes in each layer
N_epochs = 500
network = Sequential() # Build Network with keras Sequential API
network.add(Dense(N_nodes, activation = 'relu', kernel_initializer = 'random_normal', input_dim = N_input)) # First dense layer
network.add(Dense(N_nodes, activation = 'relu', kernel_initializer = 'random_normal')) # Second dense layer
network.add(Dense(1, activation = 'linear', kernel_initializer = 'random_normal')) # Output layer with binary activation
network.compile(optimizer = 'adam', loss = 'mean_absolute_error', metrics = ['mean_squared_error']) # Compile network with Adaptive moment estimation, and follow loss and accuracy
history = network.fit(x_1, y_1, batch_size = 10, epochs = N_epochs) # Fitting the data to the train outcome, with batch size and number of epochs
result_6 = pd.DataFrame({'Loss': history.history['loss']})

#### Predict focus group with reference group
y_1_hat = network.predict(x_1) # Predict values from test data
y_2_KOB = network.predict(x_2) # Predict values from test data
KOB_6 = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_6

### Export to Summary File
text_md = open('_docs//' + label_name + '//' + label_run + '//summary.md', 'a')
text_md.write('#### ' + step_2 + '\n')
text_md.write('\n')
text_md.write('##### ' + model_2 + '\n')
text_md.write('\n')
text_md.write(str(result_1) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_1) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_2a) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_2a) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_2b) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_2b) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_2c) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_2c) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_3 + '\n')
text_md.write('\n')
text_md.write(str(result_3a) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_3a) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_3b) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_3b) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_3c) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_3c) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_4 + '\n')
text_md.write('\n')
text_md.write(str(result_4a) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_4a) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_4b) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_4b) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_4c) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_4c) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_5 + '\n')
text_md.write('\n')
text_md.write(str(result_5a) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_5a) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_5b) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_5b) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_5c) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_5c) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_6 + '\n')
text_md.write('\n')
text_md.write(str(result_6) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_6) + '<br>\n')
text_md.write('\n')
text_md.close() # Close file

## 'Learn Step 3: Decomposition Allowed amounts Using Machine Learning Models'
step_3 = 'Learn Step 2: Decomposition Using Machine Learning Models' 
method_1 = 'Model is trained on the reference group and predicts values for the focus group. The difference in predicted to actual values represents what is explained by group identififcation independent of the predictors.'

### Linear Regression
model_1 = 'Linear Regression using Demographics, Income, and Diagnosis (Total)'
label = 'OLS'

### Simplified Variables
X = ['AGE', 'SEX', 'CONDITIONS', 'SDOH_FPL']
Y = ['ALWD_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x_1, y_1) # Fit model
result_1 = pd.DataFrame(OLS.coef_, columns = X)
y_1_hat = OLS.predict(x_1)
y_2_KOB = OLS.predict(x_2)
KOB_1 = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_1

### Random Forests
model_2 = 'Random Forests'
label = 'RandomForest'

### Social Determinants
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|SDOH')].columns.to_list()
Y = ['ALWD_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result_2a = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
result_2a = result_2a.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
result_2a.to_csv(r'_data/AIM3_importance_SDOH.csv') # Write dataframe to CSV
y_2_KOB = forest.predict(x_2)
y_1_hat = forest.predict(x_1)
KOB_2a = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_2a

### Diagnoses
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|ICD10')].columns.to_list()
Y = ['ALWD_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result_2b = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
result_2b = result_2b.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
result_2b.to_csv(r'_data/AIM3_importance_ICD10.csv') # Write dataframe to CSV
y_2_KOB = forest.predict(x_2)
y_1_hat = forest.predict(x_1)
KOB_2b = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_2b

### Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|VISIT')].columns.to_list()
Y = ['ALWD_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result_2c = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
result_2c = result_2c.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
result_2c.to_csv(r'_data/AIM3_importance_VISIT.csv') # Write dataframe to CSV
y_2_KOB = forest.predict(x_2)
y_1_hat = forest.predict(x_1)
KOB_2c = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_2c

### Gradient Boosting
model_3 = 'Gradient Boosting'
label = "XGBoost"

### Social Determinants
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|SDOH')].columns.to_list()
Y = ['ALWD_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
boost = GradientBoostingRegressor(random_state = 0) # define selection parameters, in this case all features are selected. See Readme for more ifo
boost.fit(x_1, y_1) # This will take time
result_3a = pd.DataFrame({'Variables': X, 'Importances': boost.feature_importances_})
result_3a = result_3a.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = boost.predict(x_2)
y_1_hat = boost.predict(x_1)
KOB_3a = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_3a

### Diagnoses
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|ICD10')].columns.to_list()
Y = ['ALWD_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
boost = GradientBoostingRegressor(random_state = 0) # define selection parameters, in this case all features are selected. See Readme for more ifo
boost.fit(x_1, y_1) # This will take time
result_3b = pd.DataFrame({'Variables': X, 'Importances': boost.feature_importances_})
result_3b = result_3b.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = boost.predict(x_2)
y_1_hat = boost.predict(x_1)
KOB_3b = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_3b

### Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|VISIT')].columns.to_list()
Y = ['ALWD_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
boost = GradientBoostingRegressor(random_state = 0) # define selection parameters, in this case all features are selected. See Readme for more ifo
boost.fit(x_1, y_1) # This will take time
result_3c = pd.DataFrame({'Variables': X, 'Importances': boost.feature_importances_})
result_3c = result_3c.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = boost.predict(x_2)
y_1_hat = boost.predict(x_1)
KOB_3c = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_3c

### Ridge Regression
model_4 = 'Ridge Regression (with Cross Validation)'
label = "Ridge"

### Social Determinants
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|SDOH')].columns.to_list()
Y = ['ALWD_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
ridge = RidgeCV(cv = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
ridge.fit(x_1, y_1) # This will take time
result_4a = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(ridge.coef_)})
result_4a = result_4a.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = ridge.predict(x_2)
y_1_hat = ridge.predict(x_1)
KOB_4a = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_4a

### Diagnoses
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|ICD10')].columns.to_list()
Y = ['ALWD_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
ridge = RidgeCV(cv = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
ridge.fit(x_1, y_1) # This will take time
result_4b = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(ridge.coef_)})
result_4b = result_4b.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = ridge.predict(x_2)
y_1_hat = ridge.predict(x_1)
KOB_4b = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_4b

### Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|VISIT')].columns.to_list()
Y = ['ALWD_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
ridge = RidgeCV(cv = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
ridge.fit(x_1, y_1) # This will take time
result_4c = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(ridge.coef_)})
result_4c = result_4c.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = ridge.predict(x_2)
y_1_hat = ridge.predict(x_1)
KOB_4c = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_4c

### Least absolute shrinkage and selection operator
model_5 = 'Least absolute shrinkage and selection operator'
label = "Lasso"

### Social Determinants
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|SDOH')].columns.to_list()
Y = ['ALWD_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
lasso = LassoCV(cv = 5, random_state = 0) # define selection parameters, in this case all features are selected. See Readme for more ifo
lasso.fit(x_1, y_1) # This will take time
result_5a = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(lasso.coef_)})
result_5a = result_5a.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = lasso.predict(x_2)
y_1_hat = lasso.predict(x_1)
KOB_5a = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_5a

### Diagnoses
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|ICD10')].columns.to_list()
Y = ['ALWD_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
lasso = RidgeCV(cv = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
lasso.fit(x_1, y_1) # This will take time
result_5b = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(lasso.coef_)})
result_5b = result_5b.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = lasso.predict(x_2)
y_1_hat = lasso.predict(x_1)
KOB_5b = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_5b

### Utilizaiton
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|VISIT')].columns.to_list()
Y = ['ALWD_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
lasso = RidgeCV(cv = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
lasso.fit(x_1, y_1) # This will take time
result_5c = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(lasso.coef_)})
result_5c = result_5c.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = lasso.predict(x_2)
y_1_hat = lasso.predict(x_1)
KOB_5c = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_5c

### Neural Networks
model_6 = 'Multi-Layer Perceptron'
label = "MLP"

### Everything
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|SDOH|ICD10|VISIT|HEALTH|CONDITION')].columns.to_list()
Y = ['ALWD_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()

#### Train MLP on reference group
N_input = x_1.shape[1] # Save number of columns as input dimension
N_nodes = round(N_input / 2) # Number of input dimensions divided by two for nodes in each layer
N_epochs = 500
network = Sequential() # Build Network with keras Sequential API
network.add(Dense(N_nodes, activation = 'relu', kernel_initializer = 'random_normal', input_dim = N_input)) # First dense layer
network.add(Dense(N_nodes, activation = 'relu', kernel_initializer = 'random_normal')) # Second dense layer
network.add(Dense(1, activation = 'linear', kernel_initializer = 'random_normal')) # Output layer with binary activation
network.compile(optimizer = 'adam', loss = 'mean_absolute_error', metrics = ['mean_squared_error']) # Compile network with Adaptive moment estimation, and follow loss and accuracy
history = network.fit(x_1, y_1, batch_size = 10, epochs = N_epochs) # Fitting the data to the train outcome, with batch size and number of epochs
result_6 = pd.DataFrame({'Loss': history.history['loss']})

#### Predict focus group with reference group
y_1_hat = network.predict(x_1) # Predict values from test data
y_2_KOB = network.predict(x_2) # Predict values from test data
KOB_6 = [
    "White Average = " + str(round(np.mean(y_1), 4))
    , "Non-White Average = " + str(round(np.mean(y_2), 4)) 
    , "Non-White Predicted = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1) - np.mean(y_2)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_2_KOB) - np.mean(y_2)), 4))
    , "R-squared + " + str(round(r2_score(y_1, y_1_hat), 4))
    ]
KOB_6

### Export to Summary File
text_md = open('_docs//' + label_name + '//' + label_run + '//summary.md', 'a')
text_md.write('#### ' + step_3 + '\n')
text_md.write('\n')
text_md.write('##### ' + model_2 + '\n')
text_md.write('\n')
text_md.write(str(result_1) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_1) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_2a) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_2a) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_2b) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_2b) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_2c) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_2c) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_3 + '\n')
text_md.write('\n')
text_md.write(str(result_3a) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_3a) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_3b) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_3b) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_3c) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_3c) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_4 + '\n')
text_md.write('\n')
text_md.write(str(result_4a) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_4a) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_4b) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_4b) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_4c) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_4c) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_5 + '\n')
text_md.write('\n')
text_md.write(str(result_5a) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_5a) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_5b) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_5b) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_5c) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_5c) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_6 + '\n')
text_md.write('\n')
text_md.write(str(result_6) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_6) + '<br>\n')
text_md.write('\n')
text_md.close() # Close file

### Group Level Statistics
XY = df_WXYZ.loc[:, df_WXYZ.columns.str.contains('PERSON_ID|YEAR|RACE|ICD10')].columns.to_list()
df = df_WXYZ.filter(XY).groupby(['PERSON_ID', 'YEAR', 'RACE'], as_index = False).sum() # Keep selected columns and sum by key columns (keeping all as columns not index)
df['PERSON_N'] = 1
XY = df.loc[:, df.columns.str.contains('PERSON_N|RACE|ICD10')].columns.to_list()
df = df.filter(XY).groupby(['RACE'], as_index = False).sum() # Keep selected columns and sum by key columns (keeping all as columns not index)
df.columns
for i in df.loc[:, df.columns.str.contains('ICD10')].columns.to_list(): df[i] = df[i]/df['PERSON_N']
df['RACE'] = np.where(df['RACE'] == 1, 'HISPANIC',
                    np.where(df['RACE'] == 2, 'WHITE',
                        np.where(df['RACE'] == 3, 'BLACK',
                            'ASIAN'))) # Create column based nested conditions
df = df.transpose()
df.columns = df.iloc[0]
df = df.iloc[1:]
df['DISPARITY_HISPANIC'] = (df['WHITE'] - df["HISPANIC"])
df['DISPARITY_ASIAN'] = (df['WHITE'] - df['ASIAN'])
df['DISPARITY_BLACK'] = (df['WHITE'] - df["BLACK"])
df = df.sort_values(by = ['DISPARITY_BLACK'], ascending = False) # Sort dataframe by selected column in descending order
df = df.iloc[1:]
df.reset_index()
df = df.rename(columns = {'index': 'Variable'}) # Rename selected columns with dictionary
df.to_csv(r'_data/AIM3_disparity_ICD.csv') # Write dataframe to CSV
desc_ICD = df

### Group Level Statistics
XY = df_WXYZ.loc[:, df_WXYZ.columns.str.contains('PERSON_ID|YEAR|RACE|VISIT')].columns.to_list()
df = df_WXYZ.filter(XY).groupby(['PERSON_ID', 'YEAR', 'RACE'], as_index = False).sum() # Keep selected columns and sum by key columns (keeping all as columns not index)
df['PERSON_N'] = 1
XY = df.loc[:, df.columns.str.contains('PERSON_N|RACE|VISIT')].columns.to_list()
df = df.filter(XY).groupby(['RACE'], as_index = False).sum() # Keep selected columns and sum by key columns (keeping all as columns not index)
df.columns
for i in df.loc[:, df.columns.str.contains('VISIT')].columns.to_list(): df[i] = df[i]/df['PERSON_N']
df['RACE'] = np.where(df['RACE'] == 1, 'HISPANIC',
                    np.where(df['RACE'] == 2, 'WHITE',
                        np.where(df['RACE'] == 3, 'BLACK',
                            'ASIAN'))) # Create column based nested conditions
df = df.transpose()
df.columns = df.iloc[0]
df = df.iloc[1:]
df['DISPARITY_HISPANIC'] = (df['WHITE'] - df["HISPANIC"])
df['DISPARITY_ASIAN'] = (df['WHITE'] - df['ASIAN'])
df['DISPARITY_BLACK'] = (df['WHITE'] - df["BLACK"])
df = df.sort_values(by = ['DISPARITY_BLACK'], ascending = False) # Sort dataframe by selected column in descending order
df = df.iloc[1:]
df.reset_index()
df = df.rename(columns = {'index': 'Variable'}) # Rename selected columns with dictionary
df.to_csv(r'_data/AIM3_disparity_VISIT.csv') # Write dataframe to CSV
desc_VISIT = df

### Group Level Statistics
XY = df_WXYZ.loc[:, df_WXYZ.columns.str.contains('PERSON_ID|YEAR|RACE|SDOH')].columns.to_list()
df = df_WXYZ.filter(XY).groupby(['PERSON_ID', 'YEAR', 'RACE'], as_index = False).sum() # Keep selected columns and sum by key columns (keeping all as columns not index)
df['PERSON_N'] = 1
XY = df.loc[:, df.columns.str.contains('PERSON_N|RACE|SDOH')].columns.to_list()
df = df.filter(XY).groupby(['RACE'], as_index = False).sum() # Keep selected columns and sum by key columns (keeping all as columns not index)
df.columns
for i in df.loc[:, df.columns.str.contains('SDOH')].columns.to_list(): df[i] = df[i]/df['PERSON_N']
df['RACE'] = np.where(df['RACE'] == 1, 'HISPANIC',
                    np.where(df['RACE'] == 2, 'WHITE',
                        np.where(df['RACE'] == 3, 'BLACK',
                            'ASIAN'))) # Create column based nested conditions
df = df.transpose()
df.columns = df.iloc[0]
df = df.iloc[1:]
df['DISPARITY_HISPANIC'] = (df['WHITE'] - df["HISPANIC"])
df['DISPARITY_ASIAN'] = (df['WHITE'] - df['ASIAN'])
df['DISPARITY_BLACK'] = (df['WHITE'] - df["BLACK"])
df = df.sort_values(by = ['DISPARITY_BLACK'], ascending = False) # Sort dataframe by selected column in descending order
df = df.iloc[1:]
df.reset_index()
df = df.rename(columns = {'index': 'Variable'}) # Rename selected columns with dictionary
df.to_csv(r'_data/AIM3_disparity_SDOH.csv') # Write dataframe to CSV
desc_SDOH = df

### Group Level Statistics
XY = df_WXYZ.loc[:, df_WXYZ.columns.str.contains('PERSON_ID|YEAR|RACE|PAID|ALWD')].columns.to_list()
df = df_WXYZ.filter(XY).groupby(['PERSON_ID', 'YEAR', 'RACE'], as_index = False).sum() # Keep selected columns and sum by key columns (keeping all as columns not index)
df['PERSON_N'] = 1
XY = df.loc[:, df.columns.str.contains('PERSON_N|RACE|PAID|ALWD')].columns.to_list()
df = df.filter(XY).groupby(['RACE'], as_index = False).sum() # Keep selected columns and sum by key columns (keeping all as columns not index)
df.columns
for i in df.loc[:, df.columns.str.contains('PAID|ALWD')].columns.to_list(): df[i] = df[i]/df['PERSON_N']
df['RACE'] = np.where(df['RACE'] == 1, 'HISPANIC',
                    np.where(df['RACE'] == 2, 'WHITE',
                        np.where(df['RACE'] == 3, 'BLACK',
                            'ASIAN'))) # Create column based nested conditions
df = df.transpose()
df.columns = df.iloc[0]
df = df.iloc[1:]
df['DISPARITY_HISPANIC'] = (df['WHITE'] - df["HISPANIC"])
df['DISPARITY_ASIAN'] = (df['WHITE'] - df['ASIAN'])
df['DISPARITY_BLACK'] = (df['WHITE'] - df["BLACK"])
df = df.sort_values(by = ['DISPARITY_BLACK'], ascending = False) # Sort dataframe by selected column in descending order
df.reset_index()
df = df.rename(columns = {'index': 'Variable'}) # Rename selected columns with dictionary
df.to_csv(r'_data/AIM3_disparity_COST.csv') # Write dataframe to CSV
desc_COST = df

### Group Level Statistics
XY = df_WXYZ.loc[:, df_WXYZ.columns.str.contains('PERSON_ID|YEAR|RACE|HEALTH_STATUS')].columns.to_list()
df = df_WXYZ.filter(XY)
df['HEALTH'] = np.where(df['HEALTH_STATUS'] == 1, 'EXCELLENT',
                        np.where(df['HEALTH_STATUS'] == 2, 'VERYGOOD',
                            np.where(df['HEALTH_STATUS'] == 3, 'GOOD',
                                np.where(df['HEALTH_STATUS'] == 4, 'FAIR',
                                    np.where(df['HEALTH_STATUS'] == 5, 'POOR',
                                        np.where(df['HEALTH_STATUS'] < 1, 'MISSING',
                                            'MISSING')))))) # Create column based nested conditions
df = pd.get_dummies(df, columns = ['HEALTH'])
df = df.groupby(['PERSON_ID', 'YEAR', 'RACE'], as_index = False).sum() # Keep selected columns and sum by key columns (keeping all as columns not index)
df['PERSON_N'] = 1
XY = df.loc[:, df.columns.str.contains('PERSON_N|RACE|HEALTH')].columns.to_list()
df = df.filter(XY).groupby(['RACE'], as_index = False).sum() # Keep selected columns and sum by key columns (keeping all as columns not index)
df.columns
for i in df.loc[:, df.columns.str.contains('HEALTH')].columns.to_list(): df[i] = df[i]/df['PERSON_N']
df['RACE'] = np.where(df['RACE'] == 1, 'HISPANIC',
                    np.where(df['RACE'] == 2, 'WHITE',
                        np.where(df['RACE'] == 3, 'BLACK',
                            'ASIAN'))) # Create column based nested conditions
df = df.transpose()
df.columns = df.iloc[0]
df = df.iloc[1:]
df['DISPARITY_HISPANIC'] = (df['WHITE'] - df["HISPANIC"])
df['DISPARITY_ASIAN'] = (df['WHITE'] - df['ASIAN'])
df['DISPARITY_BLACK'] = (df['WHITE'] - df["BLACK"])
df = df.sort_values(by = ['DISPARITY_BLACK'], ascending = False) # Sort dataframe by selected column in descending order
df = df.iloc[1:]
df.reset_index()
df = df.rename(columns = {'index': 'Variable'}) # Rename selected columns with dictionary
df.to_csv(r'_data/AIM3_disparity_HEALTH.csv') # Write dataframe to CSV
desc_HEALTH = df