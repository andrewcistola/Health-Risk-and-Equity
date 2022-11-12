# Calc

## Import
df_WXYZ = pd.read_csv('_data//' + label_name + '//' + label_run + '//clean.csv', encoding = 'ISO-8859-1')
df_WXYZ.info()

## Split into sperate tables

### Unique Demographics
df_W = df_WXYZ.filter(['PERSON_ID', 'YEAR', 'AGE', 'SEX', 'RACE', 'FPL_PERCENT']).drop_duplicates()
df_W['YEAR'] = df_W['YEAR'].astype('int64') # Change column data type to integer
df_W['PERSON_ID'] = df_W['PERSON_ID'].astype('int64') # Change column data type to integer
df_W.info()

### ICD10X in Yes/No format
df_X1 = df_WXYZ.filter(['PERSON_ID', 'YEAR', 'ICD10']).drop_duplicates()
df_X1 = pd.get_dummies(df_X1, columns = ['ICD10'])
df_X1['YEAR'] = df_X1['YEAR'].astype('int64') # Change column data type to integer
df_X1['PERSON_ID'] = df_X1['PERSON_ID'].astype('int64') # Change column data type to integer
df_X1.info()

### Condition Count by individual per year
df_X2 = df_WXYZ.filter(['PERSON_ID', 'YEAR', 'ICD10']).drop_duplicates().groupby(['YEAR', 'PERSON_ID'], as_index = False).count() # Keep selected columns and count unique by key columns (keeping all as columns not index)
df_X2 = df_X2.rename(columns = {'ICD10': 'ICD10_TOTAL'})
df_X2['YEAR'] = df_X2['YEAR'].astype('int64') # Change column data type to integer
df_X2['PERSON_ID'] = df_X2['PERSON_ID'].astype('int64') # Change column data type to integer
df_X2.info()

### Payments by setting type
df_Y1 = df_WXYZ.filter(['YEAR', 'PERSON_ID', 'PAID', 'SETTING']).groupby(['YEAR', 'PERSON_ID', 'SETTING'], as_index = False).sum()
df_Y1 = df_Y1.pivot(index = ['YEAR', 'PERSON_ID'], columns = 'SETTING', values = 'PAID').reset_index() # Pivot from long to wide
df_Y1 = df_Y1.rename(columns = {'ER': 'ER_PAID', 'HOME': 'HOME_PAID', 'INPATIENT': 'INPATIENT_PAID', 'OFFICE': 'OFFICE_PAID', 'OUTPATIENT': 'OUTPATIENT_PAID', 'RX': 'RX_PAID'})
df_Y1 = df_Y1.fillna(0).astype(np.int64) # Change missing vlaues to int64 zeros
df_Y1['YEAR'] = df_Y1['YEAR'].astype('int64') # Change column data type to integer
df_Y1['PERSON_ID'] = df_Y1['PERSON_ID'].astype('int64') # Change column data type to integer
df_Y1.info()

### Total payments by individual per year
df_Y2 = df_WXYZ.filter(['YEAR', 'PERSON_ID', 'PAID']).groupby(['YEAR', 'PERSON_ID'], as_index = False).sum()
df_Y2 = df_Y2.rename(columns = {'PAID': 'PAID_TOTAL'})
df_Y2['YEAR'] = df_Y2['YEAR'].astype('int64') # Change column data type to integer
df_Y2['PERSON_ID'] = df_Y2['PERSON_ID'].astype('int64') # Change column data type to integer
df_Y2.info()

### Visits by setting type
df_Z1 = df_WXYZ.filter(['YEAR', 'PERSON_ID', 'SETTING', 'EVENT_ID']).groupby(['YEAR', 'PERSON_ID', 'SETTING'], as_index = False).count()
df_Z1 = df_Z1.pivot(index = ['YEAR', 'PERSON_ID'], columns = 'SETTING', values = 'EVENT_ID').reset_index() # Pivot from long to wide
df_Z1 = df_Z1.rename(columns = {'ER': 'ER_VISITS', 'HOME': 'HOME_VISITS', 'INPATIENT': 'INPATIENT_VISITS', 'OFFICE': 'OFFICE_VISITS', 'OUTPATIENT': 'OUTPATIENT_VISITS', 'RX': 'RX_VISITS'})
df_Z1 = df_Z1.fillna(0).astype(np.int64) # Change missing vlaues to int64 zeros
df_Z1['YEAR'] = df_Z1['YEAR'].astype('int64') # Change column data type to integer
df_Z1['PERSON_ID'] = df_Z1['PERSON_ID'].astype('int64') # Change column data type to integer
df_Z1.info()

