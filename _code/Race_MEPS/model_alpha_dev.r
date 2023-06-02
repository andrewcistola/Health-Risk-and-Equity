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
df_WXYZ$NON_WHITE[df_WXYZ$RACE != 2 & df_WXYZ$RACE != 5] <- 1
df_WXYZ = df_WXYZ[which(df_WXYZ$RACE < 5), ] # based on variable values

### Transform Y variables
df_WXYZ$Y_raw <- df_WXYZ$PAID_TOTAL
df_WXYZ$Y_binary <- 0
df_WXYZ$Y_binary[df_WXYZ$PAID_TOTAL > 0] <- 1
df_WXYZ$PAID_ZERO <- df_WXYZ$PAID_TOTAL
df_WXYZ$PAID_ZERO[df_WXYZ$PAID_TOTAL == 0 | is.na(df_WXYZ$PAID_ZERO) | is.infinite(df_WXYZ$PAID_ZERO)] <- 0.001
df_WXYZ$Y_log = log(df_WXYZ$PAID_ZERO)
df_WXYZ$Y_scale = df_WXYZ$PAID_ZERO/mean(df_WXYZ$PAID_ZERO)
skim(df_WXYZ)

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

### Final Model - Log
title = 'Final Model: OLS on Log costs, RACE = Missing excluded, 2018-2020'
G = 'FINAL'
W = 'PERSON_ID'
F = as.formula('Y_raw ~  NON_WHITE + AGE + SEX + FPL_PERCENT + ICD10_TOTAL')
D = subset(df_WXYZ, select = c('NON_WHITE', 'AGE', 'SEX', 'FPL_PERCENT', 'ICD10_TOTAL', 'Y_raw'))

### OLS Assumption 0: Sampling (Observations are a random sample, there are more observations than variables, IV is a result of DV)
test_0 =  'OLS Assumption 0: Sampling (Random sample, observations > predictors, predictor is independent)'
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
cat(c('#### ', title, '\n'), file = file, append = TRUE)
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

### Final Model 3 - 2 Part Model
title = 'Final Model 3: Two Step Model on Costs, RACE = Missing excluded, 2018-2020'

#### Step 1
result_1 = 'Logistic Regression on Presence Non-Zero Costs'
F1 = as.formula('Y_binary ~  NON_WHITE + AGE + SEX + FPL_PERCENT + ICD10_TOTAL')
D1 = subset(df_WXYZ, select = c('NON_WHITE', 'AGE', 'SEX', 'FPL_PERCENT', 'ICD10_TOTAL', 'Y_scale', 'Y_binary', 'Y_raw', 'Y_log'))
M1 = glm(F1, family = binomial(link = "logit"), data = D1) 
summary(M1)

#### Step 2 - Log
result_2 = 'Poisson Regression on Costs'
F2 = as.formula('Y_raw ~  NON_WHITE + AGE + SEX + FPL_PERCENT + ICD10_TOTAL')
D2 = D1[which(D1$Y_raw > 0), ] 
M2 = glm(F2, family = poisson(link = "log"), data = D2) 
summary(M2)

### Export to Summary File
sink(file = file, append = TRUE, type = 'output')
cat(c('#### ', title, '\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### ', result_1, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
summary(M1)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('##### ', result_2, '\n\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('<pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
summary(M2)
cat(c('\n'), file = file, append = TRUE)
cat(c('</pre>'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
cat(c('\n'), file = file, append = TRUE)
sink()