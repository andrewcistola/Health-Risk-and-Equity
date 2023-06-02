# Machine Learning Script

## Mahcine Learning Step 1: Data Processing of Predictors and Outcomes
step_1 = 'Machine Learning Step 1: Data Processing of Predictors and Outcomes'
method_1 = 'Various machine learning models were trained on a reference population and then used to predict values from a focus populaiton. The difference in predicted to actual values for the focus group then to reflects the impact of group identification. This is an adaptation of the Kitigawa-Oaxaca-Blinder method.'
group_1 = 'Non-Hispanic White (RACETH == 2)'
group_2 = 'Non-Hispanic Black (RACETH == 3)'
group_focus = 2
W = 'PERSON_ID'
X = ['AGE', 'SEX']
Y = 'PAID_TOTAL'
Z = 'YEAR'


### Import Labels/Demographics (W) with Predictors (X) Outcomes (Y) and Shapes/Subgroups (Z)
df_WXYZ = pd.read_csv('_data//' + label_name + '//' + label_run + '//analytical_Q2.csv')

### Define Predictors from imported data (X)

### Create Outcome-Predictor pandas dataframe (XY)
df_XY = df_WXYZ.set_index([W, Z]) # Reset Index
df_XY['Y_log'] = np.log(df_XY[Y]).replace([np.inf, -np.inf], np.nan).fillna(0).astype(np.float64)
df_XY = df_XY.dropna()
df_XY.info() # Get class, memory, and column info: names, data types, obs.

### Save dataframe info for output
buffer = io.StringIO()
df_WXYZ.info(buf = buffer, show_counts = True)
info_WXYZ = buffer.getvalue()

### Create Outcome and predictor standard scaled numpy arrays for reference group (n_1, x_1, y_1)
df_XY_1 = df_XY[df_XY['RACE'] == 2].dropna()
y_1 = df_XY_1.filter(['Y_log']).to_numpy()
x_1 = StandardScaler().fit_transform(df_XY_1.filter(X).to_numpy())
n_1 = df_XY_1.index.to_numpy()

### Create Outcome and predictor standard scaled numpy arrays for focus group (n_2, x_2, y_2)
df_XY_2 = df_XY[df_XY['RACE'] != group_focus].dropna()
y_2 = df_XY_2.filter(['Y_log']).to_numpy()
x_2 = StandardScaler().fit_transform(df_XY_2.filter(X).to_numpy())
n_2 = df_XY_2.index.to_numpy()

### Save dataframe info for output
buffer = io.StringIO()
df_XY_1.info(buf = buffer, show_counts = True)
info_XY1 = buffer.getvalue()

### Save dataframe info for output
buffer = io.StringIO()
df_XY_2.info(buf = buffer, show_counts = True)
info_XY2 = buffer.getvalue()

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
text_md.write('Y (Outcome variables): ' + Y + '<br>\n')
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
text_md.close() # Close file

## Learn Step 2: Manual Feature Selection
step_2 = 'Learn Step 2: Baseline Regression Models' 
method_2 = 'Regression model is trained on the reference group and predicts values for the focus group. The difference in predicted to actual values represents what is explained by group identififcation independent of the predictors.'

### Linear regression model with hand selected variables
model_2a = 'Linear Regression using Demographics'
label = 'OLS'
X = ['AGE', 'SEX']
x_1 = StandardScaler().fit_transform(df_XY_1.filter(X).to_numpy())
x_2 = StandardScaler().fit_transform(df_XY_2.filter(X).to_numpy())
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x_1, y_1) # Fit model
result_2a = pd.DataFrame(OLS.coef_, columns = X)
RSQ_2a = OLS.score(x_1, y_1) # rsq value
y_1_pred = OLS.predict(x_1)

OLS.fit(x_2, y_2) # Fit model
y_2_pred = OLS.predict(x_2)
KOB_2a = [np.mean(np.exp(y_1)),  np.mean(np.exp(y_2)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2))), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_pred)]

### Linear regression model with hand selected variables
model_2b = 'Linear Regression using Demographics and Income'
label = 'OLS'
X = ['AGE', 'SEX', 'FPL_PERCENT']
x_1 = StandardScaler().fit_transform(df_XY_1.filter(X).to_numpy())
x_2 = StandardScaler().fit_transform(df_XY_2.filter(X).to_numpy())
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x_1, y_1) # Fit model
result_2b = pd.DataFrame(OLS.coef_, columns = X)
RSQ_2b = OLS.score(x_1, y_1) # rsq value
y_1_hat = OLS.predict(x_1)
y_2_pred = OLS.predict(x_2)
OLS.fit(x_2, y_2) # Fit model
y_2_hat = OLS.predict(x_2)
KOB_2b = [np.mean(np.exp(y_1_hat)),  np.mean(np.exp(y_2_hat)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1_hat)) - np.mean(np.exp(y_2_hat))), (np.mean(np.exp(y_1_hat)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_hat)]

