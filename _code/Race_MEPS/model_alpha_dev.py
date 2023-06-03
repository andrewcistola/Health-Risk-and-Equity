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
df_XY['Y_Zero'] = df_XY['PAID_TOTAL'].replace([np.inf, -np.inf, np.nan, 0], 0.001).astype(np.float64)
df_XY['Y_scale'] = (df_XY['Y_Zero']/np.mean(df_XY['Y_Zero'])).astype(np.float64)
df_XY['Y_log'] = np.log(df_XY['Y_Zero']).astype(np.float64)
df_XY = df_XY.loc[:, df_XY.loc[:, df_XY.columns.str.contains('AGE|RACE|SEX|FPL_PERCENT|VISIT|PAID|ICD10|Y_log')].columns.to_list()]
df_XY['WHITE'] = np.where(df_XY['RACE'] == 2, 1, 0) # Create column based on conditions
df_XY = df_XY.drop(columns = ['VISITS_TOTAL', 'PAID_TOTAL'])
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
df_XY_2 = df_XY[df_XY['RACE'] != 2]
n_2 = df_XY_2.index.to_numpy()

### Save dataframe info for output
buffer = io.StringIO()
df_XY_1.info(buf = buffer, show_counts = True)
info_XY1 = buffer.getvalue()

### Save dataframe info for output
buffer = io.StringIO()
df_XY_2.info(buf = buffer, show_counts = True)
info_XY2 = buffer.getvalue()

### Linear Regression Baseline
model_0 = 'Linear Regression Model for All Groups'
X = ['WHITE', 'AGE', 'SEX', 'FPL_PERCENT', 'ICD10_TOTAL']
Y = ['Y_log']
x = df_XY.filter(X).to_numpy()
y = df_XY.filter(Y).to_numpy()
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x, y) # Fit model
result_0 = pd.DataFrame(OLS.coef_, columns = X)

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
text_md.write('</pre>')
text_md.write('\n')
text_md.write(info_XY1)
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(info_XY2)
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write('##### ' + model_0 + '\n')
text_md.write('\n')
text_md.write(str(result_0) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write('\n')
text_md.close() # Close file

## Learn Step 2: Linear regression model with basic variables
step_2 = 'Learn Step 2: Baseline Regression Models' 
method_1 = 'Regression model is trained on the reference group and predicts values for the focus group. The difference in predicted to actual values represents what is explained by group identififcation independent of the predictors.'

### Linear Regression
model_1 = 'Linear Regression using Demographics, Income, and Diagnosis (Total)'
label = 'OLS'

### Demographics
X = ['AGE', 'SEX']
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x_1, y_1) # Fit model
result_1z = pd.DataFrame(OLS.coef_, columns = X)
y_1_hat = OLS.predict(x_1)
y_2_KOB = OLS.predict(x_2)
OLS.fit(x_2, y_2) # Fit model
y_2_hat = OLS.predict(x_2)
KOB_1z = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics
X = ['FPL_PERCENT']
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x_1, y_1) # Fit model
result_1a = pd.DataFrame(OLS.coef_, columns = X)
y_1_hat = OLS.predict(x_1)
y_2_KOB = OLS.predict(x_2)
OLS.fit(x_2, y_2) # Fit model
y_2_hat = OLS.predict(x_2)
KOB_1a = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics and Utilization
X = ['ICD10_TOTAL']
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x_1, y_1) # Fit model
result_1b = pd.DataFrame(OLS.coef_, columns = X)
y_1_hat = OLS.predict(x_1)
y_2_KOB = OLS.predict(x_2)
OLS.fit(x_2, y_2) # Fit model
y_2_hat = OLS.predict(x_2)
KOB_1b = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics, Diagnoses, and Office Utilization
X = ['INPATIENT_VISITS']
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x_1, y_1) # Fit model
result_1c = pd.DataFrame(OLS.coef_, columns = X)
y_1_hat = OLS.predict(x_1)
y_2_KOB = OLS.predict(x_2)
OLS.fit(x_2, y_2) # Fit model
y_2_hat = OLS.predict(x_2)
KOB_1c = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics, Diagnoses, and Office Utilization
X = ['OFFICE_VISITS']
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x_1, y_1) # Fit model
result_1d = pd.DataFrame(OLS.coef_, columns = X)
y_1_hat = OLS.predict(x_1)
y_2_KOB = OLS.predict(x_2)
OLS.fit(x_2, y_2) # Fit model
y_2_hat = OLS.predict(x_2)
KOB_1d = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics, Diagnoses, and Hospital Utilization
X = ['RX_PAID']
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x_1, y_1) # Fit model
result_1e = pd.DataFrame(OLS.coef_, columns = X)
y_1_hat = OLS.predict(x_1)
y_2_KOB = OLS.predict(x_2)
OLS.fit(x_2, y_2) # Fit model
y_2_hat = OLS.predict(x_2)
KOB_1e = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics, Income, Diagnoses, and Utilization
X = ['AGE', 'SEX', 'ICD10_TOTAL', 'INPATIENT_VISITS', 'OFFICE_VISITS', 'RX_PAID']
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x_1, y_1) # Fit model
result_1f = pd.DataFrame(OLS.coef_, columns = X)
y_1_hat = OLS.predict(x_1)
y_2_KOB = OLS.predict(x_2)
OLS.fit(x_2, y_2) # Fit model
y_2_hat = OLS.predict(x_2)
KOB_1f = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Export to Summary File
text_md = open('_docs//' + label_name + '//' + label_run + '//summary.md', 'a')
text_md.write('#### ' + step_2 + '\n')
text_md.write(method_1 + '\n')
text_md.write('\n')
text_md.write('##### ' + model_1 + '\n')
text_md.write('\n')
text_md.write(str(result_1) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write('\n')
text_md.write(str(result_1z) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_1z) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_1a) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_1a) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_1b) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_1b) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_1c) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_1c) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_1d) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_1d) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_1e) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_1e) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_1f) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_1f) + '<br>\n')
text_md.write('\n')
text_md.close() # Close file

