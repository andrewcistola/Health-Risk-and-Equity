# Data Section: Import and Clean Data

## Data Step 1: Import and Join Datasets

### Import and clean Labels (W)
df_W = read.csv('_data/ALL_HNB_CW2020_FIPS_ZCTA.csv', stringsAsFactors = FALSE) # Import dataset from _data folder
head(df_W)        
        
### Import and clean Predictors (X)
df_XY = read.csv(paste('_data/US_', target, '_stage.csv', sep = ''), stringsAsFactors = FALSE, fileEncoding = 'UTF-8-BOM') # Import dataset from _data folder
df_X1 = df_XY[c('ZCTA', 'age', 'sex', 'race')]
df_X2 = read.csv('_data/CENSUS_ACS_DP2018_ZCTA.csv', stringsAsFactors = FALSE) # Import dataset from _data folder
df_X = merge(df_X1, df_X2, by = 'ZCTA', how = 'inner') # Merge data frame into data slot in SpatialDataFrame
head(df_X)

### Import and clean Predictors and Outcomes (Y)
df_Y = df_XY[c('ZCTA', 'count')]
head(df_Y)

### Join Labels (W), Predictors (X), and Outcomes (Y)
df_WXY = merge(df_X, df_Y, by = 'ZCTA')
df_WXY = merge(df_WXY, df_W, by = 'ZCTA', all.x = TRUE)
df_WXY = df_WXY[which(df_WXY$ST == ST & df_WXY$population >= 0), ]
head(df_WXY) # Verify

## Data Step 2: Calculate Variables

### Adult and Child population
df_WXY$count[df_WXY$count > 0 & df_WXY$count <= 10] <- 10
df_WXY$adult_population <- df_WXY$DP05_0021PE * df_WXY$population / 100 #DP05_0021E,Percent Estimate!!SEX AND AGE!!Total population!!18 years and over
df_WXY$child_population <- df_WXY$DP05_0019PE * df_WXY$population / 100 #DP05_0019E,Percent Estimate!!SEX AND AGE!!Total population!!Under 18 years
df_WXY$adult_population[!is.finite(df_WXY$adult_population)] <- 0
df_WXY$child_population[!is.finite(df_WXY$child_population)] <- 0
summary(df_WXY$adult_population)
summary(df_WXY$child_population)
summary(df_WXY$population)

### Crude rate per 1000 for pop > 500
df_WXY = df_WXY[which(df_WXY$population > 500), ]
df_WXY$crude_population <- df_WXY %>% pull(paste(pop, '_population', sep = ''))
df_WXY$crude3 <- df_WXY$count / df_WXY$crude_population * 1000
df_WXY$crude3[df_WXY$crude3 > mean(df_WXY$crude3)*2] <- mean(df_WXY$crude3)*2
df_WXY$crude3[!is.finite(df_WXY$crude3)] <- 0
summary(df_WXY$crude3)
summary(df_WXY$crude_population)

### Create Deprivation Index with PCA     
Y = 'crude3'
X = c('DP03_0128PE', # Percent Estimate!!PERCENTAGE OF FAMILIES AND PEOPLE WHOSE INCOME IN THE PAST 12 MONTHS IS BELOW THE POVERTY LEVEL!!All people
      'DP03_0009PE', # Percent Estimate!!EMPLOYMENT STATUS!!Civilian labor force!!Unemployment Rate
      'DP04_0047PE', # Percent Estimate!!HOUSING TENURE!!Occupied housing units!!Renter-occupied
      'DP04_0058PE', # Percent Estimate!!VEHICLES AVAILABLE!!Occupied housing units!!No vehicles available
      'DP03_0099PE', # Percent Estimate!!HEALTH INSURANCE COVERAGE!!Civilian non institutionalized population!!No health insurance coverage
      'DP02_0061PE') # Percent Estimate!!EDUCATIONAL ATTAINMENT!!Population 25 years and over!!High school graduate (includes equivalency)
R = as.formula(paste(Y, ' ~ ', paste(X, collapse = ' + '), sep = ''))
D = df_WXY[c(X, Y)]
for(i in 1:ncol(D)) {D[ , i][is.na(D[ , i])] <- median(D[ , i], na.rm = TRUE)} # Replace missing values with column medians
pca = prcomp(D[X], scale = TRUE, rank. = 1) # PCA from tidyverse, `scale = TRUE` standard scale features, `tol = 0.1` threshold percent of highest variance to keep components
df_pca = rownames_to_column(data.frame(abs(pca$rotation)))
df_pca = df_pca[which(df_pca$PC1 > quantile(df_pca$PC1, 0.5)[[1]]), ]
colnames(df_pca) <- c('feature', 'variance')
df_X$ZDI = rowSums(df_X[df_pca$feature] * df_pca$variance)
df_WXY = merge(df_WXY, df_X[c('ZCTA', 'ZDI')], by = 'ZCTA') # Merge data frame into data slot in SpatialDataFrame
df_WXY$ZDI[!is.finite(df_WXY$ZDI)] <- median(df_WXY$ZDI, na.rm = TRUE)
write.csv(df_WXY[c('ZDI', 'ZCTA')], '_data/ALL_HNB_ZDI2018_FL.csv', row.names = F) # Export ZDI
summary(df_WXY$ZDI) # Verify

### Clean demographic variables
df_WXY$race <- 100 - df_WXY$race 
df_WXY$age[!is.finite(df_WXY$age)] <- 0
df_WXY$sex[!is.finite(df_WXY$sex)] <- 0
df_WXY$race[!is.finite(df_WXY$race)] <- 0

### Subset final dataset
df_WXY = df_WXY[c('ZCTA', 'ST', 'FIPS', 'ZDI', 'age', 'sex', 'race', 'crude3', 'count', 'population')]
head(df_WXY) # Verify

## Data Step 3: Export files

### Export final dataset
write.csv(df_WXY, paste('_data/', ST, '_', target, '_final.csv', sep = ''), row.names = F) # Clean in excel and select variable
df_WXY = read.csv(paste('_data/', ST, '_', target, '_final.csv', sep = ''), stringsAsFactors = FALSE, fileEncoding = 'UTF-8-BOM') # Import dataset from _data folder
head(df_WXY) # Verify