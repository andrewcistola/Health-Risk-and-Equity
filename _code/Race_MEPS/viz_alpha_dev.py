# Visuals

## Q1 Results
df = pd.read_csv('_data//' + label_name + '//' + label_run + '//analytical_Q1.csv')
df['PERCENT_FEMALE'] = np.where(df['SEX'] == 1, 0, 
                                np.where(df['SEX'] == 2, 1,
                                    0)) # Create column based on conditions
df['RACE_DESC'] = np.where(df['RACE'] == 1, 'HISPANIC', 
                                np.where(df['RACE'] == 2, 'WHITE',
                                    np.where(df['RACE'] == 3, 'BLACK',
                                        np.where(df['RACE'] == 4, 'ASIAN',
                                            'OTHER')))) # Create column based on conditions                                 
df['X_LABEL'] = df['YEAR'].astype('str') + '-' + df['RACE_DESC']

### Condtional Means: Total Paid
G = 'PAID_TOTAL'
graph = 'Total Paid Amounts from Private Payers per Person'
df_graph = df.filter(['YEAR', 'RACE_DESC', G]).groupby(['YEAR', 'RACE_DESC'], as_index = False).mean() # Keep selected columns and sum by key columns (keeping all as columns not index)
df_graph = df_graph.pivot(index = 'YEAR', columns = 'RACE_DESC', values = G) # Pivot from long to wide
plt.figure(figsize = (12, 9))
x = np.arange(3)
plt.bar((x), df_graph.WHITE, color = 'r', width = 0.16, label = 'White')
plt.bar((x+.2), df_graph.BLACK, color = 'b', width = 0.16, label = 'Black')
plt.bar((x+.4), df_graph.HISPANIC, color = 'g', width = 0.16, label = 'Hispanic')
plt.bar((x+.6), df_graph.ASIAN, color = 'purple', width = 0.16, label = 'Asian')
plt.xticks([0.3, 1.3, 2.3], ['2018', '2019', '2020'])
plt.ylabel(graph)
plt.xlabel('Year')
plt.legend()
plt.title('Individuals Enrolled in Marketplaces 2018-2021')
plt.savefig('_fig//' + label_name + '//' + label_run + '//' + G + '.jpeg')

### Condtional Means: Total Visits
G = 'VISITS_TOTAL'
graph = 'Total Visits for Any Setting per Person'
df_graph = df.filter(['YEAR', 'RACE_DESC', G]).groupby(['YEAR', 'RACE_DESC'], as_index = False).mean() # Keep selected columns and sum by key columns (keeping all as columns not index)
df_graph = df_graph.pivot(index = 'YEAR', columns = 'RACE_DESC', values = G) # Pivot from long to wide
plt.figure(figsize = (12, 9))
x = np.arange(3)
plt.bar((x), df_graph.WHITE, color = 'r', width = 0.16, label = 'White')
plt.bar((x+.2), df_graph.BLACK, color = 'b', width = 0.16, label = 'Black')
plt.bar((x+.4), df_graph.HISPANIC, color = 'g', width = 0.16, label = 'Hispanic')
plt.bar((x+.6), df_graph.ASIAN, color = 'purple', width = 0.16, label = 'Asian')
plt.xticks([0.3, 1.3, 2.3], ['2018', '2019', '2020'])
plt.ylabel(graph)
plt.xlabel('Year')
plt.legend()
plt.title('Individuals Enrolled in Marketplaces 2018-2021')
plt.savefig('_fig//' + label_name + '//' + label_run + '//' + G + '.jpeg')

### Condtional Means: ICD10 Count
G = 'ICD10_TOTAL'
graph = 'Number of Diagnoses per Person'
df_graph = df.filter(['YEAR', 'RACE_DESC', G]).groupby(['YEAR', 'RACE_DESC'], as_index = False).mean() # Keep selected columns and sum by key columns (keeping all as columns not index)
df_graph = df_graph.pivot(index = 'YEAR', columns = 'RACE_DESC', values = G) # Pivot from long to wide
plt.figure(figsize = (12, 9))
x = np.arange(3)
plt.bar((x), df_graph.WHITE, color = 'r', width = 0.16, label = 'White')
plt.bar((x+.2), df_graph.BLACK, color = 'b', width = 0.16, label = 'Black')
plt.bar((x+.4), df_graph.HISPANIC, color = 'g', width = 0.16, label = 'Hispanic')
plt.bar((x+.6), df_graph.ASIAN, color = 'purple', width = 0.16, label = 'Asian')
plt.xticks([0.3, 1.3, 2.3], ['2018', '2019', '2020'])
plt.ylabel(graph)
plt.xlabel('Year')
plt.legend()
plt.title('Individuals Enrolled in Marketplaces 2018-2021')
plt.savefig('_fig//' + label_name + '//' + label_run + '//' + G + '.jpeg')