## Learn Step 3: Automated Feature Selection
step_3 = 'Learn Step 3: Automated Feature Selection Assisted with Supervised Learning' 
method_3 = 'Supervised algorithms are used to automatically identify relevant features and predict outcomes. These models allow for the inclusion of more data in closer to raw form than OLS. The models are trained on the reference group and then predict values for the focus group. The difference in predicted to actual values represents what is explained by group identififcation independent of the predictors.'

### Random Forests
model_2 = 'Random Forests'
label = 'RandomForest'

### Demographics and Income
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|SDOH')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result_2a = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
result_2a = result_2a.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = forest.predict(x_2)
forest.fit(x_2, y_2) # Fit model
y_2_hat = forest.predict(x_2)
KOB_2a = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics and Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|VISIT')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result_2b = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
result_2b = result_2b.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = forest.predict(x_2)
forest.fit(x_2, y_2) # Fit model
y_2_hat = forest.predict(x_2)
KOB_2b = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics and Diagnoses
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|ICD10')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result_2c = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
result_2c = result_2c.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = forest.predict(x_2)
forest.fit(x_2, y_2) # Fit model
y_2_hat = forest.predict(x_2)
KOB_2c = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics, Income, Diagnoses, and Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|FPL_PERCENT|VISIT|ICD10')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result_2d = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
result_2d = result_2d.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = forest.predict(x_2)
forest.fit(x_2, y_2) # Fit model
y_2_hat = forest.predict(x_2)
KOB_2d = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Gradient Boosting
model_3 = 'Gradient Boosting'
label = "XGBoost"

