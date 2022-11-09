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




# Import