### Condtional Means: FPL Percent
G = 'FPL_PERCENT'
graph = 'Average Income as percent of federal poverty line'
df_graph = df.filter(['YEAR', 'RACE_DESC', G]).groupby(['YEAR', 'RACE_DESC'], as_index = False).mean() # Keep selected columns and sum by key columns (keeping all as columns not index)
df_graph = df_graph.pivot(index = 'YEAR', columns = 'RACE_DESC', values = G) # Pivot from long to wide
plt.figure(figsize = (12, 9))
x = np.arange(3)
plt.bar((x), df_graph.WHITE, color = 'r', width = 0.16, label = 'White')
plt.bar((x+.2), df_graph.BLACK, color = 'b', width = 0.16, label = 'Black')
plt.bar((x+.4), df_graph.HISPANIC, color = 'g', width = 0.16, label = 'Hispanic')
plt.bar((x+.6), df_graph.ASIAN, color = 'purple', width = 0.16, label = 'Asian')
plt.xticks([0.3, 1.3, 2.3], ['2018', '2019', '2020'])
plt.ylabel(graph)
plt.xlabel('Year')
plt.legend()
plt.title('Individuals Enrolled in Marketplaces 2018-2021')
plt.savefig('_fig//' + label_name + '//' + label_run + '//' + G + '.jpeg')

### Condtional Means: Age
G = 'PERCENT_FEMALE'
graph = 'Percent Female'
df_graph = df.filter(['YEAR', 'RACE_DESC', G]).groupby(['YEAR', 'RACE_DESC'], as_index = False).mean() # Keep selected columns and sum by key columns (keeping all as columns not index)
df_graph = df_graph.pivot(index = 'YEAR', columns = 'RACE_DESC', values = G) # Pivot from long to wide
plt.figure(figsize = (12, 9))
x = np.arange(3)
plt.bar((x), df_graph.WHITE, color = 'r', width = 0.16, label = 'White')
plt.bar((x+.2), df_graph.BLACK, color = 'b', width = 0.16, label = 'Black')
plt.bar((x+.4), df_graph.HISPANIC, color = 'g', width = 0.16, label = 'Hispanic')
plt.bar((x+.6), df_graph.ASIAN, color = 'purple', width = 0.16, label = 'Asian')
plt.xticks([0.3, 1.3, 2.3], ['2018', '2019', '2020'])
plt.ylabel(graph)
plt.xlabel('Year')
plt.legend()
plt.title('Individuals Enrolled in Marketplaces 2018-2021')
plt.savefig('_fig//' + label_name + '//' + label_run + '//' + G + '.jpeg')

### Condtional Means: Age
G = 'AGE'
graph = 'Average Age'
df_graph = df.filter(['YEAR', 'RACE_DESC', G]).groupby(['YEAR', 'RACE_DESC'], as_index = False).mean() # Keep selected columns and sum by key columns (keeping all as columns not index)
df_graph = df_graph.pivot(index = 'YEAR', columns = 'RACE_DESC', values = G) # Pivot from long to wide
plt.figure(figsize = (12, 9))
x = np.arange(3)
plt.bar((x), df_graph.WHITE, color = 'r', width = 0.16, label = 'White')
plt.bar((x+.2), df_graph.BLACK, color = 'b', width = 0.16, label = 'Black')
plt.bar((x+.4), df_graph.HISPANIC, color = 'g', width = 0.16, label = 'Hispanic')
plt.bar((x+.6), df_graph.ASIAN, color = 'purple', width = 0.16, label = 'Asian')
plt.xticks([0.3, 1.3, 2.3], ['2018', '2019', '2020'])
plt.ylabel(graph)
plt.xlabel('Year')
plt.legend()
plt.title('Individuals Enrolled in Marketplaces 2018-2021')
plt.savefig('_fig//' + label_name + '//' + label_run + '//' + G + '.jpeg')

