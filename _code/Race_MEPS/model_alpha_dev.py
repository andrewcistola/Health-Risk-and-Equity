# Mahcine Learning Script

## Mahcine Learning Step 1: Data Processing of Predictors and Outcomes
step_1 = 'Mahcine Learning Step 1: Data Processing of Predictors and Outcomes'
method_1 = 'Various machine learning models were trained on a reference population and then used to predict values from a focus populaiton. The difference in predicted to actual values for the focus group then to reflects the impact of group identification. This is an adaptation of the Kitigawa-Oaxaca-Blinder method.'
group_1 = 'Non-Hispanic White (RACETH = 2)'
group_2 = 'Hispanic, Black, Asian, or Other (RACETH <> 2)'
W = 'PERSON_ID'
X_label = 'RACE, AGE, SEX, ICD10_TOTAL, ICD10_YN, VISITS_TOTAL, VISITS_X_TYPE, PAID_X_TYPE'
Y = 'PAID_TOTAL'
Z = 'YEAR'

### Import Labels/Demographics (W) with Predictors (X) Outcomes (Y) and Shapes/Subgroups (Z)
df_WXYZ = pd.read_csv('_data//' + label_name + '//' + label_run + '//analytical_Q2.csv')

### Define Predictors from imported data (X)
X = df_WXYZ.drop(columns = [W, Y, Z]).columns.to_list()

### Create Outcome-Predictor pandas dataframe (XY)
df_XY = df_WXYZ.set_index([W, Z]) # Reset Index
df_XY['Y_log'] = np.log(df_XY[Y]).replace([np.inf, -np.inf], np.nan).fillna(0).astype(np.float64)
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
df_XY_2 = df_XY[df_XY['RACE'] != 2].dropna()
y_2 = df_XY_2.filter(['Y_log']).to_numpy()
x_2 = StandardScaler().fit_transform(df_XY_2.filter(X).to_numpy())
n_2 = df_XY_2.index.to_numpy()

### Export to Summary File
text_md = open('_docs//' + label_name + '//' + label_run + '//summary.md', 'a')
text_md.write('### ' + 'Machine Learning Result Summary' + '\n')
text_md.write(method_1 + '\n')
text_md.write('Reference group: ' + group_1 + '\n')
text_md.write('Focus group: ' + group_2 + '\n')
text_md.write('The following results used the scikit-learn and keras libraries for Python version ' + str(sys.version) + '\n')
text_md.write('\n')
text_md.write('#### ' + step_1 + '\n')
text_md.write('Source: ' + '_data//' + label_name + '//' +  label_run + '//analytical_Q2.csv' + '\n')
text_md.write('\n')
text_md.write('W (ID variables): ' + W + '\n')
text_md.write('X (Predictor variables): ' + X_label + '\n')
text_md.write('Y (Outcome variables): ' + Y + '\n')
text_md.write('Z (Subgroup variables): ' + Z + '\n')
text_md.write('\n')
text_md.write(info_WXYZ)
text_md.write('\n')
text_md.close() # Close file

## Learn Step 2: Manual Feature Selection
step_2 = 'Learn Step 2: Manual Feature Selection Assisted with Unsupervised Learning' 
method_2 = 'Unsupervised learning models are used to review predictors for inclusion in a regression model. The regression model is trained on the reference group and predicts values for the focus group. The difference in predicted to actual values represents what is explained by group identififcation independent of the predictors.'

### Principal Component Analysis
model_1a = 'Principal Component Analysis'
label = 'PCA'
pca = PCA(n_components = 'mle') # Pass the number of components to make PCA model based on degrees of freedom
pca.fit_transform(x_1) # finally call fit_transform on the aggregate data to create PCA results object
result = pd.DataFrame(pca.components_, columns = X) # Export eigenvectors to data frame with column names from original data
result["Variance_Ratio"] = pca.explained_variance_ratio_ # Save eigenvalues as their own column
result = result.set_index(["Variance_Ratio"])
result = result.transpose()
with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
        result.to_excel(writer, sheet_name = label, index = False)

### K-means
model_1b = 'K-Means'
label = 'KMeans'
kmeans = KMeans()
kmeans.fit(x_1)
result = df_XY_1
result['Clusters'] = kmeans.labels_
with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer: 
    result.to_excel(writer, sheet_name = label, index = False)

