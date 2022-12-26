# Regression Modeling Script

## Regression Step 1: Import and Clean Data
step_1 = 'Regression Step 1: Import and Clean Data'
W = 'PERSON_ID'
X = c('NON_WHITE', 'AGE', 'SEX', 'FPL_PERCENT', 'ICD10_TOTAL')
Y = 'PAID_TOTAL'
Z = 'YEAR'

### Import Labels/Demographics (W) with Predictors (X) Outcomes (Y) and Shapes/Subgroups (Z)
df_WXYZ = read.csv(paste('_data', label_name, label_run, 'analytical_Q1.csv', sep = '//'), stringsAsFactors = FALSE) # Import dataset from _data folder

### Recode Racial Groups
df_WXYZ$HISPANIC <- 0
df_WXYZ$WHITE <- 0
df_WXYZ$BLACK <- 0
df_WXYZ$ASIAN <- 0
df_WXYZ$OTHER <- 0
df_WXYZ$NON_WHITE <- 0
df_WXYZ$HISPANIC[df_WXYZ$RACE == 1] <- 1
df_WXYZ$WHITE[df_WXYZ$RACE == 2] <- 1
df_WXYZ$BLACK[df_WXYZ$RACE == 3] <- 1
df_WXYZ$ASIAN[df_WXYZ$RACE == 4] <- 1
df_WXYZ$NON_WHITE[df_WXYZ$RACE != 2] <- 1