### Linear regression model with hand selected variables
model_2c = 'Linear Regression using Demographics, Income, and Diagnosis (Total)'
label = 'OLS'
X = ['AGE', 'SEX', 'FPL_PERCENT', 'ICD10_TOTAL']
x_1 = StandardScaler().fit_transform(df_XY_1.filter(X).to_numpy())
x_2 = StandardScaler().fit_transform(df_XY_2.filter(X).to_numpy())
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x_1, y_1) # Fit model
result_2c = pd.DataFrame(OLS.coef_, columns = X)
RSQ_2c = OLS.score(x_1, y_1) # rsq value
y_1_hat = OLS.predict(x_1)
y_2_pred = OLS.predict(x_2)
OLS.fit(x_2, y_2) # Fit model
y_2_hat = OLS.predict(x_2)
KOB_2c = [np.mean(np.exp(y_1_hat)),  np.mean(np.exp(y_2_hat)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1_hat)) - np.mean(np.exp(y_2_hat))), (np.mean(np.exp(y_1_hat)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_hat)]

### Linear regression model with hand selected variables
model_2d = 'Linear Regression using Demographics, Income, Diagnosis (Total), and Visit (Total)'
label = 'OLS'
X = ['AGE', 'SEX', 'FPL_PERCENT', 'ICD10_TOTAL', 'VISITS_TOTAL']
x_1 = StandardScaler().fit_transform(df_XY_1.filter(X).to_numpy())
x_2 = StandardScaler().fit_transform(df_XY_2.filter(X).to_numpy())
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x_1, y_1) # Fit model
result_2d = pd.DataFrame(OLS.coef_, columns = X)
RSQ_2d = OLS.score(x_1, y_1) # rsq value
y_1_hat = OLS.predict(x_1)
y_2_pred = OLS.predict(x_2)
OLS.fit(x_2, y_2) # Fit model
y_2_hat = OLS.predict(x_2)
KOB_2d = [np.mean(np.exp(y_1_hat)),  np.mean(np.exp(y_2_hat)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1_hat)) - np.mean(np.exp(y_2_hat))), (np.mean(np.exp(y_1_hat)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_hat)]

### Export to Summary File
text_md = open('_docs//' + label_name + '//' + label_run + '//summary.md', 'a')
text_md.write('#### ' + step_2 + '\n')
text_md.write(method_2 + '\n')
text_md.write('\n')
text_md.write('##### ' + model_2a + '\n')
text_md.write('\n')
text_md.write('<pre>')
text_md.write('\n')
text_md.write('Rsq: ' + str(RSQ_2a) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_2a) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_2b) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_2b + '\n')
text_md.write('\n')
text_md.write('<pre>')
text_md.write('\n')
text_md.write('Rsq: ' + str(RSQ_2b) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_2b) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_2b) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_2c + '\n')
text_md.write('\n')
text_md.write('<pre>')
text_md.write('\n')
text_md.write('Rsq: ' + str(RSQ_2c) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_2c) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_2c) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_2d + '\n')
text_md.write('\n')
text_md.write('<pre>')
text_md.write('\n')
text_md.write('Rsq: ' + str(RSQ_2d) + '<br>\n')
text_md.write('\n')
text_md.write(str(result_2d) + '\n')
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_2d) + '<br>\n')
text_md.write('\n')
text_md.close() # Close file

## Learn Step 3: Automated Feature Selection
step_3 = 'Learn Step 3: Automated Feature Selection Assisted with Supervised Learning' 
method_3 = 'Supervised algorithms are used to automatically identify relevant features and predict outcomes. These models allow for the inclusion of more data in closer to raw form than OLS. The models are trained on the reference group and then predict values for the focus group. The difference in predicted to actual values represents what is explained by group identififcation independent of the predictors.'

### Random Forest Regressor
model_3a = 'Random Forests with Demographics'
label = 'RandomForest'
X = ['AGE', 'SEX']
x_1 = StandardScaler().fit_transform(df_XY_1.filter(X).to_numpy())
x_2 = StandardScaler().fit_transform(df_XY_2.filter(X).to_numpy())
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
RSQ_3 = forest.score(x_1, y_1) # rsq value
y_1_pred = forest.predict(x_1)
y_2_pred = forest.predict(x_2)
KOB_3a = [np.mean(np.exp(y_1)),  np.mean(np.exp(y_2)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2))), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_pred)]
#with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
KOB_3a #result.to_excel(writer, sheet_name = label, index = False)

