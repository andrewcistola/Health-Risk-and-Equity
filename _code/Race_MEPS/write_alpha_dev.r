# Setup

## Libraries

### Hadley Wickham
library(tidyverse) # All of the libraries above in one line of code

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

### Machine Learning
library(randomForest) # Popular random forest package for R
library(randomForestExplainer) # Complimentary to randfomForest package with tools for analysis

### Other
library(ineq) # Gini coefficient and Lorenz curve

### Visualization
library(RColorBrewer) # Creates nice looking color palettes especially for thematic maps in R

### Spatial
library(rpostgis) # PostGIS with Postgres in R
library(sp) # S4 classes for spatial data in R
library(ggmap) # General use mapping library with ggplot API
library(GWmodel) # Geographic weighted regression in R
library(rgdal)
library(rgeos) 
library(maptools) 
library(ggsn)
library(spdep)  
library(DCluster)  
library(gstat) 
library(tigris)  
library(raster)  
library(dismo)  
library(smacpod)
library(rsatscan)
library(spatstat)

## Variables

### Standard Variables
label_home = 'C://Users//'
label_user = 'drewc'
label_character = 'neville'
label_project = 'Health-Risk-and-Equity'
label_topic = 'Race'

### Python Variables
df = read.csv(paste(label_home, label_user, label_character, label_project, label_topic, '_tmp//variables.csv', sep = '//'))
desc_project = filter(df, Label == 'desc_project')$Value
desc_title = filter(df, Label == 'desc_title')$Value
desc_author = filter(df, Label == 'desc_author')$Value
desc_summary = filter(df, Label == 'desc_summary')$Value
desc_reference = filter(df, Label == 'desc_reference')$Value
desc_notes = filter(df, Label == 'desc_notes')$Value
desc_status = filter(df, Label == 'desc_status')$Value
desc_time = filter(df, Label == 'desc_time')$Value
label_home = filter(df, Label == 'label_home')$Value
label_user = filter(df, Label == 'label_user')$Value
label_character = filter(df, Label == 'label_character')$Value
label_project = filter(df, Label == 'label_project')$Value
label_topic = filter(df, Label == 'label_topic')$Value
label_subject = filter(df, Label == 'label_subject')$Value
label_jobs = filter(df, Label == 'label_jobs')$Value
label_version = filter(df, Label == 'label_version')$Value
label_status = filter(df, Label == 'label_status')$Value
label_reference = filter(df, Label == 'label_reference')$Value
label_dir = filter(df, Label == 'label_dir')$Value
label_time = filter(df, Label == 'label_time')$Value
label_name = filter(df, Label == 'label_name')$Value

## Files

### Database
db_con = dbConnect(RSQLite::SQLite(), paste(label_topic, '/_wrap/', label_name, '.db')) # create a connection to the postgres database











# Write

