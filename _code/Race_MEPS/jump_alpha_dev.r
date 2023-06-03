# Jump Back In

### Data Sceience Basics
library(tidyverse) # All of the libraries above in one line of code
library(skimr) # SUmmary statistics and glimpse for dataframes


### SQL
library(RSQLite) # SQLite databases in R
library(sqldf) # Use SQL commands on R dataframes
library(RPostgreSQL) # Postgre SQL databases in R

### Statistics
library(lme4) # Linear mixed effect modeling in R
library(arm) # Visualizations of linear mixed effect modeling using 'lme4' in R
library(lmtest) # Linear model tests including Breusch Pagan
library(lmerTest) # Linear mixed effect model tests allowing for Saittherwaier DOF and signficiance tests
library(DescTools) # Descriptive statistics including Jarque-Bera, Andrerson-Darling, Durbin-Watson, Cronbach's Alpha
library(performance) # Inter class correlation coefficient foir HLM
library(twopartm) # Two part modeling 

### Machine Learning
library(randomForest) # Popular random forest package for R
library(randomForestExplainer) # Complimentary to randfomForest package with tools for analysis

### Other
library(ineq) # Gini coefficient and Lorenz curve
library(rmarkdown) # Converting markdown documents

### Visualization
library(RColorBrewer) # Creates nice looking color palettes especially for thematic maps in R

### Standard Variables
label_home = 'C://Users'
label_user = 'drewc'
label_character = 'neville'
label_project = 'Health-Risk-and-Equity'
label_topic = 'Race'

### Import Variables
setwd(paste(label_home, label_user, label_character, label_project, sep = '//'))
df = read.csv(paste(label_home, label_user, label_character, label_project, '_tmp//variables.csv', sep = '//'))
desc_project = filter(df, Label == 'desc_project')$Value
desc_title = filter(df, Label == 'desc_title')$Value
desc_author = filter(df, Label == 'desc_author')$Value
desc_summary = filter(df, Label == 'desc_summary')$Value
desc_reference = filter(df, Label == 'desc_reference')$Value
desc_notes = filter(df, Label == 'desc_notes')$Value
desc_status = filter(df, Label == 'desc_status')$Value
desc_time = filter(df, Label == 'desc_time')$Value
label_subject = filter(df, Label == 'label_subject')$Value
label_version = filter(df, Label == 'label_version')$Value
label_status = filter(df, Label == 'label_status')$Value
label_reference = filter(df, Label == 'label_reference')$Value
label_time = filter(df, Label == 'label_time')$Value
label_name = filter(df, Label == 'label_name')$Value
label_run = filter(df, Label == 'label_run')$Value

### Database
db_con = dbConnect(RSQLite::SQLite(), paste('_data', label_name, label_run, 'database.db', sep = '//')) # create a connection to the postgres database

### Style preferences
low = 'blue3' # Standard map colorscheme
mid = 'lightyellow' # Standard map colorscheme
high = 'red3' # Standard map colorscheme
na = 'grey50' # Standard map colorscheme
line = 'black' # Standard map colorscheme
breaks = 9 # Standard map colorscheme
scheme = 'trad' # Standard map colorscheme
font = 'Vollkorn' # Define font for all figs 
