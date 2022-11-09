## Set Script variables
title = 'HSR MEPS 2019' # Input basic title
descriptive = '- Sample Study for HSR Resource Repository' # Input descriptive title
author = 'Andrew S. Cistola, MPH' # Input author information
GH = 'https://github.com/andrewcistola/HSR' # Input GitHub repository
name = 'HSR_MEPS_2019_alpha' # Input generic file name with repo, project, subject, and version
project = 'MEPS/' # Input project file name inside repository
repo = 'HSR/' # Input repository filename
user = 'Andrew S. Cistola, MPH; https://github.com/andrewcistola' # Input name and GitHub profile of user
local = '/home/drewc/GitHub/' # Input local path to repository
directory = paste(local, repo, project, sep = "") # Set wd to project repository using variables
day = Sys.Date() # Save dimple date as string
stamp = date() # Save Date and timestamp

## Set working directory
setwd(directory) # Set wd to project repository

## Import data
df_meps = read.csv('MEPS_2019_raw.csv') # Import dataset from _data folder 
df_meps = df_meps[which(df_meps$AGE19X >= 65), ] # based on variable values
head(df_meps) # Print mini table with first 6 observations 
nrow(df_meps) # Number of rows

## Create subset table
df_XY = df_meps[c('PID', # ID
                    # Diagnoses 
                    'DIABDX_M18', # Diabetes Diagnosis
                    'STRKDX', # 2 = stroke diagnosis
                    'EMPHDX', # 2 = emphezema diagnosis
                    'CHDDX', # 2 = Coronary heart disease diagnosis
                    'ANGIDX', # 2 = Angina diagnosis 
                    'CANCERDX', # 2 = Cancer Diagnosis                        
                    # Social determinants
                    'HIDEG', # 1-3 = HS or less
                    'EMPST53', # 4 = Not employed
                    'HRWG31X', # Hourly wage, -10 >= 96.15
                    'RETPLN31', # 2 = No Pension Plan at retirement age
                    'HWELLSPK', # 3+ = Speak english not well                        
                    'MCDEV19', # Ever Medicaid in 2019
                    'RACETHX', # 3 = Non-Hispanic Black
                    'NWK31', # 3 = Does not work due to disability
                    'EVRETIRE', # 1 = Retired
                    # Confounders and fixed effects
                    'REGION19', # Census region
                    'AGE19X', # Age in years
                    'MCRPHO19', # 1 = MA, 2 = FFS, 3 = Not Medicare
                    # Outcomes
                    'ERTOT19', # Total ED visits
                    'IPNGT19', # Total Inpatient nights
                    'IPDIS19', # Total Inpatient discharges
                    'OBDRV19', # Total office based physician visits 
                    'OPDRV19' # Total outpaitnet physician visits
                    )] # 
df_XY = replace(df_XY, df_XY <= 0, 0) # Replace all values below 0 with 0 
head(df_XY)# Print mini table with first 6 observations 

## Create Predictor table
df_X = df_XY[c('DIABDX_M18', # Diabetes Diagnosis
                        'STRKDX', # 2 = stroke diagnosis
                        'EMPHDX', # 2 = emphezema diagnosis
                        'CHDDX', # 2 = Coronary heart disease diagnosis
                        'ANGIDX', # 2 = Angina diagnosis 
                        'CANCERDX', # 2 = Cancer Diagnosis
                        'AGE19X'
                        )] # 
df_X = replace(df_X, df_X == 2, 0) # Replace all values below 0 with 0 
df_X = replace(df_X, df_X == NA, 0) # Replace all values below 0 with 0 
df_X$CHRCMI = df_X$DIABDX_M18 + df_X$STRKDX + df_X$EMPHDX + df_X$CHDDX + df_X$ANGIDX + df_X$CANCERDX*6 # Calculate Charlson comorbidity index
summary(df_X) # Print mini table with first 6 observations 
head(df_X)# Print mini table with first 6 observations 

### Create SDOH predictor table
df_S = df_XY[c('HIDEG', # 1-3 = HS or less
                        'EMPST53', # 4 = Not employed
                        'HRWG31X', # Hourly wage, 0.17 - 96.15
                        'RETPLN31', # 2 = No Pension Plan at retirement age
                        'HWELLSPK', # 3+ = Speak english not well
                        'MCDEV19', # 1 = Ever Medicaid in 2019
                        'RACETHX', # 3 = Non-Hispanic Black
                        'NWK31' # 3 = Does not work due to disability
                        )] # 
df_S$HIDEG[df_S$HIDEG < 3] <- 1 # Create new column based on conditions
df_S$EMPST53[df_S$EMPST53 == 4] <- 1 # Create new column based on conditions
df_S$HRWG31X[df_S$HRWG31X < 15] <- 1 # Create new column based on conditions
df_S$RETPLN31[df_S$RETPLN31 == 2] <- 1 # Create new column based on conditions
df_S$HWELLSPK[df_S$HWELLSPK > 3] <- 1 # Create new column based on conditions
df_S$MCDEV19[df_S$MCDEV19 == 1] <- 1 # Create new column based on conditions
df_S$RACETHX[df_S$RACETHX == 3] <- 1 # Create new column based on conditions
df_S$NWK31[df_S$NWK31 == 3] <- 1 # Create new column based on conditions
df_S = replace(df_S, df_S == NA, 0) # Replace all values below 0 with 0 
df_S = replace(df_S, df_S > 1, 0) # Replace all values below 0 with 0 
df_S = replace(df_S, df_S < 1, 0) # Replace all values below 0 with 0 
df_S$SDOH = df_S$HIDEG + df_S$EMPST53 + df_S$HRWG31X + df_S$RETPLN31 + df_S$HWELLSPK + df_S$MCDEV19 + df_S$RACETHX + df_S$NWK31
summary(df_S) # Print mini table with first 6 observations 
head(df_S)# Print mini table with first 6 observations 

## Create outcome table
df_Y = df_XY[c('IPNGT19')] # Select columns of dataframe
df_Y = replace(df_Y, df_Y == NA, 0) # Replace all values below 0 with 0 
summary(df_Y) # Print mini table with first 6 observations 

### Create final table
df_F = merge(df_X, df_S, by = 0, keep = FALSE) # Join dataframes by index
df_F = merge(df_F, df_Y, by = 0, keep = FALSE) # Join data frames by index
df_F = df_F[c('CHRCMI', 'SDOH', 'IPNGT19', 'AGE19X')] # Select final varibales for model
df_F$INT = df_F$CHRCMI * df_F$SDOH
head(df_F)# Print mini table with first 6 observations 
summary(df_F) # Print mini table with first 6 observations 

### OLS Model
y <- df_F$IPNGT19
x1 <- df_F$CHRCMI
x2 <- df_F$SDOH
x3 <- df_F$AGE19X
x4 <- df_F$INT
model = lm(y ~ x1 + x2 + x3 + x4)
res = resid(model)

### Utt's Rainbox Test
library(lmtest)
raintest(y ~ x1 + x2 + x3 + x4)

### Residuals Plot
library(ggplot2)
png(paste(name, '_res.png'))
plot(fitted(model), res)
abline(0,0)
dev.off()

### Histogram
library(ggplot2)
png(paste(name, '_hist.png'))
plot(fitted(model), res)
abline(0,0)
dev.off()