## Q2 Results

### Kitigawa-Oaxaca-Blinder
df_graph = pd.read_csv('_data//' + label_name + '//' + label_run + '//results_Q2.csv')
plt.figure()
x = np.arange(len(df_graph['Kitigawa-Oaxaca-Blinder']))
plt.bar((x), df_graph['Kitigawa-Oaxaca-Blinder'], color = 'b', width = 0.6)
plt.xticks(np.arange(len(df_graph['Kitigawa-Oaxaca-Blinder']), step = 5), np.arange(len(df_graph['Kitigawa-Oaxaca-Blinder']), step = 5), rotation = 90)
plt.ylabel('Predicted from white model - Observed')
plt.xlabel('Machine Learning Algorithm w/predictors selected')
plt.legend(['log(Paid Claims)'])
plt.title('Paid Claims for Non-Whites Enrolled in Marketplaces 2018-2021')
plt.savefig('_fig//' + label_name + '//' + label_run + '//Kitigawa-Oaxaca-Blinder.jpeg')

### Export to Summary File
text_md = open('_docs//' + label_name + '//' + label_run + '//summary.md', 'a')
text_md.write('### ' + 'Tables and Figures' + '\n')
text_md.write('Files can be found at: _fig//' + label_name + '//' + label_run + '//' + '\n')
text_md.write('\n')
text_md.write('#### ' + 'Descriptive Statistics' + '\n')
text_md.write('![Average Age](_fig//' + label_name + '//' + label_run + '//AGE.jpeg)' + '\n')
text_md.write('![Percent_Female](_fig//' + label_name + '//' + label_run + '//PERCENT_FEMALE.jpeg)' + '\n')
text_md.write('![Average Income as percent of federal poverty line](_fig//' + label_name + '//' + label_run + '//FPL_PERCENT.jpeg)' + '\n')
text_md.write('![Number of Diagnoses per Person](_fig//' + label_name + '//' + label_run + '//ICD10_TOTAL).jpeg)' + '\n')
text_md.write('![Total Visits for Any Setting per Person](_fig//' + label_name + '//' + label_run + '//VISITS_TOTAL.jpeg)' + '\n')
text_md.write('![Total Paid Amounts from Private Payers per Person](_fig//' + label_name + '//' + label_run + '//PAID_TOTAL.jpeg)' + '\n')
text_md.write('\n')
text_md.write('#### ' + 'Regression Results' + '\n')
text_md.write('![2018 QQ Plot](_fig//' + label_name + '//' + label_run + '//2018_QQ_PERSON_ID_plot.png)' + '\n')
text_md.write('![2019 QQ Plot](_fig//' + label_name + '//' + label_run + '//2019_QQ_PERSON_ID_plot.png)' + '\n')
text_md.write('![2020 QQ Plot](_fig//' + label_name + '//' + label_run + '//2020_QQ_PERSON_ID_plot.png)' + '\n')
text_md.write('![2018 Residuals](_fig//' + label_name + '//' + label_run + '//2018_residuals_PERSON_ID_plot.png)' + '\n')
text_md.write('![2019 Residuals](_fig//' + label_name + '//' + label_run + '//2019_residuals_PERSON_ID_plot.png)' + '\n')
text_md.write('![2020 Residuals](_fig//' + label_name + '//' + label_run + '//2020_residuals_PERSON_ID_plot.png)' + '\n')
text_md.write('![2018 Colinearity](_fig//' + label_name + '//' + label_run + '//2018_correlation_PERSON_ID_plot.png)' + '\n')
text_md.write('![2019 Colinearity](_fig//' + label_name + '//' + label_run + '//2019_correlation_PERSON_ID_plot.png)' + '\n')
text_md.write('![2020 Colinearity](_fig//' + label_name + '//' + label_run + '//2020_correlation_PERSON_ID_plot.png)' + '\n')
text_md.write('\n')
text_md.close() # Close file