### Linear regression model with standard variables
model_2 = 'Linear Regression'
label = 'OLS'
X_ACA = ['AGE', 'SEX', 'FPL_PERCENT', 'ICD10_TOTAL']
x_1_ACA = StandardScaler().fit_transform(df_XY_1.filter(X_ACA).to_numpy())
x_2_ACA = StandardScaler().fit_transform(df_XY_2.filter(X_ACA).to_numpy())
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x_1_ACA, y_1) # Fit model
result_1 = pd.DataFrame(OLS.coef_, columns = X_ACA)
RSQ_1 = OLS.score(x_1_ACA, y_1) # rsq value
y_2_pred = OLS.predict(x_2_ACA)
ABS_1 = np.mean(y_1) - np.mean(y_2)
KOB_1 = np.mean(y_2_pred) - np.mean(y_2)

### Linear regression model with hand selected variables
model_2 = 'Linear Regression'
label = 'OLS'
X_hand = ['AGE', 'SEX', 'ICD10_TOTAL', 'VISITS_TOTAL', 'ER_PAID', 'OFFICE_PAID']
x_1_hand = StandardScaler().fit_transform(df_XY_1.filter(X_hand).to_numpy())
x_2_hand = StandardScaler().fit_transform(df_XY_2.filter(X_hand).to_numpy())
OLS = LinearRegression() # Linear Regression in scikit learn
OLS.fit(x_1_hand, y_1) # Fit model
result_2 = pd.DataFrame(OLS.coef_, columns = X_hand)
RSQ_2 = OLS.score(x_1_hand, y_1) # rsq value
y_2_pred = OLS.predict(x_2_hand)
ABS_2 = np.mean(y_1) - np.mean(y_2)
KOB_2 = np.mean(y_2_pred) - np.mean(y_2)

### Export to Summary File
text_md = open('_docs//' + label_name + '//' + label_run + '//summary.md', 'a')
text_md.write('#### ' + step_2 + '\n')
text_md.write(method_2 + '\n')
text_md.write('\n')
text_md.write('##### ' + model_1a + '\n')
text_md.write('See ' + '_fig//' + label_name + '//' + label_run + '//results.xlsx' + '\n')
text_md.write('\n')
text_md.write('##### ' + model_1b + '\n')
text_md.write('See ' + '_fig//' + label_name + '//' + label_run + '//results.xlsx' + '\n')
text_md.write('\n')
text_md.write('##### ' + model_2 + '\n')
text_md.write('Regression Model using hand selected variables: ' + '\n')
text_md.write('\n')
text_md.write('Rsq: ' + str(RSQ_1) + '\n')
text_md.write('\n')
text_md.write(str(result_1) + '\n')
text_md.write('\n')
text_md.write('Absolute difference between groups: ' + str(ABS_1) + '\n')
text_md.write('Difference attributable to groups: ' + str(KOB_1) + '\n')
text_md.write('\n')
text_md.write('Regression Model using hand selected variables: ' + '\n')
text_md.write('\n')
text_md.write('Rsq: ' + str(RSQ_2) + '\n')
text_md.write('\n')
text_md.write(str(result_2) + '\n')
text_md.write('\n')
text_md.write('Absolute difference between groups: ' + str(ABS_2) + '\n')
text_md.write('Difference attributable to groups: ' + str(KOB_2) + '\n')
text_md.write('\n')
text_md.close() # Close file

## Learn Step 3: Automated Feature Selection
step_3 = 'Learn Step 3: Automated Feature Selection Assisted with Supervised Learning' 
method_3 = 'Supervised algorithms are used to automatically identify relevant features and predict outcomes. These models allow for the inclusion of more data in closer to raw form than OLS. The models are trained on the reference group and then predict values for the focus group. The difference in predicted to actual values represents what is explained by group identififcation independent of the predictors.'

### Random Forest Regressor
model_3 = 'Random Forests'
label = 'RandomForest'
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
RSQ_3 = forest.score(x_1, y_1) # rsq value
y_2_pred = forest.predict(x_2)
ABS_3 = np.mean(y_1) - np.mean(y_2)
KOB_3 = np.mean(y_2_pred) - np.mean(y_2)
with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
        result.to_excel(writer, sheet_name = label, index = False)