### Demographics and Income
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|FPL_PERCENT')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
boost = GradientBoostingRegressor(random_state = 0) # define selection parameters, in this case all features are selected. See Readme for more ifo
boost.fit(x_1, y_1) # This will take time
result_3a = pd.DataFrame({'Variables': X, 'Importances': boost.feature_importances_})
result_3a = result_3a.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = boost.predict(x_2)
boost.fit(x_2, y_2) # Fit model
y_2_hat = boost.predict(x_2)
KOB_3a = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics and Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|VISIT')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
boost = GradientBoostingRegressor(random_state = 0) # define selection parameters, in this case all features are selected. See Readme for more ifo
boost.fit(x_1, y_1) # This will take time
result_3b = pd.DataFrame({'Variables': X, 'Importances': boost.feature_importances_})
result_3b = result_3b.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = boost.predict(x_2)
boost.fit(x_2, y_2) # Fit model
y_2_hat = boost.predict(x_2)
KOB_3b = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics and Diagnoses
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|ICD10')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
boost = GradientBoostingRegressor(random_state = 0) # define selection parameters, in this case all features are selected. See Readme for more ifo
boost.fit(x_1, y_1) # This will take time
result_3c = pd.DataFrame({'Variables': X, 'Importances': boost.feature_importances_})
result_3c = result_3c.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = boost.predict(x_2)
boost.fit(x_2, y_2) # Fit model
y_2_hat = boost.predict(x_2)
KOB_3c = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics, Income, Diagnoses, and Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|RACE|FPL_PERCENT|VISIT|ICD10')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
boost = GradientBoostingRegressor(random_state = 0) # define selection parameters, in this case all features are selected. See Readme for more ifo
boost.fit(x_1, y_1) # This will take time
result_3d = pd.DataFrame({'Variables': X, 'Importances': boost.feature_importances_})
result_3d = result_3d.sort_values(by = ['Importances'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = boost.predict(x_2)
boost.fit(x_2, y_2) # Fit model
y_2_hat = boost.predict(x_2)
KOB_3d = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Support Vector Machines
model_4 = 'Support Vector Machines'
label = 'SVM'

### Demographics and Income
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|FPL_PERCENT')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
vector = LinearSVR() # Support vector machines with a linear kernel for multi-level categorical outrcomes
vector.fit(x_1, y_1) # fit model
result_4a = pd.DataFrame({'Variables': X, 'Vectors': abs(vector.coef_)})
result_4a = result_4a.sort_values(by = ['Vectors'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = vector.predict(x_2)
vector.fit(x_2, y_2) # Fit model
y_2_hat = vector.predict(x_2)
KOB_4a = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics and Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|VISIT')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
vector = LinearSVR() # Support vector machines with a linear kernel for multi-level categorical outrcomes
vector.fit(x_1, y_1) # fit model
result_4b = pd.DataFrame({'Variables': X, 'Vectors': abs(vector.coef_)})
result_4b = result_4b.sort_values(by = ['Vectors'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = vector.predict(x_2)
vector.fit(x_2, y_2) # Fit model
y_2_hat = vector.predict(x_2)
KOB_4b = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics and Diagnoses
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|ICD10')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
vector = LinearSVR() # Support vector machines with a linear kernel for multi-level categorical outrcomes
vector.fit(x_1, y_1) # fit model
result_4c = pd.DataFrame({'Variables': X, 'Vectors': abs(vector.coef_)})
result_4c = result_4c.sort_values(by = ['Vectors'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = vector.predict(x_2)
vector.fit(x_2, y_2) # Fit model
y_2_hat = vector.predict(x_2)
KOB_4c = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics, Income, Diagnoses, and Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|RACE|FPL_PERCENT|VISIT|ICD10')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
vector = LinearSVR() # Support vector machines with a linear kernel for multi-level categorical outrcomes
vector.fit(x_1, y_1) # fit model
result_4d = pd.DataFrame({'Variables': X, 'Vectors': abs(vector.coef_)})
result_4d = result_4d.sort_values(by = ['Vectors'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = vector.predict(x_2)
vector.fit(x_2, y_2) # Fit model
y_2_hat = vector.predict(x_2)
KOB_4d = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Recursive feature Elimination
model_5 = 'Recursive feature Elimination'
label = "RFE-CV"

### Demographics and Income
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|FPL_PERCENT')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
recursive = RFECV(estimator = LinearRegression(), min_features_to_select = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
recursive.fit(x_1, y_1) # This will take time
result_5a = pd.DataFrame({'Variables': X, 'Rankings': recursive.ranking_})
result_5a = result_5a.sort_values(by = ['Rankings'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = recursive.predict(x_2)
recursive.fit(x_2, y_2) # Fit model
y_2_hat = recursive.predict(x_2)
KOB_5a = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics and Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|VISIT')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
recursive = RFECV(estimator = LinearRegression(), min_features_to_select = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
recursive.fit(x_1, y_1) # This will take time
result_5b = pd.DataFrame({'Variables': X, 'Rankings': recursive.ranking_})
result_5b = result_5b.sort_values(by = ['Rankings'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = recursive.predict(x_2)
recursive.fit(x_2, y_2) # Fit model
y_2_hat = recursive.predict(x_2)
KOB_5b = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics and Diagnoses
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|ICD10')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
recursive = RFECV(estimator = LinearRegression(), min_features_to_select = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
recursive.fit(x_1, y_1) # This will take time
result_5c = pd.DataFrame({'Variables': X, 'Rankings': recursive.ranking_})
result_5c = result_5c.sort_values(by = ['Rankings'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = recursive.predict(x_2)
recursive.fit(x_2, y_2) # Fit model
y_2_hat = recursive.predict(x_2)
KOB_5c = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics, Income, Diagnoses, and Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|RACE|FPL_PERCENT|VISIT|ICD10')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
recursive = RFECV(estimator = LinearRegression(), min_features_to_select = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
recursive.fit(x_1, y_1) # This will take time
result_5d = pd.DataFrame({'Variables': X, 'Rankings': recursive.ranking_})
result_5d = result_5d.sort_values(by = ['Rankings'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = recursive.predict(x_2)
recursive.fit(x_2, y_2) # Fit model
y_2_hat = recursive.predict(x_2)
KOB_5d = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Ridge Regression
model_6 = 'Ridge Regression (with Cross Validation)'
label = "Ridge"

### Demographics and Income
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|FPL_PERCENT')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
ridge = RidgeCV(cv = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
ridge.fit(x_1, y_1) # This will take time
result_6a = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(ridge.coef_)})
result_6a = result_6a.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = ridge.predict(x_2)
ridge.fit(x_2, y_2) # Fit model
y_2_hat = ridge.predict(x_2)
KOB_6a = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics and Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|VISIT')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
ridge = RidgeCV(cv = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
ridge.fit(x_1, y_1) # This will take time
result_6b = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(ridge.coef_)})
result_6b = result_6b.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = ridge.predict(x_2)
ridge.fit(x_2, y_2) # Fit model
y_2_hat = ridge.predict(x_2)
KOB_6b = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics and Diagnoses
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|ICD10')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
ridge = RidgeCV(cv = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
ridge.fit(x_1, y_1) # This will take time
result_6c = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(ridge.coef_)})
result_6c = result_6c.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = ridge.predict(x_2)
ridge.fit(x_2, y_2) # Fit model
y_2_hat = ridge.predict(x_2)
KOB_6c = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics, Income, Diagnoses, and Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|RACE|FPL_PERCENT|VISIT|ICD10')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
ridge = RidgeCV(cv = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
ridge.fit(x_1, y_1) # This will take time
result_6d = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(ridge.coef_)})
result_6d = result_6d.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = ridge.predict(x_2)
ridge.fit(x_2, y_2) # Fit model
y_2_hat = ridge.predict(x_2)
KOB_6d = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Least absolute shrinkage and selection operator
model_7 = 'Least absolute shrinkage and selection operator'
label = "Lasso"

### Demographics and Income
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|FPL_PERCENT')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
lasso = LassoCV(cv = 5, random_state = 0) # define selection parameters, in this case all features are selected. See Readme for more ifo
lasso.fit(x_1, y_1) # This will take time
result_7a = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(lasso.coef_)})
result_7a = result_7a.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = lasso.predict(x_2)
lasso.fit(x_2, y_2) # Fit model
y_2_hat = lasso.predict(x_2)
KOB_7a = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics and Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|VISIT')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
lasso = RidgeCV(cv = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
lasso.fit(x_1, y_1) # This will take time
result_7b = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(lasso.coef_)})
result_7b = result_7b.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = lasso.predict(x_2)
lasso.fit(x_2, y_2) # Fit model
y_2_hat = lasso.predict(x_2)
KOB_7b = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics and Diagnoses
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|ICD10')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
lasso = RidgeCV(cv = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
lasso.fit(x_1, y_1) # This will take time
result_7c = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(lasso.coef_)})
result_7c = result_7c.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = lasso.predict(x_2)
lasso.fit(x_2, y_2) # Fit model
y_2_hat = lasso.predict(x_2)
KOB_7c = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Demographics, Income, Diagnoses, and Utilization
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|RACE|FPL_PERCENT|VISIT|ICD10')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()
lasso = RidgeCV(cv = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
lasso.fit(x_1, y_1) # This will take time
result_7d = pd.DataFrame({'Variables': X, 'Coefficients': np.ravel(lasso.coef_)})
result_7d = result_7d.sort_values(by = ['Coefficients'], ascending = False) # Sort dataframe by selected column in descending order
y_2_KOB = lasso.predict(x_2)
lasso.fit(x_2, y_2) # Fit model
y_2_hat = lasso.predict(x_2)
KOB_7d = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Neural Networks
model_9 = 'Multi-Layer Perceptron'
label = "MLP"

### Demographics and Income
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()

#### Train MLP on reference group
N_input = x_1.shape[1] # Save number of columns as input dimension
N_nodes = round(N_input / 2) # Number of input dimensions divided by two for nodes in each layer
N_epochs = 100
network = Sequential() # Build Network with keras Sequential API
network.add(Dense(N_nodes, activation = 'relu', kernel_initializer = 'random_normal', input_dim = N_input)) # First dense layer
network.add(Dense(N_nodes, activation = 'relu', kernel_initializer = 'random_normal')) # Second dense layer
network.add(Dense(1, activation = 'linear', kernel_initializer = 'random_normal')) # Output layer with binary activation
network.compile(optimizer = 'adam', loss = 'mean_absolute_error', metrics = ['mean_squared_error']) # Compile network with Adaptive moment estimation, and follow loss and accuracy
history = network.fit(x_1, y_1, batch_size = 10, epochs = N_epochs) # Fitting the data to the train outcome, with batch size and number of epochs
result_9a = pd.DataFrame({'Loss': history.history['loss']})

#### Predict focus group with reference group
y_1_hat = network.predict(x_1) # Predict values from test data
y_2_KOB = network.predict(x_2) # Predict values from test data

#### Refit and predict focus group
history = network.fit(x_2, y_2, batch_size = 10, epochs = N_epochs) # Fitting the data to the train outcome, with batch size and number of epochs
y_2_hat = network.predict(x_2) # Predict values from test data
KOB_9a = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Everything
X = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|FPL_PERCENT|VISIT|PAID|ICD10')].columns.to_list()
Y = ['Y_log']
x_1 = df_XY_1.filter(X).to_numpy()
x_2 = df_XY_2.filter(X).to_numpy()
y_1 = df_XY_1.filter(Y).to_numpy()
y_2 = df_XY_2.filter(Y).to_numpy()

#### Train MLP on reference group
N_input = x_1.shape[1] # Save number of columns as input dimension
N_nodes = round(N_input / 2) # Number of input dimensions divided by two for nodes in each layer
N_epochs = 100
network = Sequential() # Build Network with keras Sequential API
network.add(Dense(N_nodes, activation = 'relu', kernel_initializer = 'random_normal', input_dim = N_input)) # First dense layer
network.add(Dense(N_nodes, activation = 'relu', kernel_initializer = 'random_normal')) # Second dense layer
network.add(Dense(1, activation = 'linear', kernel_initializer = 'random_normal')) # Output layer with binary activation
network.compile(optimizer = 'adam', loss = 'mean_absolute_error', metrics = ['mean_squared_error']) # Compile network with Adaptive moment estimation, and follow loss and accuracy
history = network.fit(x_1, y_1, batch_size = 10, epochs = N_epochs) # Fitting the data to the train outcome, with batch size and number of epochs
result_9d = pd.DataFrame({'Loss': history.history['loss']})

#### Predict focus group with reference group
y_1_hat = network.predict(x_1) # Predict values from test data
y_2_KOB = network.predict(x_2) # Predict values from test data

#### Refit and predict focus group
history = network.fit(x_2, y_2, batch_size = 10, epochs = N_epochs) # Fitting the data to the train outcome, with batch size and number of epochs
y_2_hat = network.predict(x_2) # Predict values from test data
KOB_9d = [
    "White Actual = " + str(round(np.mean(y_1), 4))
    , "Non-White Actual = " + str(round(np.mean(y_2), 4))
    , "White Modeled = " + str(round(np.mean(y_1_hat), 4))
    , "Non-White Modeled = " + str(round(np.mean(y_2_hat), 4))
    , "White Rsq = " + str(round(r2_score(y_1, y_1_hat), 4))
    , "Non-White Rsq = " + str(round(r2_score(y_2, y_2_hat), 4))  
    , "Non-White Predicted w/ White model = " + str(round(np.mean(y_2_KOB), 4))
    , "Difference in Bs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_hat)), 4))
    , "Difference in Xs = " + str(round((np.mean(y_1_hat) - np.mean(y_2_KOB)), 4))
    ]

### Export to Summary File
text_md = open('_docs//' + label_name + '//' + label_run + '//summary.md', 'a')
text_md.write('##### ' + model_2 + '\n')
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
text_md.write(str(result_2d) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_2d) + '<br>\n')
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
text_md.write(str(result_3d) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_3d) + '<br>\n')
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
text_md.write(str(result_4d) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_4d) + '<br>\n')
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
text_md.write(str(result_5d) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_5d) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_6 + '\n')
text_md.write('\n')
text_md.write(str(result_6a) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_6a) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_6b) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_6b) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_6c) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_6c) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_4d) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_6d) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_7 + '\n')
text_md.write('\n')
text_md.write(str(result_7a) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_7a) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_7b) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_7b) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_7c) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_7c) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_7d) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_7d) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_9 + '\n')
text_md.write('\n')
text_md.write(str(result_9a) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_9a) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_9d) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write(str(KOB_9d) + '<br>\n')
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
df = df.iloc[1:370]
df['DISPARITY_HISPANIC'] = (df['WHITE'] - df["HISPANIC"])
df['DISPARITY_ASIAN'] = (df['WHITE'] - df['ASIAN'])
df['DISPARITY_BLACK'] = (df['WHITE'] - df["BLACK"])
df = df.sort_values(by = ['DISPARITY_BLACK'], ascending = False) # Sort dataframe by selected column in descending order
df.to_csv(r'_data/AIM3_disparity.csv') # Write dataframe to CSV
df