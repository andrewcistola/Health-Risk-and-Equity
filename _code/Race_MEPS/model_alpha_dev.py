# Mahcine Learning Script

## Mahcine Learning Step 1: Data Processing of Predictors and Outcomes
step_1 = 'Mahcine Learning Step 1: Data Processing of Predictors and Outcomes'
methods_1 = 'Various machine learning models were trained on a reference population and then used to predict values from a focus populaiton. The difference in predicted to actual values for the focus group then to reflects the impact of group identification. This is an adaptation of the Kitigawa-Oaxaca-Blinder method.'
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
text_md.write('The following results used the scikit-learn library collected for Python version ' + str(sys.version) + '\n')
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
model_1 = 'Principal Component Analysis'
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
model_2 = 'K-Means'
label = 'KMeans'
kmeans = KMeans()
kmeans.fit(x_1)
result = df_XY_1
result['Clusters'] = kmeans.labels_
with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer: 
    result.to_excel(writer, sheet_name = label, index = False)

### Linear regression model with standard variables
model_3 = 'Linear Regression'
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
model_3 = 'Linear Regression'
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
text_md.write('##### ' + model_1 + '\n')
text_md.write('See ' + '_fig//' + label_name + '//' + label_run + '//results.xlsx' + '\n')
text_md.write('\n')
text_md.write('##### ' + model_2 + '\n')
text_md.write('See ' + '_fig//' + label_name + '//' + label_run + '//results.xlsx' + '\n')
text_md.write('\n')
text_md.write('##### ' + model_3 + '\n')
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
model_1 = 'Random Forests'
label = 'RandomForest'
forest = RandomForestRegressor(n_estimators = 1000, max_depth = 10) #Use default values except for number of trees. For a further explanation see readme included in repository. 
forest.fit(x_1, y_1) # Fit Forest model, This will take time
result = pd.DataFrame({'Variables': X, 'Importances': forest.feature_importances_})
RSQ_1 = forest.score(x_1, y_1) # rsq value
y_2_pred = forest.predict(x_2)
ABS_1 = np.mean(y_1) - np.mean(y_2)
KOB_1 = np.mean(y_2_pred) - np.mean(y_2)
with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
        result.to_excel(writer, sheet_name = label, index = False)

### Recursive Feature Elimination
model_2 = 'Recursive feature Elimination'
label = "RFE-CV"
recursive = RFECV(estimator = LinearRegression(), min_features_to_select = 5) # define selection parameters, in this case all features are selected. See Readme for more ifo
recursive.fit(x_1, y_1) # This will take time
result = pd.DataFrame({'Variables': X, 'Rankings': recursive.ranking_})
RSQ_2 = recursive.score(x_1, y_1) # rsq value
y_2_pred = recursive.predict(x_2)
ABS_2 = np.mean(y_1) - np.mean(y_2)
KOB_2 = np.mean(y_2_pred) - np.mean(y_2)
with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
        result.to_excel(writer, sheet_name = label, index = False)

### Support Vector Machines
model_3 = 'Support Vector Machines'
label = 'SVM'
vector = LinearSVR() # Support vector machines with a linear kernel for multi-level categorical outrcomes
vector.fit(x_1, y_1) # fit model
result = pd.DataFrame({'Variables': X, 'Vectors': vector.coef_})
RSQ_3 = vector.score(x_1, y_1) # rsq value
y_2_pred = vector.predict(x_2)
ABS_3 = np.mean(y_1) - np.mean(y_2)
KOB_3 = np.mean(y_2_pred) - np.mean(y_2)
with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'a', engine = 'openpyxl', if_sheet_exists = 'replace') as writer:  
        result.to_excel(writer, sheet_name = label, index = False)