### Random Forest Regressor
model_3b = 'Random Forests with Demographics and Income'
label = 'RandomForest'
X = ['AGE', 'SEX', 'FPL_PERCENT']
x_1 = StandardScaler().fit_transform(df_XY_1.filter(X).to_numpy())
x_2 = StandardScaler().fit_transform(df_XY_2.filter(X).to_numpy())
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
RSQ_3 = forest.score(x_1, y_1) # rsq value
y_1_pred = forest.predict(x_1)
y_2_pred = forest.predict(x_2)
KOB_3b = [np.mean(np.exp(y_1)),  np.mean(np.exp(y_2)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2))), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_pred)]
#with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
KOB_3b #result.to_excel(writer, sheet_name = label, index = False)

### Random Forest Regressor
model_3c = 'Random Forests with Demographics, Income, Diagnosis (Total)'
label = 'RandomForest'
X = ['AGE', 'SEX', 'FPL_PERCENT', 'ICD10_TOTAL']
x_1 = StandardScaler().fit_transform(df_XY_1.filter(X).to_numpy())
x_2 = StandardScaler().fit_transform(df_XY_2.filter(X).to_numpy())
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
RSQ_3 = forest.score(x_1, y_1) # rsq value
y_1_pred = forest.predict(x_1)
y_2_pred = forest.predict(x_2)
KOB_3c = [np.mean(np.exp(y_1)),  np.mean(np.exp(y_2)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2))), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_pred)]
#with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
KOB_3c #result.to_excel(writer, sheet_name = label, index = False)

### Random Forest Regressor
model_3d = 'Random Forests with Demographics, Income, Diagnosis (Total), and Visit (Total)'
label = 'RandomForest'
X = ['AGE', 'SEX', 'FPL_PERCENT', 'ICD10_TOTAL', 'VISITS_TOTAL']
x_1 = StandardScaler().fit_transform(df_XY_1.filter(X).to_numpy())
x_2 = StandardScaler().fit_transform(df_XY_2.filter(X).to_numpy())
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
RSQ_3 = forest.score(x_1, y_1) # rsq value
y_1_pred = forest.predict(x_1)
y_2_pred = forest.predict(x_2)
KOB_3d = [np.mean(np.exp(y_1)),  np.mean(np.exp(y_2)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2))), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_pred)]
#with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
KOB_3d #result.to_excel(writer, sheet_name = label, index = False)

### Random Forest Regressor
model_4a = 'Random Forests with Demographics, Income, and Diagnosis (Specific)'
label = 'RandomForest'
X = df_XY_1.loc[:, df_XY_1.columns.str.contains('AGE|SEX|RACE|FPL_PERCENT|ICD10')].columns.to_list() # Generate list of columns with string value (use with filter or drop)
x_1 = StandardScaler().fit_transform(df_XY_1.filter(X).to_numpy())
x_2 = StandardScaler().fit_transform(df_XY_2.filter(X).to_numpy())
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
RSQ_3 = forest.score(x_1, y_1) # rsq value
y_1_pred = forest.predict(x_1)
y_2_pred = forest.predict(x_2)
KOB_4a = [np.mean(np.exp(y_1)),  np.mean(np.exp(y_2)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2))), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_pred)]
#with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
KOB_4a #result.to_excel(writer, sheet_name = label, index = False)

### Random Forest Regressor
model_4b = 'Random Forests with Demographics, Income, and Utilizaiton (Specific)'
label = 'RandomForest'
X = df_XY_1.loc[:, df_XY_1.columns.str.contains('AGE|SEX|RACE|FPL_PERCENT|COST|VISIT')].columns.to_list() # Generate list of columns with string value (use with filter or drop)
x_1 = StandardScaler().fit_transform(df_XY_1.filter(X).to_numpy())
x_2 = StandardScaler().fit_transform(df_XY_2.filter(X).to_numpy())
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
RSQ_3 = forest.score(x_1, y_1) # rsq value
y_1_pred = forest.predict(x_1)
y_2_pred = forest.predict(x_2)
KOB_4b = [np.mean(np.exp(y_1)),  np.mean(np.exp(y_2)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2))), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_pred)]
#with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
KOB_4b #result.to_excel(writer, sheet_name = label, index = False)

### Random Forest Regressor
model_4c = 'Random Forests with Demographics, Income, Diagnosis (Specific), and Utilizaiton (Specific)'
label = 'RandomForest'
X = df_XY_1.loc[:, df_XY_1.columns.str.contains('AGE|SEX|RACE|FPL_PERCENT|VISIT|COST|ICD10')].columns.to_list() # Generate list of columns with string value (use with filter or drop)
x_1 = StandardScaler().fit_transform(df_XY_1.filter(X).to_numpy())
x_2 = StandardScaler().fit_transform(df_XY_2.filter(X).to_numpy())
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
RSQ_3 = forest.score(x_1, y_1) # rsq value
y_1_pred = forest.predict(x_1)
y_2_pred = forest.predict(x_2)
KOB_4c = [np.mean(np.exp(y_1)),  np.mean(np.exp(y_2)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2))), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_pred)]
#with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
KOB_4c #result.to_excel(writer, sheet_name = label, index = False)