### Recursive Feature Elimination
model_4 = 'Recursive feature Elimination'
label = "RFE-CV"
recursive = RFECV(estimator = LinearRegression(), min_features_to_select = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
recursive.fit(x_1, y_1) # This will take time
result = pd.DataFrame({'Variables': X, 'Rankings': recursive.ranking_})
RSQ_4 = recursive.score(x_1, y_1) # rsq value
y_2_pred = recursive.predict(x_2)
ABS_4 = np.mean(y_1) - np.mean(y_2)
KOB_4 = np.mean(y_2_pred) - np.mean(y_2)
with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
        result.to_excel(writer, sheet_name = label, index = False)

### Support Vector Machines
model_5 = 'Support Vector Machines'
label = 'SVM'
vector = LinearSVR() # Support vector machines with a linear kernel for multi-level categorical outrcomes
vector.fit(x_1, y_1) # fit model
result = pd.DataFrame({'Variables': X, 'Vectors': vector.coef_})
RSQ_5 = vector.score(x_1, y_1) # rsq value
y_2_pred = vector.predict(x_2)
ABS_5 = np.mean(y_1) - np.mean(y_2)
KOB_5 = np.mean(y_2_pred) - np.mean(y_2)
with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
        result.to_excel(writer, sheet_name = label, index = False)

### Export to Summary File
text_md = open('_docs//' + label_name + '//' + label_run + '//summary.md', 'a')
text_md.write('#### ' + step_3 + '\n')
text_md.write(method_3 + '\n')
text_md.write('For feature selection results, see ' + '_fig//' + label_name + '//' + label_run + '//results.xlsx' + '\n')
text_md.write('\n')
text_md.write('##### ' + model_3 + '\n')
text_md.write('Reference Group Rsq: ' + str(RSQ_3) + '\n')
text_md.write('Absolute difference between groups: ' + str(ABS_3) + '\n')
text_md.write('Difference attributable to groups: ' + str(KOB_3) + '\n')
text_md.write('\n')
text_md.write('##### ' + model_4 + '\n')
text_md.write('Reference Group Rsq: ' + str(RSQ_4) + '\n')
text_md.write('Absolute difference between groups: ' + str(ABS_4) + '\n')
text_md.write('Difference attributable to groups: ' + str(KOB_4) + '\n')
text_md.write('\n')
text_md.write('##### ' + model_5 + '\n')
text_md.write('Reference Group Rsq: ' + str(RSQ_5) + '\n')
text_md.write('Absolute difference between groups: ' + str(ABS_5) + '\n')
text_md.write('Difference attributable to groups: ' + str(KOB_5) + '\n')
text_md.write('\n')
text_md.close() # Close file

## Learn Step 4: Deep Learning with Expanded predictors
step_4 = 'Learn Step 4: Deep Learning with Expanded predictors' 
method_4 = 'Deep learning algorithms are used for an expanded set of predictors in raw format. These models allow for virtually all structured data without processing and can handle complex interactions not yet understood. The models are trained on the reference group and then predict values for the focus group. The difference in predicted to actual values represents what is explained by group identififcation independent of the predictors.'

### MLP Using ACA and Diagnosis Data
model_6 = 'MLP Using ACA Data'
label = 'MLP_ACA'
df_XY3 = df_XY.loc[:, df_XY.columns.str.contains('YEAR|AGE|SEX|RACE|FPL_PERCENT|Y_log')]
df_XY3.info(verbose = True)

#### Create Outcome and predictor standard scaled numpy arrays for reference group (n_1, x_1, y_1)
df_XY3_1 = df_XY3[df_XY3['RACE'] == 2].dropna()
y3_1 = df_XY3_1.filter(['Y_log']).to_numpy()
x3_1 = StandardScaler().fit_transform(df_XY3_1.drop(columns = ['Y_log', 'RACE']).to_numpy())
n3_1 = df_XY3_1.index.to_numpy()

#### Create Outcome and predictor standard scaled numpy arrays for focus group (n_2, x_2, y_2)
df_XY3_2 = df_XY3[df_XY3['RACE'] != 2].dropna()
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
with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
        result.to_excel(writer, sheet_name = label, index = False)

### Predict focus group
y3_2_pred = network.predict(x3_2) # Predict values from test data
ABS_6 = np.mean(y3_1) - np.mean(y3_2)
KOB_6 = np.mean(y3_2_pred) - np.mean(y3_2)
KOB_6

### MLP Using ACA and Diagnosis Data
model_7 = 'MLP Using ACA and Diagnosis Data'
label = 'MLP_DX'
df_XY3 = df_XY.loc[:, df_XY.columns.str.contains('YEAR|AGE|SEX|RACE|FPL_PERCENT|ICD10|Y_log')]
df_XY3.info(verbose = True)

#### Create Outcome and predictor standard scaled numpy arrays for reference group (n_1, x_1, y_1)
df_XY3_1 = df_XY3[df_XY3['RACE'] == 2].dropna()
y3_1 = df_XY3_1.filter(['Y_log']).to_numpy()
x3_1 = StandardScaler().fit_transform(df_XY3_1.drop(columns = ['Y_log', 'RACE']).to_numpy())
n3_1 = df_XY3_1.index.to_numpy()

#### Create Outcome and predictor standard scaled numpy arrays for focus group (n_2, x_2, y_2)
df_XY3_2 = df_XY3[df_XY3['RACE'] != 2].dropna()
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
with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
        result.to_excel(writer, sheet_name = label, index = False)

### Predict focus group
y3_2_pred = network.predict(x3_2) # Predict values from test data
ABS_7 = np.mean(y3_1) - np.mean(y3_2)
KOB_7 = np.mean(y3_2_pred) - np.mean(y3_2)
KOB_7

### MLP Using Diagnosis and Office Visit Data

#### Extract Office Visit Data
model_8 = 'MLP Using ACA, Diagnosis, and Office Visit Data'
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
df_XY3_1 = df_XY3[df_XY3['RACE'] == 2].dropna()
y3_1 = df_XY3_1.filter(['Y_log']).to_numpy()
x3_1 = StandardScaler().fit_transform(df_XY3_1.drop(columns = ['Y_log', 'RACE']).to_numpy())
n3_1 = df_XY3_1.index.to_numpy()

#### Create Outcome and predictor standard scaled numpy arrays for focus group (n_2, x_2, y_2)
df_XY3_2 = df_XY3[df_XY3['RACE'] != 2].dropna()
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
with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
        result.to_excel(writer, sheet_name = label, index = False)

#### Predict focus group
y3_2_pred = network.predict(x3_2) # Predict values from test data
ABS_8 = np.mean(y3_1) - np.mean(y3_2)
KOB_8 = np.mean(y3_2_pred) - np.mean(y3_2)
KOB_8


### MLP Using Diagnosis and Hospital Visit Data
model_9 = 'MLP Using ACA, Diagnosis, and Hospital Visit Data'
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
df_XY3_2 = df_XY3[df_XY3['RACE'] != 2].dropna()
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
with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
        result.to_excel(writer, sheet_name = label, index = False)

#### Predict focus group
y3_2_pred = network.predict(x3_2) # Predict values from test data
ABS_9 = np.mean(y3_1) - np.mean(y3_2)
KOB_9 = np.mean(y3_2_pred) - np.mean(y3_2)
KOB_9

### MLP Using Diagnosis and ER Visit Data
model_10 = 'MLP Using ACA, Diagnosis, and ER Visit Data'
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
df_XY3_2 = df_XY3[df_XY3['RACE'] != 2].dropna()
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
with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
        result.to_excel(writer, sheet_name = label, index = False)

#### Predict focus group
y3_2_pred = network.predict(x3_2) # Predict values from test data
ABS_10 = np.mean(y3_1) - np.mean(y3_2)
KOB_10 = np.mean(y3_2_pred) - np.mean(y3_2)
KOB_10

### Export to Summary File
text_md = open('_docs//' + label_name + '//' + label_run + '//summary.md', 'a')
text_md.write('#### ' + step_4 + '\n')
text_md.write(method_4 + '\n')
text_md.write('For training results, see ' + '_fig//' + label_name + '//' + label_run + '//results.xlsx' + '\n')
text_md.write('\n')
text_md.write('##### ' + model_6 + '\n')
text_md.write('Absolute difference between groups: ' + str(ABS_1) + '\n')
text_md.write('Difference attributable to groups: ' + str(KOB_1) + '\n')
text_md.write('\n')
text_md.write('##### ' + model_7 + '\n')
text_md.write('Absolute difference between groups: ' + str(ABS_2) + '\n')
text_md.write('Difference attributable to groups: ' + str(KOB_2) + '\n')
text_md.write('\n')
text_md.write('##### ' + model_8 + '\n')
text_md.write('Absolute difference between groups: ' + str(ABS_3) + '\n')
text_md.write('Difference attributable to groups: ' + str(KOB_3) + '\n')
text_md.write('\n')
text_md.write('##### ' + model_9 + '\n')
text_md.write('Absolute difference between groups: ' + str(ABS_3) + '\n')
text_md.write('Difference attributable to groups: ' + str(KOB_3) + '\n')
text_md.write('\n')
text_md.write('##### ' + model_10 + '\n')
text_md.write('Absolute difference between groups: ' + str(ABS_3) + '\n')
text_md.write('Difference attributable to groups: ' + str(KOB_3) + '\n')
text_md.write('\n')
text_md.close() # Close file