### Export to Summary File
text_md = open('_docs//' + label_name + '//' + label_run + '//summary.md', 'a')
text_md.write('#### ' + step_3 + '\n')
text_md.write(method_3 + '\n')
text_md.write('For feature selection results, see ' + '_fig//' + label_name + '//' + label_run + '//results.xlsx' + '\n')
text_md.write('\n')
text_md.write('##### ' + model_1 + '\n')
text_md.write('Reference Group Rsq: ' + str(RSQ_1) + '\n')
text_md.write('Absolute difference between groups: ' + str(ABS_1) + '\n')
text_md.write('Difference attributable to groups: ' + str(KOB_1) + '\n')
text_md.write('\n')
text_md.write('##### ' + model_2 + '\n')
text_md.write('Reference Group Rsq: ' + str(RSQ_2) + '\n')
text_md.write('Absolute difference between groups: ' + str(ABS_2) + '\n')
text_md.write('Difference attributable to groups: ' + str(KOB_2) + '\n')
text_md.write('\n')
text_md.write('##### ' + model_3 + '\n')
text_md.write('Reference Group Rsq: ' + str(RSQ_3) + '\n')
text_md.write('Absolute difference between groups: ' + str(ABS_3) + '\n')
text_md.write('Difference attributable to groups: ' + str(KOB_3) + '\n')
text_md.write('\n')
text_md.close() # Close file

### Multi-Layered Perceptron with complete predictors

QUERY = """
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , D.*
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
            AND Y.PRSTX20 = 1
            AND Y.INSCOV20 = 1
        ) SQ
    INNER JOIN (SELECT * FROM h220d WHERE EVNTIDX <> 'NONE') D
        ON SQ.DUPERSID = D.DUPERSID
UNION
    SELECT
        2019 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , D.*
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h216 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
            AND Y.PRSTX19 = 1
            AND Y.INSCOV19 = 1
        ) SQ
    INNER JOIN (SELECT * FROM h213d WHERE EVNTIDX <> 'NONE') D
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

### Create Outcome and predictor standard scaled numpy arrays for reference group (n_1, x_1, y_1)
df_XY3_1 = df_XY3[df_XY3['RACE'] == 2].dropna()
y3_1 = df_XY3_1.filter(Y).to_numpy()
x3_1 = StandardScaler().fit_transform(df_XY3_1.drop(columns = [Y]).to_numpy())
n3_1 = df_XY3_1.index.to_numpy()

### Create Outcome and predictor standard scaled numpy arrays for focus group (n_2, x_2, y_2)
df_XY3_2 = df_XY3[df_XY3['RACE'] != 2].dropna()
y3_2 = df_XY3_2.filter([Y]).to_numpy()
x3_2 = StandardScaler().fit_transform(df_XY3_2.drop(columns = [Y]).to_numpy())
n3_2 = df_XY3_2.index.to_numpy()

### Train MLP on reference group
input = x3_1.shape[1] # Save number of columns as input dimension
nodes = round(input / 2) # Number of input dimensions divided by two for nodes in each layer
epochs = 100
network = Sequential() # Build Network with keras Sequential API
network.add(Dense(nodes, activation = 'relu', kernel_initializer = 'random_normal', input_dim = input)) # First dense layer
network.add(Dense(nodes, activation = 'relu', kernel_initializer = 'random_normal')) # Second dense layer
network.add(Dense(1, activation = 'sigmoid', kernel_initializer = 'random_normal')) # Output layer with binary activation
network.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy']) # Compile network with Adaptive moment estimation, and follow loss and accuracy
history = network.fit(x3_1, y3_1, batch_size = 10, epochs = epochs) # Fitting the data to the train outcome, with batch size and number of epochs
result_7 = history.history['loss']
RSQ_7 = network.score(x3_1, y3_1) # rsq value

### Predict focus group
y3_2_pred = network.predict(x3_2) # Predict values from test data
ABS_7 = np.mean(y3_1) - np.mean(y3_2)
KOB_7 = np.mean(y3_2_pred) - np.mean(y3_2)