### Recursive Feature Elimination
model_5a = 'Recursive feature Elimination with Demographics, Income, Diagnosis (Specific), and Utilizaiton (Specific)'
label = "RFE-CV"
X = df_XY_1.loc[:, df_XY_1.columns.str.contains('AGE|SEX|RACE|FPL_PERCENT|VISIT|COST|ICD10')].columns.to_list() # Generate list of columns with string value (use with filter or drop)
x_1 = StandardScaler().fit_transform(df_XY_1.filter(X).to_numpy())
x_2 = StandardScaler().fit_transform(df_XY_2.filter(X).to_numpy())
recursive = RFECV(estimator = LinearRegression(), min_features_to_select = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
recursive.fit(x_1, y_1) # This will take time
result = pd.DataFrame({'Variables': X, 'Rankings': recursive.ranking_})
RSQ_4 = recursive.score(x_1, y_1) # rsq value
y_1_pred = recursive.predict(x_1)
y_2_pred = recursive.predict(x_2)
KOB_5a = [np.mean(np.exp(y_1)),  np.mean(np.exp(y_2)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2))), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_pred)]
#with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
KOB_5a #result.to_excel(writer, sheet_name = label, index = False)

### Gradient Boosting
model_5b = 'Gradient Boosting with Demographics, Income, Diagnosis (Specific), and Utilizaiton (Specific)'
label = "XGBoost"
X = df_XY_1.loc[:, df_XY_1.columns.str.contains('AGE|SEX|RACE|FPL_PERCENT|VISIT|COST|ICD10')].columns.to_list() # Generate list of columns with string value (use with filter or drop)
x_1 = StandardScaler().fit_transform(df_XY_1.filter(X).to_numpy())
x_2 = StandardScaler().fit_transform(df_XY_2.filter(X).to_numpy())
boost = GradientBoostingRegressor(random_state = 0) # define selection parameters, in this case all features are selected. See Readme for more ifo
boost.fit(x_1, y_1) # This will take time
result = pd.DataFrame({'Variables': X, 'Rankings': boost.ranking_})
RSQ_4 = boost.score(x_1, y_1) # rsq value
y_1_pred = boost.predict(x_1)
y_2_pred = boost.predict(x_2)
KOB_5b = [np.mean(np.exp(y_1)),  np.mean(np.exp(y_2)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2))), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_pred)]
#with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
KOB_5b #result.to_excel(writer, sheet_name = label, index = False)

### Support Vector Machines
model_5c = 'Support Vector Machines with Demographics, Income, Diagnosis (Specific), and Utilizaiton (Specific)'
label = 'SVM'
X = df_XY_1.loc[:, df_XY_1.columns.str.contains('AGE|SEX|RACE|FPL_PERCENT|VISIT|COST|ICD10')].columns.to_list() # Generate list of columns with string value (use with filter or drop)
x_1 = StandardScaler().fit_transform(df_XY_1.filter(X).to_numpy())
x_2 = StandardScaler().fit_transform(df_XY_2.filter(X).to_numpy())
vector = LinearSVR() # Support vector machines with a linear kernel for multi-level categorical outrcomes
vector.fit(x_1, y_1) # fit model
result = pd.DataFrame({'Variables': X, 'Vectors': vector.coef_})
RSQ_5 = vector.score(x_1, y_1) # rsq value
y_1_pred = vector.predict(x_1)
y_2_pred = vector.predict(x_2)
KOB_5c = [np.mean(np.exp(y_1)),  np.mean(np.exp(y_2)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2))), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_pred)]
#with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
KOB_5c #result.to_excel(writer, sheet_name = label, index = False)

### Export to Summary File
text_md = open('_docs//' + label_name + '//' + label_run + '//summary.md', 'a')
text_md.write('#### ' + step_3 + '\n')
text_md.write(method_3 + '\n')
text_md.write('For feature selection results, see ' + '_fig//' + label_name + '//' + label_run + '//results.xlsx' + '\n')
text_md.write('\n')
text_md.write('##### ' + model_3a + '\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_3a) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_3b + '\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_3b) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_3c + '\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_3c) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_3d + '\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_3d) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_4a + '\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_4a) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_4b + '\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_4b) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_4c + '\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_4c) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_5a + '\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_5a) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_5b + '\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_5b) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_5c + '\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_5c) + '<br>\n')
text_md.write('\n')
text_md.close() # Close file

## Learn Step 4: Deep Learning with Expanded predictors
step_4 = 'Learn Step 4: Deep Learning with Expanded predictors' 
method_4 = 'Deep learning algorithms are used for an expanded set of predictors in raw format. These models allow for virtually all structured data without processing and can handle complex interactions not yet understood. The models are trained on the reference group and then predict values for the focus group. The difference in predicted to actual values represents what is explained by group identififcation independent of the predictors.'