## Write to existing file
file = label_topic + '/_wrap/' + label_name + '/Summary.md'
cat(paste('### Methods', '\n', sep = ''), file = file, append = TRUE)
cat(paste(desc_methods, '\n\n', sep = ''), file = file, append = TRUE)
cat(paste('Data for this study was collected from the ', reference, '\n\n', sep = ''), file = file, append = TRUE)
cat(paste('\n', sep = ''), file = file, append = TRUE)
cat(paste('#### Variable Definitions: \n', sep = ''), file = file, append = TRUE)
cat(paste('`count` ', 'Raw count of ', full, '\n\n', sep = ''), file = file, append = TRUE) 
cat(paste('`log` ', desc_log, '\n\n', sep = ''), file = file, append = TRUE) 
cat(paste('`crude3` ', desc_crude3, '\n\n', sep = ''), file = file, append = TRUE) 
cat(paste('`ZDI` ', desc_ZDI, '\n\n', sep = ''), file = file, append = TRUE) 
cat(paste('`age` ', desc_age, '\n\n', sep = ''), file = file, append = TRUE) 
cat(paste('`sex` ', desc_sex, '\n\n', sep = ''), file = file, append = TRUE) 
cat(paste('`race` ', desc_race, '\n\n', sep = ''), file = file, append = TRUE) 
cat(paste('\n', sep = ''), file = file, append = TRUE)
cat(paste('#### Variable Notes: \n', sep = ''), file = file, append = TRUE)
cat(paste(notes, '\n', sep = ''), file = file, append = TRUE)
cat(paste('\n', sep = ''), file = file, append = TRUE)
cat('#### OLS Assumption Tests (Y = ', Y, '):\n\n', file = file, append = TRUE)
cat(capture.output(utt), file = file, append = TRUE)
cat('(Significant = Non-linearity)\n\n', file = file, append = TRUE)
cat(capture.output(jb), file = file, append = TRUE)
cat('(Significant = Non-normal)\n\n', file = file, append = TRUE)
cat(capture.output(ad), file = file, append = TRUE)
cat('(Significant = Non-normal)\n\n', file = file, append = TRUE)
cat(capture.output(dw), file = file, append = TRUE)
cat('(Significant = Auto-correlation)\n',  file = file, append = TRUE)
cat(capture.output(bp), file = file, append = TRUE)
cat('(Significant = Homoscedastic)\n\n', file = file, append = TRUE)
cat(capture.output(gq), file = file, append = TRUE)
cat('(Significant = Heteroscedastic)\n\n', file = file, append = TRUE)
cat('\n', file = file, append = TRUE)
cat(paste('### Results', '\n', sep = ''), file = file, append = TRUE) 
cat(paste('#### Univariate Statistics (Median values):\n', sep = ''), file = file, append = TRUE)
cat(paste('count = ', median(df_WXY$count), '\n\n', sep = ''), file = file, append = TRUE)
cat(paste('log = ', median(df_WXY$log), '\n\n', sep = ''), file = file, append = TRUE)
cat(paste('crude3 = ', median(df_WXY$crude3), '\n\n', sep = ''), file = file, append = TRUE)
cat(paste('ZDI = ', median(df_WXY$ZDI), '\n\n', sep = ''), file = file, append = TRUE)
cat(paste('age = ', median(df_WXY$age), '\n\n', sep = ''), file = file, append = TRUE)
cat(paste('sex = ', median(df_WXY$sex), '\n\n', sep = ''), file = file, append = TRUE)
cat(paste('race = ', median(df_WXY$race), '\n\n', sep = ''), file = file, append = TRUE)
cat(paste('\n', sep = ''), file = file, append = TRUE)
cat(paste('#### Bivariate Statistics (Y = ', Y, '):\n', sep = ''), file = file, append = TRUE)
cat(paste('ZDI = ', cor_ZDI, '\n\n', sep = ''), file = file, append = TRUE)
cat(paste('age = ', cor_age, '\n\n', sep = ''), file = file, append = TRUE)
cat(paste('sex = ', cor_sex, '\n\n', sep = ''), file = file, append = TRUE)
cat(paste('race = ', cor_race, '\n\n', sep = ''), file = file, append = TRUE)
cat(paste('\n', sep = ''), file = file, append = TRUE)
cat('#### Regression Models (Y = ', Y, '): \n\n', file = file, append = TRUE)
cat('\n', file = file, append = TRUE)
cat(paste(str_replace_all(capture.output(GWR), c(''' = '', ''' = '')), '\n\n', sep = ''), file = file, append = TRUE)
cat('\n', file = file, append = TRUE)
cat('### Tables and Figures\n\n', file = file, append = TRUE)
cat(paste('![](', ST, '_', target, '_resid_plot.png)\n\n', sep = ''), file = file, append = T)
cat(paste('![](', ST, '_', target, '_QQ_plot.png)\n\n', sep = ''), file = file, append = T)
cat(paste('![](', ST, '_', target, '_cor_plot.png)\n\n', sep = ''), file = file, append = T)
cat(paste('![](', ST, '_', target, '_count_map.png)\n\n', sep = ''), file = file, append = T)
cat(paste('![](', ST, '_', target, '_log_map.png)\n\n', sep = ''), file = file, append = T)
cat(paste('![](', ST, '_', target, '_crude3_map.png)\n\n', sep = ''), file = file, append = T)
cat(paste('![](', ST, '_', target, '_ZDI_map.png)\n\n', sep = ''), file = file, append = T)
cat(paste('![](', ST, '_', target, '_GWR_ZDI_map.png)\n\n', sep = ''), file = file, append = T)
cat(paste('![](', ST, '_', target, '_age_map.png)\n\n', sep = ''), file = file, append = T)
cat(paste('![](', ST, '_', target, '_sex_map.png)\n\n', sep = ''), file = file, append = T)
cat(paste('![](', ST, '_', target, '_race_map.png)\n\n', sep = ''), file = file, append = T)
cat(paste('########################################\n\n', 
          'Last Update: ', stamp, ' by ', user, '<br>\n',
          'Disclaimer: ', disclaimer, '\n',
          '\n', sep = ''), file = file, append = TRUE)

render(input = file, output_format = 'html_document',  output_file = paste(ST, '_', target, '_page.html', sep = ''))
render(input = file, output_format = 'word_document',  output_file = paste(ST, '_', target, '_report.doc', sep = ''))