### Total visits by individual per year
df_Z2 = df_WXYZ.filter(['YEAR', 'PERSON_ID', 'SETTING']).groupby(['YEAR', 'PERSON_ID'], as_index = False).count()
df_Z2 = df_Z2.rename(columns = {'SETTING': 'VISITS_TOTAL'})
df_Z2['YEAR'] = df_Z2['YEAR'].astype('int64') # Change column data type to integer
df_Z2['PERSON_ID'] = df_Z2['PERSON_ID'].astype('int64') # Change column data type to integer
df_Z2.info()

### Calculate Risk Scores

### Uniquie Age, Sex, ICD10X for risk score calc
df_X3 = df_WXYZ.filter(['PERSON_ID', 'YEAR', 'AGE', 'SEX', 'FPL_PERCENT', 'ICD10']).drop_duplicates()
df_X3.info()

#Import DIY
#Modify for ICD10X
#df_X3 = pd.merge(df_X3, df_DIY, on = 'ICD10X')
#for row in iterrows:
#    if 'AGE' > 'AGE_MAX' then 'CC' == NULL
#    elif 'AGE' < 'AGE_MIN' then 'CC' == NULL
#    elif 'AGE' > 'DX_MAX' then 'CC' == NULL
#    elif 'AGE' < 'DX_MIN' then 'CC' == NULL
#    elif 'SEX' != 'DX_SEX' then 'CC' == NULL

#Add RXCs
#Transform
#Apply hierarchy
#Groupings
#Demo terms
#Apply 2020 Silver Weights
#CSR Adjustment

df_X3 = df_X3.fillna(0).astype(np.int64) # Change missing vlaues to int64 zeros
df_X3 = df_X3.filter(['PERSON_ID', 'YEAR', 'UNADJ_RS', 'ADJ_RS'])
df_X3['YEAR'] = df_X3['YEAR'].astype('int64') # Change column data type to integer
df_X3['PERSON_ID'] = df_X3['PERSON_ID'].astype('int64') # Change column data type to integer
df_X3.info()

## Assmeble Analytical Files

### Q1: Regression Model for Paid Claims Cost using demographics and risk score
df_Q1 = pd.merge(df_W, df_X2, on = ['PERSON_ID', 'YEAR'], how = 'inner')
df_Q1 = pd.merge(df_Q1, df_Y2, on = ['PERSON_ID', 'YEAR'], how = 'left')
df_Q1 = pd.merge(df_Q1, df_Z2, on = ['PERSON_ID', 'YEAR'], how = 'left')
df_Q1.to_csv('_data//' + label_name + '//' + label_run + '//analytical_Q1.csv', index = False)
df_Q1.info()

### Save datafram info for output
buffer = io.StringIO()
df_Q1.info(verbose = True, buf = buffer, show_counts = True)
info_Q1 = buffer.getvalue()

### Q2: Preidction Model for Paid Claims Cost using ICD10 Codes, Visits, and Payments
df_Q2 = pd.merge(df_W, df_X2, on = ['PERSON_ID', 'YEAR'], how = 'inner')
df_Q2 = pd.merge(df_Q2, df_Y1, on = ['PERSON_ID', 'YEAR'], how = 'left')
df_Q2 = pd.merge(df_Q2, df_Y2, on = ['PERSON_ID', 'YEAR'], how = 'left')
df_Q2 = pd.merge(df_Q2, df_Z1, on = ['PERSON_ID', 'YEAR'], how = 'left')
df_Q2 = pd.merge(df_Q2, df_Z2, on = ['PERSON_ID', 'YEAR'], how = 'left')
df_Q2 = pd.merge(df_Q2, df_X1, on = ['PERSON_ID', 'YEAR'], how = 'left')
df_Q2 = df_Q2.groupby(['PERSON_ID', 'YEAR'], as_index = False).max()
df_Q2.to_csv('_data//' + label_name + '//' + label_run + '//analytical_Q2.csv', index = False)
df_Q2.info()

### Save dataframe info for output
df_Q2 = df_Q2.replace(0, np.nan) # Replace infitite values with missing value
buffer = io.StringIO()
df_Q2.info(verbose = True, buf = buffer, show_counts = True)
info_Q2 = buffer.getvalue()
df_Q2 = df_Q2.replace(np.nan, 0) # Replace infitite values with missing value

### Gather Descriptive Statistics
df_Q1['PERCENT_FEMALE'] = np.where(df_Q1['SEX'] == 1, 0, 
                                np.where(df_Q1['SEX'] == 2, 1,
                                    'MISSING')) # Create column based on conditions