### MLP Using ACA and Diagnosis and Visit Type Data
model_10 = 'MLP with Demographics, Income, Diagnosis (Specific), and Utilizaiton (Specific)'
label = 'MLP_DX'
df_XY3 = df_XY.loc[:, df_XY.columns.str.contains('AGE|SEX|RACE|FPL_PERCENT|VISIT|COST|ICD10|Y_log')]
df_XY3.info(verbose = True)

#### Create Outcome and predictor standard scaled numpy arrays for reference group (n_1, x_1, y_1)
df_XY3_1 = df_XY3[df_XY3['RACE'] == 2].dropna()
y3_1 = df_XY3_1.filter(['Y_log']).to_numpy()
x3_1 = StandardScaler().fit_transform(df_XY3_1.drop(columns = ['Y_log', 'RACE']).to_numpy())
n3_1 = df_XY3_1.index.to_numpy()

#### Create Outcome and predictor standard scaled numpy arrays for focus group (n_2, x_2, y_2)
df_XY3_2 = df_XY3[df_XY3['RACE'] == group_focus].dropna()
y3_2 = df_XY3_2.filter(['Y_log']).to_numpy()
x3_2 = StandardScaler().fit_transform(df_XY3_2.drop(columns = ['Y_log', 'RACE']).to_numpy())
n3_2 = df_XY3_2.index.to_numpy()

#### Train MLP on reference group
N_input = x3_1.shape[1] # Save number of columns as input dimension
N_nodes = round(N_input / 2) # Number of input dimensions divided by two for nodes in each layer
N_epochs = 100
network = Sequential() # Build Network with keras Sequential API
network.add(Dense(N_nodes, activation = 'relu', kernel_initializer = 'random_normal', input_dim = N_input)) # First dense layer
network.add(Dense(N_nodes, activation = 'relu', kernel_initializer = 'random_normal')) # Second dense layer
network.add(Dense(1, activation = 'linear', kernel_initializer = 'random_normal')) # Output layer with binary activation
network.compile(optimizer = 'adam', loss = 'mean_absolute_error', metrics = ['mean_squared_error']) # Compile network with Adaptive moment estimation, and follow loss and accuracy
history = network.fit(x3_1, y3_1, batch_size = 10, epochs = N_epochs) # Fitting the data to the train outcome, with batch size and number of epochs
result = pd.DataFrame({'Loss': history.history['loss']})
#with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
KOB_10 #result.to_excel(writer, sheet_name = label, index = False)

### Predict focus group
y_2_pred = network.predict(x3_2) # Predict values from test data
y_1_pred = network.predict(x3_1) # Predict values from test data
r2_score(y_1, y_1_pred)
KOB_10 = [np.mean(np.exp(y_1)),  np.mean(np.exp(y_2)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2))), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_pred)]

### MLP Using Diagnosis and Office Visit Data

#### Extract Office Visit Data
model_9a = 'MLP Using ACA, Diagnosis, and Office Visit Data'
label = 'MLP_OF'
QUERY = """
    SELECT
        2018 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , G.*
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
            AND Y.PRSTX18 = 1
            AND Y.INSCOV18 = 1
        ) SQ
    INNER JOIN (SELECT * FROM h206g WHERE EVNTIDX <> 'NONE') G
        ON SQ.DUPERSID = G.DUPERSID
"""
df_X3 = pd.read_sql_query(QUERY, db_con)
df_X3 = df_X3.dropna()
df_X3[W] = df_X3[W].astype('int64') # Change column data type to integer
df_X3[Z] = df_X3[Z].astype('int64') # Change column data type to integer
df_X3['EVENT_ID'] = df_X3['EVNTIDX'].astype('int64') # Change column data type to integer
df_XY3 = pd.merge(df_WXYZ, df_X3, on = [W, Z], how = 'inner')
df_XY3 = df_XY3.drop_duplicates(subset = [W, Z, 'EVENT_ID'])
df_XY3 = df_XY3.set_index([W, Z, 'EVENT_ID'])
df_XY3['Y_log'] = np.log(df_XY3[Y]).replace([np.inf, -np.inf], np.nan).fillna(0).astype(np.float64)
df_XY3 = df_XY3.drop(columns = [Y])
df_XY3 = df_XY3.drop(columns = ['DUID', 'PID', 'DUPERSID', 'EVNTIDX', 'FFEEIDX'])
df_XY3.info(verbose = True)

#### Create Outcome and predictor standard scaled numpy arrays for reference group (n_1, x_1, y_1)
df_XY3_1 = df_XY3[df_XY3['RACE'] == 2].fillna(0).astype(np.float64)
y3_1 = df_XY3_1.filter(['Y_log']).to_numpy()
x3_1 = StandardScaler().fit_transform(df_XY3_1.drop(columns = ['Y_log', 'RACE']).to_numpy())
n3_1 = df_XY3_1.index.to_numpy()