### Export to Summary File
file = paste('_docs', label_name, label_run, 'summary.md', sep = '//')
sink(file = file, append = TRUE, type = 'output')
cat(c('### ', 'Regression Modeling Result Summary', '\n'), file = file, append = TRUE)
cat(c('The following results were collected using ', R.Version()$version.string, '\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('#### ', step_1, '\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('Source: ', paste('_data', label_name, label_run, 'analytical_Q1.csv', sep = '//'), '\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('W (ID variables): ', W, '<br>\n'), file = file, append = TRUE)
cat(c('X (Predictor variables): ', X, '<br>\n'), file = file, append = TRUE)
cat(c('Y (Outcome variables): ', Y, '<br>\n'), file = file, append = TRUE)
cat(c('Z (Subgroup variables): ', Z, '<br>\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
skim(df_WXYZ)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
sink()

## Regression Step 2: Test for OLS Assumptions
step_2 = 'Regression Step 2: Test for OLS Assumptions'

### Regression Step 2: Subgroups
G = 2018

### OLS Assumption 0: Sampling (Observations are a random sample, there are more observations than variables, IV is a result of DV)
test_0 =  'OLS Assumption 0: Sampling (Random sample, observations > predictors, predictor is independent)'
D = subset(df_WXYZ, df_WXYZ[Z] == G, select = c(X, Y))
F = as.formula(paste(Y, ' ~ ', paste(X, collapse = ' + '), sep = ''))
OLS = lm(F, data = D) # Identitiy link [Y = DV*1] (aka: Linear) with gaussian error (aka: Linear regression)

### OLS Assumption 1: Specification (Relationship between predictor and outcome is linear)
test_1 = 'OLS Assumption 1: Specification (Relationship between predictor and outcome is linear)'
utt = raintest(OLS) # Utt's Rainbox Test

### OLS Assumption 2: Normality (Errors are normal with a mean = 0)
test_2 = 'OLS Assumption 2:  Normality (Errors are normal with a mean = 0)'
jb = JarqueBeraTest(resid(OLS)) # Jarque Bera Test
ad = AndersonDarlingTest(resid(OLS)) # Anderson-Darling Test
png(paste('_fig/', label_name, '//', label_run, '//', G, '_QQ_', W, '_plot.png', sep = ''))

qqnorm(resid(OLS))
qqline(resid(OLS))
dev.off()

### OLS Assumption 3: No Autocorrelation (Error terms are not correlated among observations)
test_3 = 'OLS Assumption 3: No Autocorrelation (Error terms are not correlated with each other)'
dw = DurbinWatsonTest(OLS) # Drubin-Watson Test

### OLS Assumption 4: Homoskedasticity (Error terms have constant variance across observations)
test_4 = 'OLS Assumption 4: Homoskedasticity (Error is even across observations)'
bp = bptest(OLS) # Breusch-Pagan Test
gq = gqtest(OLS) # Goldfield Quant Test
png(paste('_fig//', label_name, '//', label_run, '//', G, '_residuals_', W, '_plot.png', sep = ''))
plot(resid(OLS))
abline(0,0)
dev.off()

### OLS Assumption 5: No Colinearity (Predictors are not correlated with each other)
test_5 = 'OLS Assumption 5: No Colinearity (Predictors are not correlated with each other)'
plot = ggplot(subset(data.table::melt(round(cor(df_WXYZ[X], use = "pairwise.complete.obs"), 3)), value < 1), 
                aes(Var1, 
                    Var2)) + 
            geom_tile(aes(
                fill = value)) + 
            geom_text(aes(
                label = value),
                size = 1) + 
            scale_fill_gradient2(
                low = low,
                mid = mid,
                high = high) +
            labs(
                title = paste('Correlation Matrix |', desc_title, sep = " "),
                fill = 'predictor\ncorrelation') +
            theme_minimal() +
            theme(
                text = element_text(family = 'Bookman'),
                plot.title = element_text(size = 12),
                panel.grid.major = element_blank(), 
                panel.grid.minor = element_blank(),
                panel.border = element_blank(),
                panel.background = element_blank(),
                axis.title = element_blank(),
                axis.text = element_text(size = 8),
                axis.text.x = element_text(angle = 90))
ggsave(paste('_fig//', label_name, '//', label_run, '//', G, '_correlation_', W, '_plot.png', sep = ''), plot = plot) # Save ggplot as jpeg

### Export to Summary File
sink(file = file, append = TRUE, type = 'output')
cat(c('#### ', step_2, '\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### Results for Subgroup: ', G, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### ', test_0, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
summary(OLS)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### ', test_1, '\n\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(utt)
print('Significant = Non-linearity')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### ', test_2, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(jb)
print('Significant = Non-normal')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(ad)
print('Signficiant = Non-normal')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n\n'), file = file, append = TRUE)
cat(c('##### ', test_3, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(dw)
print('Signficiant = Autocorrelation')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n\n'), file = file, append = TRUE)
cat(c('##### ', test_4, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(bp)
print('Signficiant = Homoscedastic')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n\n'), file = file, append = TRUE)
cat(c('##### ', test_5, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(gq)
print('Signficiant = Heteroscedastic')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
sink()

### Regression Step 2: Subgroups
G = 2019

### OLS Assumption 0: Sampling (Observations are a random sample, there are more observations than variables, IV is a result of DV)
test_0 =  'OLS Assumption 0: Sampling (Random sample, observations > predictors, predictor is independent)'
D = subset(df_WXYZ, df_WXYZ[Z] == G, select = c(X, Y))
F = as.formula(paste(Y, ' ~ ', paste(X, collapse = ' + '), sep = ''))
OLS = lm(F, data = D) # Identitiy link [Y = DV*1] (aka: Linear) with gaussian error (aka: Linear regression)

### OLS Assumption 1: Specification (Relationship between predictor and outcome is linear)
test_1 = 'OLS Assumption 1: Specification (Relationship between predictor and outcome is linear)'
utt = raintest(OLS) # Utt's Rainbox Test

### OLS Assumption 2: Normality (Errors are normal with a mean = 0)
test_2 = 'OLS Assumption 2:  Normality (Errors are normal with a mean = 0)'
jb = JarqueBeraTest(resid(OLS)) # Jarque Bera Test
ad = AndersonDarlingTest(resid(OLS)) # Anderson-Darling Test
png(paste('_fig/', label_name, '//', label_run, '//', G, '_QQ_', W, '_plot.png', sep = ''))
qqnorm(resid(OLS))
qqline(resid(OLS))
dev.off()

### OLS Assumption 3: No Autocorrelation (Error terms are not correlated among observations)
test_3 = 'OLS Assumption 3: No Autocorrelation (Error terms are not correlated with each other)'
dw = DurbinWatsonTest(OLS) # Drubin-Watson Test

### OLS Assumption 4: Homoskedasticity (Error terms have constant variance across observations)
test_4 = 'OLS Assumption 4: Homoskedasticity (Error is even across observations)'
bp = bptest(OLS) # Breusch-Pagan Test
gq = gqtest(OLS) # Goldfield Quant Test
png(paste('_fig//', label_name, '//', label_run, '//', G, '_residuals_', W, '_plot.png', sep = ''))
plot(resid(OLS))
abline(0,0)
dev.off()

### OLS Assumption 5: No Colinearity (Predictors are not correlated with each other)
test_5 = 'OLS Assumption 5: No Colinearity (Predictors are not correlated with each other)'
plot = ggplot(subset(data.table::melt(round(cor(df_WXYZ[X], use = "pairwise.complete.obs"), 3)), value < 1), 
                aes(Var1, 
                    Var2)) + 
            geom_tile(aes(
                fill = value)) + 
            geom_text(aes(
                label = value),
                size = 1) + 
            scale_fill_gradient2(
                low = low,
                mid = mid,
                high = high) +
            labs(
                title = paste('Correlation Matrix |', desc_title, sep = " "),
                fill = 'predictor\ncorrelation') +
            theme_minimal() +
            theme(
                text = element_text(family = 'Bookman'),
                plot.title = element_text(size = 12),
                panel.grid.major = element_blank(), 
                panel.grid.minor = element_blank(),
                panel.border = element_blank(),
                panel.background = element_blank(),
                axis.title = element_blank(),
                axis.text = element_text(size = 8),
                axis.text.x = element_text(angle = 90))
ggsave(paste('_fig//', label_name, '//', label_run, '//', G, '_correlation_', W, '_plot.png', sep = ''), plot = plot) # Save ggplot as jpeg

### Export to Summary File
sink(file = file, append = TRUE, type = 'output')
cat(c('#### ', step_2, '\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### Results for Subgroup: ', G, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### ', test_0, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
summary(OLS)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### ', test_1, '\n\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(utt)
print('Significant = Non-linearity')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### ', test_2, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(jb)
print('Significant = Non-normal')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(ad)
print('Signficiant = Non-normal')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n\n'), file = file, append = TRUE)
cat(c('##### ', test_3, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(dw)
print('Signficiant = Autocorrelation')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n\n'), file = file, append = TRUE)
cat(c('##### ', test_4, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(bp)
print('Signficiant = Homoscedastic')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n\n'), file = file, append = TRUE)
cat(c('##### ', test_5, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(gq)
print('Signficiant = Heteroscedastic')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
sink()


### Regression Step 2: Subgroups
G = 2020

### OLS Assumption 0: Sampling (Observations are a random sample, there are more observations than variables, IV is a result of DV)
test_0 =  'OLS Assumption 0: Sampling (Random sample, observations > predictors, predictor is independent)'
D = subset(df_WXYZ, df_WXYZ[Z] == G, select = c(X, Y))
F = as.formula(paste(Y, ' ~ ', paste(X, collapse = ' + '), sep = ''))
OLS = lm(F, data = D) # Identitiy link [Y = DV*1] (aka: Linear) with gaussian error (aka: Linear regression)

### OLS Assumption 1: Specification (Relationship between predictor and outcome is linear)
test_1 = 'OLS Assumption 1: Specification (Relationship between predictor and outcome is linear)'
utt = raintest(OLS) # Utt's Rainbox Test

### OLS Assumption 2: Normality (Errors are normal with a mean = 0)
test_2 = 'OLS Assumption 2:  Normality (Errors are normal with a mean = 0)'
jb = JarqueBeraTest(resid(OLS)) # Jarque Bera Test
ad = AndersonDarlingTest(resid(OLS)) # Anderson-Darling Test
png(paste('_fig/', label_name, '//', label_run, '//', G, '_QQ_', W, '_plot.png', sep = ''))

qqnorm(resid(OLS))
qqline(resid(OLS))
dev.off()

### OLS Assumption 3: No Autocorrelation (Error terms are not correlated among observations)
test_3 = 'OLS Assumption 3: No Autocorrelation (Error terms are not correlated with each other)'
dw = DurbinWatsonTest(OLS) # Drubin-Watson Test

### OLS Assumption 4: Homoskedasticity (Error terms have constant variance across observations)
test_4 = 'OLS Assumption 4: Homoskedasticity (Error is even across observations)'
bp = bptest(OLS) # Breusch-Pagan Test
gq = gqtest(OLS) # Goldfield Quant Test
png(paste('_fig//', label_name, '//', label_run, '//', G, '_residuals_', W, '_plot.png', sep = ''))
plot(resid(OLS))
abline(0,0)
dev.off()

### OLS Assumption 5: No Colinearity (Predictors are not correlated with each other)
test_5 = 'OLS Assumption 5: No Colinearity (Predictors are not correlated with each other)'
plot = ggplot(subset(data.table::melt(round(cor(df_WXYZ[X], use = "pairwise.complete.obs"), 3)), value < 1), 
                aes(Var1, 
                    Var2)) + 
            geom_tile(aes(
                fill = value)) + 
            geom_text(aes(
                label = value),
                size = 1) + 
            scale_fill_gradient2(
                low = low,
                mid = mid,
                high = high) +
            labs(
                title = paste('Correlation Matrix |', desc_title, sep = " "),
                fill = 'predictor\ncorrelation') +
            theme_minimal() +
            theme(
                text = element_text(family = 'Bookman'),
                plot.title = element_text(size = 12),
                panel.grid.major = element_blank(), 
                panel.grid.minor = element_blank(),
                panel.border = element_blank(),
                panel.background = element_blank(),
                axis.title = element_blank(),
                axis.text = element_text(size = 8),
                axis.text.x = element_text(angle = 90))
ggsave(paste('_fig//', label_name, '//', label_run, '//', G, '_correlation_', W, '_plot.png', sep = ''), plot = plot) # Save ggplot as jpeg


### Export to Summary File
sink(file = file, append = TRUE, type = 'output')
cat(c('#### ', step_2, '\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### Results for Subgroup: ', G, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### ', test_0, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
summary(OLS)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### ', test_1, '\n\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(utt)
print('Significant = Non-linearity')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### ', test_2, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(jb)
print('Significant = Non-normal')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(ad)
print('Signficiant = Non-normal')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n\n'), file = file, append = TRUE)
cat(c('##### ', test_3, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(dw)
print('Signficiant = Autocorrelation')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n\n'), file = file, append = TRUE)
cat(c('##### ', test_4, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(bp)
print('Signficiant = Homoscedastic')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n\n'), file = file, append = TRUE)
cat(c('##### ', test_5, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
print(gq)
print('Signficiant = Heteroscedastic')
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
sink()


## Regression Step 3: Create Generalized Models
step_3 = 'Regression Step 3: Create Generalized Linear Models'

### Create Linear Regression Model
glm = 'DV = Y, regression = linear'
D = subset(df_WXYZ, select = c(X, Y, Z))
F = as.formula(paste(Y, ' ~ ', paste(c(X, Z), collapse = ' + '), sep = ''))
GLM = glm(F, data = D, family = gaussian())

### Create Linear Regression Model with relative mean
df_WXYZ['Y_mean'] = df_WXYZ[Y]/mean(df_WXYZ[[Y]])
glm_0 = 'DV = Y/mean(Y), regression = linear'
D = subset(df_WXYZ, select = c(X, 'Y_mean', Z))
F = as.formula(paste('Y_mean', ' ~ ', paste(c(X, Z), collapse = ' + '), sep = ''))
GLM_0 = glm(F, data = D, family = gaussian()) 

### Create Linear Regression Model with log transformation 
df_WXYZ['Y_log'] = log(df_WXYZ[Y])
df_WXYZ$Y_log[is.infinite(df_WXYZ$Y_log)] <- 0
glm_1 = 'DV = log(Y), regression = linear'
D = subset(df_WXYZ, select = c(X, 'Y_log', Z))
F = as.formula(paste('Y_log', ' ~ ', paste(c(X, Z), collapse = ' + '), sep = ''))
GLM_1 = glm(F, data = D, family = gaussian()) 

### Create Linear Regression Model with polynomials
df_WXYZ['ICD10_sq'] = df_WXYZ['ICD10_TOTAL']^2
X_poly = c('ICD10_sq', 'FPL_PERCENT', 'NON_WHITE', 'AGE', 'SEX')
glm_2 = 'DV^2 = Y, regression = linear'
D = subset(df_WXYZ, select = c(X_poly, Y, Z))
F = as.formula(paste(Y, ' ~ ', paste(c(X_poly, Z), collapse = ' + '), sep = ''))
GLM_2 = glm(F, data = D, family = gaussian()) 

### Create Logistic Regression Model
df_WXYZ['Y_binary'] = 0
df_WXYZ['Y_binary'][df_WXYZ$Y > 0] <- 1 
glm_3 = 'DV = Y > 0, regression = binomial'
D = subset(df_WXYZ, select = c(X, 'Y_binary', Z))
F = as.formula(paste('Y_binary', ' ~ ', paste(c(X, Z), collapse = ' + '), sep = ''))
GLM_3 = glm(F, data = D, family = binomial()) 

### Create Poisson Regression Model
glm_4 = 'DV = Y, regression = poisson'
D = subset(df_WXYZ, select = c(X, Y, Z))
F = as.formula(paste(Y, ' ~ ', paste(c(X, Z), collapse = ' + '), sep = ''))
GLM_4 = glm(F, data = D, family = poisson()) 

### Create Negative Binomial Regression Model
glm_5 = 'DV = Y, regression = negative binomial'
D = subset(df_WXYZ, select = c(X, Y, Z))
F = as.formula(paste(Y, ' ~ ', paste(c(X, Z), collapse = ' + '), sep = ''))
GLM_5 = glm.nb(F, data = D) 

### F-test for overdispersion
test = 1 - pchisq(deviance(GLM), df.residual(GLM)) # Chi-Sq on null deviance to residual deviance
test_0 = 1 - pchisq(deviance(GLM_0), df.residual(GLM_0)) # Chi-Sq on null deviance to residual deviance
test_1 = 1 - pchisq(deviance(GLM_1), df.residual(GLM_1)) # Chi-Sq on null deviance to residual deviance
test_2 = 1 - pchisq(deviance(GLM_2), df.residual(GLM_2)) # Chi-Sq on null deviance to residual deviance
test_3 = 1 - pchisq(deviance(GLM_3), df.residual(GLM_3)) # Chi-Sq on null deviance to residual deviance
test_4 = 1 - pchisq(deviance(GLM_4), df.residual(GLM_4)) # Chi-Sq on null deviance to residual deviance
test_5 = 1 - pchisq(deviance(GLM_5), df.residual(GLM_5)) # Chi-Sq on null deviance to residual deviance

### Export to Summary File
sink(file = file, append = TRUE, type = 'output')
cat(c('#### ', step_3, '\n\n'), file = file, append = TRUE)
cat(c('##### Linear', '\n\n'), file = file, append = TRUE)
cat(c('Generalized model for', glm, '\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
summary(GLM)
print('F-Test for overdispersion: ')
print(test)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### Relative Mean Y', '\n\n'), file = file, append = TRUE)
cat(c('Generalized model for', glm_0, '\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
summary(GLM_0)
print('F-Test for overdispersion: ')
print(test_0)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### Log Transform Y', '\n\n'), file = file, append = TRUE)
cat(c('Generalized model for', glm_1, '\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
summary(GLM_1)
print('F-Test for overdispersion: ')
print(test_1)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### Polynomial', '\n\n'), file = file, append = TRUE)
cat(c('Generalized model for', glm_2, '\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
summary(GLM_2)
print('F-Test for overdispersion: ')
print(test_2)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### Logistic', '\n\n'), file = file, append = TRUE)
cat(c('Generalized model for', glm_3, '\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
summary(GLM_3)
print('F-Test for overdispersion: ')
print(test_3)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### Poisson', '\n\n'), file = file, append = TRUE)
cat(c('Generalized model for', glm_4, '\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
summary(GLM_4)
print('F-Test for overdispersion: ')
print(test_4)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### Negative Binomial', '\n\n'), file = file, append = TRUE)
cat(c('Generalized model for', glm_5, '\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
summary(GLM_5)
print('F-Test for overdispersion: ')
print(test_5)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
sink()

## Regression Step 4: Hierarchical Linear Models
step_4 = 'Regression Step 4: Hierarchical Linear Models'
X2 = c('AGE', 'SEX', 'FPL_PERCENT', 'ICD10_TOTAL')
X_coef = 'RACE'
X_int = 'YEAR'
Y2 = 'Y_log'

#### Varying Intercepts by Racial Group
fix = paste('DV =', Y2, 'regression = linear', 'with varying intercepts by', X_mix)
D = subset(df_WXYZ, select = c(X_mix, X2, Y2, Z))
F = as.formula(paste(Y2, ' ~ (1| ', X_mix, ' ) + ', paste(X2, collapse = ' + '), sep = ''))
FIX = lmer(F, data = D)

#### Varying Intercepts by Racial Group
mix = paste('DV =', Y2, 'regression = linear', 'with varying coeffeicints of', X_int, 'by', X_coef)
D = subset(df_WXYZ, select = c(X_mix, X2, Y2, Z))
F = as.formula(paste(Y2, ' ~ (1 + ', X_coef, ' | ', X_int, ' ) + ', paste(X2, collapse = ' + '), sep = ''))
MIX = lmer(F, data = D)

### One Way ANOVA for MLE
test_1 = 'One Way ANOVA for MLE'
HLM_1 = ranova(FIX)
HLM_2 = ranova(MIX)

### Intra-class correlation coefficient
test_2 = 'Inter class correlation coefficient'
ICC_1 = ICC(HLM_1)
ICC_2 = ICC(HLM_2)

### Export to Summary File
sink(file = file, append = TRUE, type = 'output')
cat(c('#### ', step_4, '\n\n'), file = file, append = TRUE)
cat(c('##### Fixed Efects', '\n\n'), file = file, append = TRUE)
cat(c('Hierarchical model for ', fix, '\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
summary(FIX)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
summary(HLM_1)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
icc(FIX, by_group = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### Random Efects', '\n\n'), file = file, append = TRUE)
cat(c('Hierarchical model for ', mix, '\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
summary(MIX)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
summary(HLM_2)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('####'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
icc(MIX)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
sink()