df_Q1['PERCENT_FEMALE'] = df_Q1['PERCENT_FEMALE'].astype('int64') # Change column data type to integer
df_Q1['RACE_DESC'] = np.where(df_Q1['RACE'] == 1, 'HISPANIC', 
                                np.where(df_Q1['RACE'] == 2, 'WHITE',
                                    np.where(df_Q1['RACE'] == 3, 'BLACK',
                                        np.where(df_Q1['RACE'] == 4, 'ASIAN',
                                            np.where(df_Q1['RACE'] == 4, 'OTHER',
                                                'MISSING'))))) # Create column based on conditions
result_01 = df_Q1.filter(['YEAR', 'AGE']).groupby(['YEAR']).describe() 
result_02 = df_Q1.filter(['YEAR', 'RACE_DESC', 'AGE']).groupby(['YEAR', 'RACE_DESC']).describe() 
result_03 = df_Q1.filter(['YEAR', 'PERCENT_FEMALE']).groupby(['YEAR']).describe() 
result_04 = df_Q1.filter(['YEAR', 'RACE_DESC', 'PERCENT_FEMALE']).groupby(['YEAR', 'RACE_DESC']).describe() 
result_05 = df_Q1.filter(['YEAR', 'FPL_PERCENT']).groupby(['YEAR']).describe()
result_06 = df_Q1.filter(['YEAR', 'RACE_DESC', 'FPL_PERCENT']).groupby(['YEAR', 'RACE_DESC']).describe() 
result_07 = df_Q1.filter(['YEAR', 'ICD10_TOTAL']).groupby(['YEAR']).describe() 
result_08 = df_Q1.filter(['YEAR', 'RACE_DESC', 'ICD10_TOTAL']).groupby(['YEAR', 'RACE_DESC']).describe() 
result_09 = df_Q1.filter(['YEAR', 'PAID_TOTAL']).groupby(['YEAR']).describe()
result_10 = df_Q1.filter(['YEAR', 'RACE_DESC', 'PAID_TOTAL']).groupby(['YEAR', 'RACE_DESC']).describe() 
result_11 = df_Q1.filter(['YEAR', 'VISITS_TOTAL']).groupby(['YEAR']).describe()
result_12 = df_Q1.filter(['YEAR', 'RACE_DESC', 'VISITS_TOTAL']).groupby(['YEAR', 'RACE_DESC']).describe() 
df_Q1 = df_Q1.drop(columns = ['RACE_DESC', 'PERCENT_FEMALE'])

### Markdown Summary in docs subrepo
text_md = open('_docs//' + label_name + '//' + label_run + '//summary.md', 'a')
text_md.write('### ' + 'Data Preparation Summary' + '\n')
text_md.write("""The following Columns were derived for this analysis:

    VISITS - VISITS_TOTAL, ER_VISITS, HOME_VISITS, INPATIENT_VISITS, OFFICE_VISITS, OUTPATIENT_VISITS, RX_VISITS
    PAID - PAID_TOTAL, ER_PAID, HOME_PAID, INPATIENT_PAID, OFFICE_PAID, OUTPATIENT_PAID, RX_PAID
    ICD10 - ICD10_TOTAL, ICD10 YES/NO (1/0)
    """ + '\n')
text_md.write('\n')
text_md.write('##### Descriptive Statistics' + '\n')
text_md.write('The following statistics describe the population used for both analyses:' + '\n')
text_md.write('\n')
text_md.write(str(result_01))
text_md.write('\n\n')
text_md.write(str(result_02))
text_md.write('\n\n')
text_md.write(str(result_03))
text_md.write('\n\n')
text_md.write(str(result_04))
text_md.write('\n\n')
text_md.write(str(result_05))
text_md.write('\n\n')
text_md.write(str(result_06))
text_md.write('\n\n')
text_md.writestr((result_07))
text_md.write('\n\n')
text_md.write(str(result_08))
text_md.write('\n\n')
text_md.write(str(result_09))
text_md.write('\n\n')
text_md.write(str(result_10))
text_md.write('\n\n')
text_md.write(str(result_11))
text_md.write('\n\n')
text_md.write(str(result_12))
text_md.write('\n\n')
text_md.write('##### Research Question 1: Analytical File' + '\n')
text_md.write('\n')
text_md.write(info_Q1)
text_md.write('\n')
text_md.write('##### Research Question 2: Analytical File' + '\n')
text_md.write('\n')
text_md.write(info_Q2)
text_md.write('\n')
text_md.close()