#### Create Outcome and predictor standard scaled numpy arrays for focus group (n_2, x_2, y_2)
df_XY3_2 = df_XY3[df_XY3['RACE'] == group_focus].fillna(0).astype(np.float64)
y3_2 = df_XY3_2.filter(['Y_log']).to_numpy()
x3_2 = StandardScaler().fit_transform(df_XY3_2.drop(columns = ['Y_log', 'RACE']).to_numpy())
n3_2 = df_XY3_2.index.to_numpy()

#### Train MLP on reference group
N_input = x3_1.shape[1] # Save number of columns as input dimension
N_nodes = round(N_input / 2) # Number of input dimensions divided by two for nodes in each layer
N_epochs = 100
network = Sequential() # Build Network with keras Sequential API
network.add(Dense(N_nodes, activation = 'relu', kernel_initializer = 'random_normal', input_dim = N_input)) # First dense layer
network.add(Dense(N_nodes, activation = 'relu', kernel_initializer = 'random_normal')) # Second dense layer
network.add(Dense(1, activation = 'linear', kernel_initializer = 'random_normal')) # Output layer with binary activation
network.compile(optimizer = 'adam', loss = 'mean_absolute_error', metrics = ['mean_squared_error']) # Compile network with Adaptive moment estimation, and follow loss and accuracy
history = network.fit(x3_1, y3_1, batch_size = 10, epochs = N_epochs) # Fitting the data to the train outcome, with batch size and number of epochs
result = pd.DataFrame({'Loss': history.history['loss']})
#with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
KOB_9a #result.to_excel(writer, sheet_name = label, index = False)

#### Predict reference group
df_XY3_1['Y_hat'] = network.predict(x3_1)
df_XY3_3 = df_XY3_1.filter(['Y_hat', W, Z]).groupby([W, Z], as_index = True).sum() # Keep selected columns and sum by key columns (keeping all as columns not index)
df_XY_3 = pd.merge(df_XY_1.reset_index(), df_XY3_3.reset_index(), on = [W, Z], how = 'left')
df_XY_3 = df_XY_3.fillna(0).astype(np.float64)
y_1_pred = df_XY_3['Y_hat']

#### Predict focus group
df_XY3_2['Y_hat'] = network.predict(x3_2)
df_XY3_3 = df_XY3_2.filter(['Y_hat', W, Z]).groupby([W, Z], as_index = True).sum() # Keep selected columns and sum by key columns (keeping all as columns not index)
df_XY_3 = pd.merge(df_XY_2.reset_index(), df_XY3_3.reset_index(), on = [W, Z], how = 'left')
df_XY_3 = df_XY_3.fillna(0).astype(np.float64)
y_2_pred = df_XY_3['Y_hat']

#### KOB Results
r2_score(y_1, y_1_pred)
KOB_9a = [np.mean(np.exp(y_1)),  np.mean(np.exp(y_2)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2))), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_pred)]

### MLP Using Diagnosis and Hospital Visit Data
model_9b = 'MLP Using ACA, Diagnosis, and Hospital Visit Data'
label = 'MLP_IP'

#### Extract Hospital Visit Data
QUERY = """
    SELECT
        2018 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , D.*
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
            AND Y.PRSTX18 = 1
            AND Y.INSCOV18 = 1
        ) SQ
    INNER JOIN (SELECT * FROM h206d WHERE EVNTIDX <> 'NONE') D
        ON SQ.DUPERSID = D.DUPERSID
"""
df_X3 = pd.read_sql_query(QUERY, db_con)
df_X3 = df_X3.dropna()
df_X3[W] = df_X3[W].astype('int64') # Change column data type to integer
df_X3[Z] = df_X3[Z].astype('int64') # Change column data type to integer
df_X3['EVENT_ID'] = df_X3['EVNTIDX'].astype('int64') # Change column data type to integer
df_XY3 = pd.merge(df_WXYZ, df_X3, on = [W, Z], how = 'inner')
df_XY3 = df_XY3.drop_duplicates(subset = [W, Z, 'EVENT_ID'])
df_XY3 = df_XY3.set_index([W, Z, 'EVENT_ID'])
df_XY3['Y_log'] = np.log(df_XY3[Y]).replace([np.inf, -np.inf], np.nan).fillna(0).astype(np.float64)
df_XY3 = df_XY3.drop(columns = [Y])
df_XY3 = df_XY3.drop(columns = ['DUID', 'PID', 'DUPERSID', 'EVNTIDX'])
df_XY3.info(verbose = True)

#### Create Outcome and predictor standard scaled numpy arrays for reference group (n_1, x_1, y_1)
df_XY3_1 = df_XY3[df_XY3['RACE'] == 2].dropna()
y3_1 = df_XY3_1.filter(['Y_log']).to_numpy()
x3_1 = StandardScaler().fit_transform(df_XY3_1.drop(columns = ['Y_log', 'RACE']).to_numpy())
n3_1 = df_XY3_1.index.to_numpy()

#### Create Outcome and predictor standard scaled numpy arrays for focus group (n_2, x_2, y_2)
df_XY3_2 = df_XY3[df_XY3['RACE'] == group_focus].dropna()
y3_2 = df_XY3_2.filter(['Y_log']).to_numpy()
x3_2 = StandardScaler().fit_transform(df_XY3_2.drop(columns = ['Y_log', 'RACE']).to_numpy())
n3_2 = df_XY3_2.index.to_numpy()

#### Train MLP on reference group
N_input = x3_1.shape[1] # Save number of columns as input dimension
N_nodes = round(N_input / 2) # Number of input dimensions divided by two for nodes in each layer
N_epochs = 100
network = Sequential() # Build Network with keras Sequential API
network.add(Dense(N_nodes, activation = 'relu', kernel_initializer = 'random_normal', input_dim = N_input)) # First dense layer
network.add(Dense(N_nodes, activation = 'relu', kernel_initializer = 'random_normal')) # Second dense layer
network.add(Dense(1, activation = 'linear', kernel_initializer = 'random_normal')) # Output layer with binary activation
network.compile(optimizer = 'adam', loss = 'mean_absolute_error', metrics = ['mean_squared_error']) # Compile network with Adaptive moment estimation, and follow loss and accuracy
history = network.fit(x3_1, y3_1, batch_size = 10, epochs = N_epochs) # Fitting the data to the train outcome, with batch size and number of epochs
result = pd.DataFrame({'Loss': history.history['loss']})
#with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
KOB_9b #result.to_excel(writer, sheet_name = label, index = False)

#### Predict reference group
df_XY3_1['Y_hat'] = network.predict(x3_1)
df_XY3_3 = df_XY3_1.filter(['Y_hat', W, Z]).groupby([W, Z], as_index = True).sum() # Keep selected columns and sum by key columns (keeping all as columns not index)
df_XY_3 = pd.merge(df_XY_1.reset_index(), df_XY3_3.reset_index(), on = [W, Z], how = 'left')
df_XY_3 = df_XY_3.fillna(0).astype(np.float64)
y_1_pred = df_XY_3['Y_hat']

#### Predict focus group
df_XY3_2['Y_hat'] = network.predict(x3_2)
df_XY3_3 = df_XY3_2.filter(['Y_hat', W, Z]).groupby([W, Z], as_index = True).sum() # Keep selected columns and sum by key columns (keeping all as columns not index)
df_XY_3 = pd.merge(df_XY_2.reset_index(), df_XY3_3.reset_index(), on = [W, Z], how = 'left')
df_XY_3 = df_XY_3.fillna(0).astype(np.float64)
y_2_pred = df_XY_3['Y_hat']

#### KOB Results
r2_score(y_1, y_1_pred)
KOB_9b = [np.mean(np.exp(y_1)),  np.mean(np.exp(y_2)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2))), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_pred)]

### MLP Using Diagnosis and ER Visit Data
model_9c = 'MLP Using ACA, Diagnosis, and ER Visit Data'
label = 'MLP_ER'

#### Extract ER Visit Data
QUERY = """
    SELECT
        2018 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , E.*
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
            AND Y.PRSTX18 = 1
            AND Y.INSCOV18 = 1
        ) SQ
    INNER JOIN (SELECT * FROM h206e WHERE EVNTIDX <> 'NONE') E
        ON SQ.DUPERSID = E.DUPERSID
"""
df_X3 = pd.read_sql_query(QUERY, db_con)
df_X3 = df_X3.dropna()
df_X3[W] = df_X3[W].astype('int64') # Change column data type to integer
df_X3[Z] = df_X3[Z].astype('int64') # Change column data type to integer
df_X3['EVENT_ID'] = df_X3['EVNTIDX'].astype('int64') # Change column data type to integer
df_XY3 = pd.merge(df_WXYZ, df_X3, on = [W, Z], how = 'inner')
df_XY3 = df_XY3.drop_duplicates(subset = [W, Z, 'EVENT_ID'])
df_XY3 = df_XY3.set_index([W, Z, 'EVENT_ID'])
df_XY3['Y_log'] = np.log(df_XY3[Y]).replace([np.inf, -np.inf], np.nan).fillna(0).astype(np.float64)
df_XY3 = df_XY3.drop(columns = [Y])
df_XY3 = df_XY3.drop(columns = ['DUID', 'PID', 'DUPERSID', 'EVNTIDX'])
df_XY3.info(verbose = True)

#### Create Outcome and predictor standard scaled numpy arrays for reference group (n_1, x_1, y_1)
df_XY3_1 = df_XY3[df_XY3['RACE'] == 2].dropna()
y3_1 = df_XY3_1.filter(['Y_log']).to_numpy()
x3_1 = StandardScaler().fit_transform(df_XY3_1.drop(columns = ['Y_log', 'RACE']).to_numpy())
n3_1 = df_XY3_1.index.to_numpy()

#### Create Outcome and predictor standard scaled numpy arrays for focus group (n_2, x_2, y_2)
df_XY3_2 = df_XY3[df_XY3['RACE'] == group_focus].dropna()
y3_2 = df_XY3_2.filter(['Y_log']).to_numpy()
x3_2 = StandardScaler().fit_transform(df_XY3_2.drop(columns = ['Y_log', 'RACE']).to_numpy())
n3_2 = df_XY3_2.index.to_numpy()

#### Train MLP on reference group
N_input = x3_1.shape[1] # Save number of columns as input dimension
N_nodes = round(N_input / 2) # Number of input dimensions divided by two for nodes in each layer
N_epochs = 100
network = Sequential() # Build Network with keras Sequential API
network.add(Dense(N_nodes, activation = 'relu', kernel_initializer = 'random_normal', input_dim = N_input)) # First dense layer
network.add(Dense(N_nodes, activation = 'relu', kernel_initializer = 'random_normal')) # Second dense layer
network.add(Dense(1, activation = 'linear', kernel_initializer = 'random_normal')) # Output layer with binary activation
network.compile(optimizer = 'adam', loss = 'mean_absolute_error', metrics = ['mean_squared_error']) # Compile network with Adaptive moment estimation, and follow loss and accuracy
history = network.fit(x3_1, y3_1, batch_size = 10, epochs = N_epochs) # Fitting the data to the train outcome, with batch size and number of epochs
result = pd.DataFrame({'Loss': history.history['loss']})
#with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
KOB_9c #result.to_excel(writer, sheet_name = label, index = False)

#### Predict reference group
df_XY3_1['Y_hat'] = network.predict(x3_1)
df_XY3_3 = df_XY3_1.filter(['Y_hat', W, Z]).groupby([W, Z], as_index = True).sum() # Keep selected columns and sum by key columns (keeping all as columns not index)
df_XY_3 = pd.merge(df_XY_1.reset_index(), df_XY3_3.reset_index(), on = [W, Z], how = 'left')
df_XY_3 = df_XY_3.fillna(0).astype(np.float64)
y_1_pred = df_XY_3['Y_hat']

#### Predict focus group
df_XY3_2['Y_hat'] = network.predict(x3_2)
df_XY3_3 = df_XY3_2.filter(['Y_hat', W, Z]).groupby([W, Z], as_index = True).sum() # Keep selected columns and sum by key columns (keeping all as columns not index)
df_XY_3 = pd.merge(df_XY_2.reset_index(), df_XY3_3.reset_index(), on = [W, Z], how = 'left')
df_XY_3 = df_XY_3.fillna(0).astype(np.float64)
y_2_pred = df_XY_3['Y_hat']

#### KOB Results
r2_score(y_1, y_1_pred)
KOB_9c = [np.mean(np.exp(y_1)),  np.mean(np.exp(y_2)), np.mean(np.exp(y_2_pred)), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2))), (np.mean(np.exp(y_1)) - np.mean(np.exp(y_2_pred))), r2_score(y_1, y_1_pred)]

### Export to Summary File
text_md = open('_docs//' + label_name + '//' + label_run + '//summary.md', 'a')
text_md.write('#### ' + step_4 + '\n')
text_md.write(method_4 + '<br>\n')
text_md.write('\n')
text_md.write('For training results, see ' + '_fig//' + label_name + '//' + label_run + '//results.xlsx' + '\n')
text_md.write('\n')
text_md.write('##### ' + model_10 + '\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_10) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_9a + '\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_9a) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_9b + '\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_9b) + '<br>\n')
text_md.write('\n')
text_md.write('##### ' + model_9c + '\n')
text_md.write('\n')
text_md.write('Kitigawa Decomposition: ' + str(KOB_9c) + '<br>\n')
text_md.write('\n')
text_md.close() # Close file

### Save Results
label = 'KOB'
ls_model = [[model_1a, model_1b], model_2, model_3, model_4, model_5, model_6, model_7, model_8, model_9a, model_9b, model_9c]
ls_KOB = [KOB_1, KOB_2, KOB_3, KOB_4, KOB_5, KOB_6, KOB_7, KOB_8, KOB_9a, KOB_9b, KOB_9c]
result = pd.DataFrame({'White_NonWhite_Predicted_Difference_UnExplained_Rsq': ls_KOB, 'Machine Learning Model': ls_model})
result.to_csv('_data//' + label_name + '//' + label_run + '//results_Q2.csv', index = False)
#with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
KOB_ #result.to_excel(writer, sheet_name = label, index = False)