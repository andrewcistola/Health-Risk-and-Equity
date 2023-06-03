# Health, Risk, and Equity
#### Risk Heterogeneity between Black and White Individuals Insured through the ACA Marketplaces from 2018-2020
### Andrew S. Cistola, MPH

### About
Previous research have shown signficiant under-utilization of ambulatory care and signficiantly lower costs among black insured individuals 18-64 from 2014-2018. (doi:10.1001/jamanetworkopen.2022.17383) If these differences persist through the ACA risk adjustment program, under-utilization represents an arbitrage opportunity for insurance providers in the individual market. This would represent how a history of systematic racism and barriers to care could be used for cost-containment measures with the beenfits of overall lower health care costs transferred among the larger population. Health equity efforts should be focused on neutralizing arbitrage opporunties based on defacto discrimination and instead incentivize issuers to address disparities in access to care. With the addition of race and zip code to the EDGE server in 2025, CMS will have the ability to reform the ACA risk adjustmenr program to improve these disparities. The purpose of this study is to identify how the ACA Risk Adjustment program interacts with known health disparities in health care utilization among raical groups. This study uses publcily available data from the Medical Expenditure Panel Survey (MEPS) from Agency for Healthcare Research and Quality (AHRQ) (https://meps.ahrq.gov/mepsweb/data_stats/download_data_files.jsp) from 2018 to 2021 to identify differences in risk that can be attributed to racial group independent of other factors and whether the ACA risk adjustment program excacerbates these diferences. Evidence from this study can identify how racial data can be used by CMS to promote health equity within the ACA marketplaces.

#### Notes:
This analysis serves to fulfill part of the the requirements for the PhD in Public Health-Heath Services Research at the University of Florida. The author is also employed by Blue Cross Blue Shield of Florida.

#### Status: 
In development

#### Reference: 
github.com/andrewcistola/Health-Risk-and_Equity

#### Updated:
2022-12-16 15:26:57.640581

### Import Results
The following files were downloaded from https://meps.ahrq.gov/mepsweb/data_files/pufs/ and saved to a local database:

##### AHRQ MEPS 2020
Household Consolidated File (h224)<br>
Medical Conditions File (h222)<br>
Prescribed Medicines File (h220a)<br>
Dental Visits File (h220b)<br>
Other Medical Expenditures File (h220c)<br>
Hospital Inpatient Stays File (h220d)<br>
Emergency Room Visits File (h220e)<br>
Outpatient Department Visits File (h220f)<br>
Office-Based Medical Provider Visits File (h220g)<br>
Home Health Visits File (h220h)<br>
Home Health Visits File (h220h)<br>
Appendix - Condition to Event File (h220if1)<br>
Appendix - Prescritpion to Condition File (h220if2)<br>

##### AHRQ MEPS 2019
Household Consolidated File (h216)<br>
Medical Conditions File (h214)<br>
Prescribed Medicines File (h213a)<br>
Dental Visits File (h213b)<br>
Other Medical Expenditures File (h213c)<br>
Hospital Inpatient Stays File (h213d)<br>
Emergency Room Visits File (h213e)<br>
Outpatient Department Visits File (h213f)<br>
Office-Based Medical Provider Visits File (h213g)<br>
Home Health Visits File (h213h)<br>
Appendix - Condition to Event File (h213if1)<br>
Appendix - Prescritpion to Condition File (h213if2)<br>

##### AHRQ MEPS 2018
Household Consolidated File (h209)<br>
Medical Conditions File (h207)<br>
Prescribed Medicines File (h206a)<br>
Dental Visits File (h206b)<br>
Other Medical Expenditures File (h206c)<br>
Hospital Inpatient Stays File (h206d)<br>
Emergency Room Visits File (h206e)<br>
Outpatient Department Visits File (h206f)<br>
Office-Based Medical Provider Visits File (h206g)<br>
Home Health Visits File (h206h)<br>
Appendix - Condition to Event File (h206if1)<br>
Appendix - Prescritpion to Condition File (h206if2)<br>

See https://datatools.ahrq.gov/meps-hc#varexpLabel for variable explorer.

### Data Cleaning Summary
Raw data was subset for the following conditions:

##### Households
Individuals 26-64 with marketplace coverage for full year

    SELECT
        2020 AS YEAR # Repeated for each year
        , DUPERSID AS PERSON_ID
        , AGELAST AS AGE
        , SEX
        , RACETHX AS RACE
        , POVCAT20 AS FPL_GROUP
        , POVLEV20 AS FPL_PERCENT
    FROM h224 W # Repeated for each household year file
    WHERE
        AGELAST > 18
        AND AGELAST < 65
        AND PRSTX20 = 1 # Variable name charges for each year
        AND INSCOV20 = 1 # Variable name charges for each year
    

##### Events
Non-Dental events for year individual has marketpalce coverage
 
    SELECT
        2020 AS YEAR # Repeated for each year
        , SQ.DUPERSID AS PERSON_ID
        , 'OUTPATIENT' AS SETTING
        , F.EVNTIDX AS EVENT_ID
        , F.OPFPV20X + F.OPDPV20X AS PAID # Combined Doctor and facility payments from privtae insurers for settings that provided both (variable name changes each year)
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y # Repeated for each household year file
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX20 = 1 # Variable name charges for each year
            AND Y.INSCOV20 = 1 # Variable name charges for each year
        ) SQ
    LEFT JOIN h220f F # Repeated for each event file in year
        ON SQ.DUPERSID = F.DUPERSID

Then paid amounts were summed by person and year and joined to household records (exclduing dental).
The setting of the event for each condition was also collected for each event that documented a ICD10 code.

    

##### Conditions
Any for individual in same year as marketpalce coverage

    SELECT
        2020 AS YEAR # Repeated for each year
        , SQ.DUPERSID AS PERSON_ID
        , Z.CONDIDX AS CONDITION_ID
        , Z.EVNTIDX AS EVENT_ID
    FROM (
        SELECT DISTINCT DUPERSID 
        FROM h224 # Repeated for each household year file
        WHERE
            AGELAST > 18
            AND AGELAST < 65
            AND RACETHX IN (1, 2, 3, 4)
            AND PRSTX20 = 1 # Variable name charges for each year
            AND INSCOV20 = 1 # Variable name charges for each year
        ) SQ
    LEFT JOIN h220if1 Z # Repeated for each appendix file
        ON SQ.DUPERSID = Z.DUPERSID

All distinct conditions were kept and joined to household records.
    

##### Final Analytical Data 

<pre>
<class 'pandas.core.frame.DataFrame'>
Int64Index: 140512 entries, 0 to 140511
Data columns (total 12 columns):
 #   Column        Non-Null Count   Dtype  
---  ------        --------------   -----  
 0   YEAR          140512 non-null  int64  
 1   PERSON_ID     140512 non-null  object 
 2   AGE           140512 non-null  float64
 3   SEX           140512 non-null  float64
 4   RACE          140512 non-null  float64
 5   FPL_GROUP     140512 non-null  float64
 6   FPL_PERCENT   140512 non-null  float64
 7   CONDITION_ID  26718 non-null   object 
 8   EVENT_ID      26718 non-null   object 
 9   ICD10         26718 non-null   object 
 10  SETTING       26718 non-null   object 
 11  PAID          26718 non-null   float64
dtypes: float64(6), int64(1), object(5)
memory usage: 13.9+ MB

</pre>
### Data Preparation Summary
The following Columns were derived for this analysis:

    VISITS - VISITS_TOTAL, ER_VISITS, HOME_VISITS, INPATIENT_VISITS, OFFICE_VISITS, OUTPATIENT_VISITS, RX_VISITS
    PAID - PAID_TOTAL, ER_PAID, HOME_PAID, INPATIENT_PAID, OFFICE_PAID, OUTPATIENT_PAID, RX_PAID
    ICD10 - ICD10_TOTAL, ICD10 YES/NO (1/0)
    

##### Descriptive Statistics
The following statistics describe the population used for both analyses:

<pre>
        AGE             ...            
      count       mean  ...   75%   max
YEAR                    ...            
2018  695.0  45.282014  ...  58.0  64.0
2019  646.0  46.202786  ...  58.0  64.0
2020  683.0  46.838946  ...  58.0  64.0

[3 rows x 8 columns]
</pre>

<pre>
                  AGE             ...             
                count       mean  ...    75%   max
YEAR RACE_DESC                    ...             
2018 ASIAN       60.0  41.050000  ...  50.00  64.0
     BLACK       80.0  45.237500  ...  57.00  64.0
     HISPANIC   164.0  43.359756  ...  55.00  64.0
     WHITE      391.0  46.746803  ...  59.00  64.0
2019 ASIAN       63.0  40.031746  ...  51.50  64.0
     BLACK       70.0  47.928571  ...  58.00  64.0
     HISPANIC   154.0  44.110390  ...  56.75  64.0
     WHITE      359.0  47.846797  ...  59.00  64.0
2020 ASIAN       64.0  41.421875  ...  52.25  63.0
     BLACK       82.0  48.865854  ...  59.00  64.0
     HISPANIC   177.0  45.225989  ...  57.00  64.0
     WHITE      360.0  48.133333  ...  60.00  64.0

[12 rows x 8 columns]
</pre>

<pre>
     PERCENT_FEMALE            ...          
              count      mean  ...  75%  max
YEAR                           ...          
2018          695.0  0.592806  ...  1.0  1.0
2019          646.0  0.591331  ...  1.0  1.0
2020          683.0  0.578331  ...  1.0  1.0

[3 rows x 8 columns]
</pre>

<pre>
               PERCENT_FEMALE            ...          
                        count      mean  ...  75%  max
YEAR RACE_DESC                           ...          
2018 ASIAN               60.0  0.616667  ...  1.0  1.0
     BLACK               80.0  0.587500  ...  1.0  1.0
     HISPANIC           164.0  0.591463  ...  1.0  1.0
     WHITE              391.0  0.590793  ...  1.0  1.0
2019 ASIAN               63.0  0.555556  ...  1.0  1.0
     BLACK               70.0  0.685714  ...  1.0  1.0
     HISPANIC           154.0  0.571429  ...  1.0  1.0
     WHITE              359.0  0.587744  ...  1.0  1.0
2020 ASIAN               64.0  0.578125  ...  1.0  1.0
     BLACK               82.0  0.670732  ...  1.0  1.0
     HISPANIC           177.0  0.610169  ...  1.0  1.0
     WHITE              360.0  0.541667  ...  1.0  1.0

[12 rows x 8 columns]
</pre>

<pre>
     FPL_PERCENT              ...                  
           count        mean  ...      75%      max
YEAR                          ...                  
2018       695.0  349.779813  ...  422.475  2411.90
2019       646.0  345.253839  ...  433.720  2727.94
2020       683.0  348.440600  ...  438.170  2100.47

[3 rows x 8 columns]
</pre>

<pre>
               FPL_PERCENT  ...         
                     count  ...      max
YEAR RACE_DESC              ...         
2018 ASIAN            60.0  ...  2215.54
     BLACK            80.0  ...  1011.36
     HISPANIC        164.0  ...  1753.15
     WHITE           391.0  ...  2411.90
2019 ASIAN            63.0  ...  2239.65
     BLACK            70.0  ...   965.99
     HISPANIC        154.0  ...   852.80
     WHITE           359.0  ...  2727.94
2020 ASIAN            64.0  ...  1269.53
     BLACK            82.0  ...   997.19
     HISPANIC        177.0  ...  1186.10
     WHITE           360.0  ...  2100.47

[12 rows x 8 columns]
</pre>

<pre>
     ICD10_TOTAL            ...           
           count      mean  ...  75%   max
YEAR                        ...           
2018       695.0  2.427338  ...  4.0  21.0
2019       646.0  2.272446  ...  3.0  25.0
2020       683.0  2.156662  ...  3.0  19.0

[3 rows x 8 columns]
</pre>

<pre>
               ICD10_TOTAL            ...           
                     count      mean  ...  75%   max
YEAR RACE_DESC                        ...           
2018 ASIAN            60.0  1.283333  ...  2.0  11.0
     BLACK            80.0  2.150000  ...  3.0  14.0
     HISPANIC        164.0  1.774390  ...  3.0  14.0
     WHITE           391.0  2.933504  ...  4.0  21.0
2019 ASIAN            63.0  1.396825  ...  2.0   7.0
     BLACK            70.0  2.614286  ...  4.0  11.0
     HISPANIC        154.0  1.707792  ...  2.0  23.0
     WHITE           359.0  2.601671  ...  4.0  25.0
2020 ASIAN            64.0  1.265625  ...  2.0   7.0
     BLACK            82.0  2.756098  ...  4.0  13.0
     HISPANIC        177.0  1.593220  ...  2.0  17.0
     WHITE           360.0  2.455556  ...  4.0  19.0

[12 rows x 8 columns]
</pre>

<pre>
     PAID_TOTAL  ...           
          count  ...        max
YEAR             ...           
2018      695.0  ...  358442.35
2019      646.0  ...  788295.78
2020      683.0  ...  160834.52

[3 rows x 8 columns]
</pre>

<pre>
               PAID_TOTAL  ...           
                    count  ...        max
YEAR RACE_DESC             ...           
2018 ASIAN           60.0  ...   25184.46
     BLACK           80.0  ...   66465.95
     HISPANIC       164.0  ...   37806.36
     WHITE          391.0  ...  358442.35
2019 ASIAN           63.0  ...   93721.43
     BLACK           70.0  ...  289529.17
     HISPANIC       154.0  ...  788295.78
     WHITE          359.0  ...  219733.64
2020 ASIAN           64.0  ...   27336.65
     BLACK           82.0  ...   51341.60
     HISPANIC       177.0  ...  128095.73
     WHITE          360.0  ...  160834.52

[12 rows x 8 columns]
</pre>

<pre>
     VISITS_TOTAL             ...              
            count       mean  ...   75%     max
YEAR                          ...              
2018        695.0  15.115108  ...  16.0  1322.0
2019        646.0  12.804954  ...  13.0   388.0
2020        683.0  11.626647  ...  14.0   255.0

[3 rows x 8 columns]
</pre>

<pre>
               VISITS_TOTAL  ...        
                      count  ...     max
YEAR RACE_DESC               ...        
2018 ASIAN             60.0  ...   127.0
     BLACK             80.0  ...    80.0
     HISPANIC         164.0  ...   174.0
     WHITE            391.0  ...  1322.0
2019 ASIAN             63.0  ...   130.0
     BLACK             70.0  ...    85.0
     HISPANIC         154.0  ...    87.0
     WHITE            359.0  ...   388.0
2020 ASIAN             64.0  ...    29.0
     BLACK             82.0  ...   164.0
     HISPANIC         177.0  ...    73.0
     WHITE            360.0  ...   255.0

[12 rows x 8 columns]
</pre>

##### Research Question 1: Analytical File

<pre>
<class 'pandas.core.frame.DataFrame'>
Int64Index: 2024 entries, 0 to 2023
Data columns (total 9 columns):
 #   Column        Non-Null Count  Dtype  
---  ------        --------------  -----  
 0   PERSON_ID     2024 non-null   int64  
 1   YEAR          2024 non-null   int64  
 2   AGE           2024 non-null   float64
 3   SEX           2024 non-null   float64
 4   RACE          2024 non-null   float64
 5   FPL_PERCENT   2024 non-null   float64
 6   ICD10_TOTAL   2024 non-null   int32  
 7   PAID_TOTAL    2024 non-null   float64
 8   VISITS_TOTAL  2024 non-null   int64  
dtypes: float64(5), int32(1), int64(3)
memory usage: 150.2 KB

</pre>
##### Research Question 2: Analytical File

<pre>
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 2024 entries, 0 to 2023
Data columns (total 355 columns):
 #    Column             Non-Null Count  Dtype  
---   ------             --------------  -----  
 0    PERSON_ID          2024 non-null   int64  
 1    YEAR               2024 non-null   int64  
 2    AGE                2024 non-null   float64
 3    SEX                2024 non-null   float64
 4    RACE               2024 non-null   float64
 5    FPL_PERCENT        1995 non-null   float64
 6    ICD10_TOTAL        1374 non-null   float64
 7    ER_PAID            182 non-null    float64
 8    HOME_PAID          11 non-null     float64
 9    INPATIENT_PAID     99 non-null     float64
 10   OFFICE_PAID        969 non-null    float64
 11   OUTPATIENT_PAID    236 non-null    float64
 12   RX_PAID            920 non-null    float64
 13   PAID_TOTAL         1277 non-null   float64
 14   ER_VISITS          230 non-null    float64
 15   HOME_VISITS        15 non-null     float64
 16   INPATIENT_VISITS   110 non-null    float64
 17   OFFICE_VISITS      1144 non-null   float64
 18   OUTPATIENT_VISITS  273 non-null    float64
 19   RX_VISITS          1229 non-null   float64
 20   VISITS_TOTAL       1440 non-null   float64
 21   ICD10_A04          2 non-null      float64
 22   ICD10_A08          3 non-null      float64
 23   ICD10_A09          5 non-null      float64
 24   ICD10_A41          1 non-null      float64
 25   ICD10_A49          11 non-null     float64
 26   ICD10_A69          1 non-null      float64
 27   ICD10_B00          18 non-null     float64
 28   ICD10_B02          5 non-null      float64
 29   ICD10_B07          6 non-null      float64
 30   ICD10_B19          4 non-null      float64
 31   ICD10_B34          7 non-null      float64
 32   ICD10_B35          9 non-null      float64
 33   ICD10_B37          27 non-null     float64
 34   ICD10_B49          1 non-null      float64
 35   ICD10_B99          4 non-null      float64
 36   ICD10_C18          2 non-null      float64
 37   ICD10_C34          2 non-null      float64
 38   ICD10_C43          6 non-null      float64
 39   ICD10_C44          20 non-null     float64
 40   ICD10_C50          18 non-null     float64
 41   ICD10_C55          1 non-null      float64
 42   ICD10_C61          1 non-null      float64
 43   ICD10_C64          3 non-null      float64
 44   ICD10_C67          1 non-null      float64
 45   ICD10_C73          5 non-null      float64
 46   ICD10_C85          4 non-null      float64
 47   ICD10_C95          6 non-null      float64
 48   ICD10_D04          1 non-null      float64
 49   ICD10_D17          3 non-null      float64
 50   ICD10_D21          4 non-null      float64
 51   ICD10_D22          10 non-null     float64
 52   ICD10_D48          2 non-null      float64
 53   ICD10_D49          7 non-null      float64
 54   ICD10_D50          3 non-null      float64
 55   ICD10_D64          20 non-null     float64
 56   ICD10_D68          1 non-null      float64
 57   ICD10_E03          86 non-null     float64
 58   ICD10_E04          8 non-null      float64
 59   ICD10_E05          10 non-null     float64
 60   ICD10_E06          6 non-null      float64
 61   ICD10_E07          80 non-null     float64
 62   ICD10_E11          148 non-null    float64
 63   ICD10_E28          5 non-null      float64
 64   ICD10_E29          1 non-null      float64
 65   ICD10_E34          16 non-null     float64
 66   ICD10_E53          4 non-null      float64
 67   ICD10_E55          28 non-null     float64
 68   ICD10_E56          2 non-null      float64
 69   ICD10_E58          1 non-null      float64
 70   ICD10_E61          6 non-null      float64
 71   ICD10_E66          9 non-null      float64
 72   ICD10_E78          273 non-null    float64
 73   ICD10_E83          1 non-null      float64
 74   ICD10_E86          5 non-null      float64
 75   ICD10_E87          14 non-null     float64
 76   ICD10_F10          7 non-null      float64
 77   ICD10_F11          2 non-null      float64
 78   ICD10_F17          1 non-null      float64
 79   ICD10_F19          3 non-null      float64
 80   ICD10_F20          6 non-null      float64
 81   ICD10_F31          15 non-null     float64
 82   ICD10_F32          155 non-null    float64
 83   ICD10_F34          2 non-null      float64
 84   ICD10_F39          4 non-null      float64
 85   ICD10_F41          176 non-null    float64
 86   ICD10_F42          10 non-null     float64
 87   ICD10_F43          42 non-null     float64
 88   ICD10_F51          1 non-null      float64
 89   ICD10_F80          1 non-null      float64
 90   ICD10_F84          2 non-null      float64
 91   ICD10_F90          43 non-null     float64
 92   ICD10_F99          17 non-null     float64
 93   ICD10_G25          23 non-null     float64
 94   ICD10_G35          1 non-null      float64
 95   ICD10_G40          9 non-null      float64
 96   ICD10_G43          43 non-null     float64
 97   ICD10_G44          1 non-null      float64
 98   ICD10_G45          8 non-null      float64
 99   ICD10_G47          101 non-null    float64
 100  ICD10_G54          2 non-null      float64
 101  ICD10_G56          5 non-null      float64
 102  ICD10_G57          6 non-null      float64
 103  ICD10_G58          3 non-null      float64
 104  ICD10_G62          6 non-null      float64
 105  ICD10_G89          15 non-null     float64
 106  ICD10_H00          1 non-null      float64
 107  ICD10_H02          3 non-null      float64
 108  ICD10_H04          8 non-null      float64
 109  ICD10_H10          4 non-null      float64
 110  ICD10_H18          1 non-null      float64
 111  ICD10_H26          15 non-null     float64
 112  ICD10_H33          6 non-null      float64
 113  ICD10_H35          9 non-null      float64
 114  ICD10_H40          16 non-null     float64
 115  ICD10_H43          5 non-null      float64
 116  ICD10_H44          4 non-null      float64
 117  ICD10_H52          34 non-null     float64
 118  ICD10_H53          11 non-null     float64
 119  ICD10_H54          5 non-null      float64
 120  ICD10_H57          17 non-null     float64
 121  ICD10_H61          3 non-null      float64
 122  ICD10_H65          1 non-null      float64
 123  ICD10_H66          18 non-null     float64
 124  ICD10_H72          1 non-null      float64
 125  ICD10_H81          1 non-null      float64
 126  ICD10_H91          3 non-null      float64
 127  ICD10_H92          13 non-null     float64
 128  ICD10_H93          2 non-null      float64
 129  ICD10_I10          404 non-null    float64
 130  ICD10_I20          3 non-null      float64
 131  ICD10_I21          25 non-null     float64
 132  ICD10_I25          24 non-null     float64
 133  ICD10_I34          5 non-null      float64
 134  ICD10_I38          2 non-null      float64
 135  ICD10_I48          7 non-null      float64
 136  ICD10_I49          9 non-null      float64
 137  ICD10_I50          4 non-null      float64
 138  ICD10_I51          9 non-null      float64
 139  ICD10_I63          2 non-null      float64
 140  ICD10_I72          2 non-null      float64
 141  ICD10_I73          6 non-null      float64
 142  ICD10_I74          8 non-null      float64
 143  ICD10_I82          1 non-null      float64
 144  ICD10_I83          3 non-null      float64
 145  ICD10_I87          1 non-null      float64
 146  ICD10_I89          4 non-null      float64
 147  ICD10_I95          1 non-null      float64
 148  ICD10_J00          30 non-null     float64
 149  ICD10_J02          26 non-null     float64
 150  ICD10_J03          3 non-null      float64
 151  ICD10_J06          9 non-null      float64
 152  ICD10_J09          3 non-null      float64
 153  ICD10_J11          53 non-null     float64
 154  ICD10_J18          8 non-null      float64
 155  ICD10_J20          4 non-null      float64
 156  ICD10_J30          30 non-null     float64
 157  ICD10_J32          40 non-null     float64
 158  ICD10_J34          14 non-null     float64
 159  ICD10_J35          1 non-null      float64
 160  ICD10_J39          7 non-null      float64
 161  ICD10_J40          20 non-null     float64
 162  ICD10_J42          9 non-null      float64
 163  ICD10_J43          7 non-null      float64
 164  ICD10_J44          11 non-null     float64
 165  ICD10_J45          100 non-null    float64
 166  ICD10_J98          7 non-null      float64
 167  ICD10_K01          3 non-null      float64
 168  ICD10_K02          1 non-null      float64
 169  ICD10_K04          11 non-null     float64
 170  ICD10_K05          1 non-null      float64
 171  ICD10_K08          20 non-null     float64
 172  ICD10_K21          79 non-null     float64
 173  ICD10_K22          3 non-null      float64
 174  ICD10_K25          2 non-null      float64
 175  ICD10_K29          12 non-null     float64
 176  ICD10_K30          15 non-null     float64
 177  ICD10_K31          9 non-null      float64
 178  ICD10_K37          5 non-null      float64
 179  ICD10_K44          3 non-null      float64
 180  ICD10_K46          6 non-null      float64
 181  ICD10_K51          2 non-null      float64
 182  ICD10_K52          2 non-null      float64
 183  ICD10_K56          1 non-null      float64
 184  ICD10_K57          9 non-null      float64
 185  ICD10_K58          11 non-null     float64
 186  ICD10_K59          5 non-null      float64
 187  ICD10_K63          6 non-null      float64
 188  ICD10_K64          8 non-null      float64
 189  ICD10_K74          2 non-null      float64
 190  ICD10_K76          9 non-null      float64
 191  ICD10_K80          3 non-null      float64
 192  ICD10_K82          7 non-null      float64
 193  ICD10_K85          5 non-null      float64
 194  ICD10_K92          8 non-null      float64
 195  ICD10_L02          7 non-null      float64
 196  ICD10_L03          3 non-null      float64
 197  ICD10_L08          7 non-null      float64
 198  ICD10_L21          1 non-null      float64
 199  ICD10_L23          8 non-null      float64
 200  ICD10_L29          1 non-null      float64
 201  ICD10_L30          22 non-null     float64
 202  ICD10_L40          7 non-null      float64
 203  ICD10_L50          6 non-null      float64
 204  ICD10_L57          2 non-null      float64
 205  ICD10_L60          7 non-null      float64
 206  ICD10_L65          7 non-null      float64
 207  ICD10_L70          17 non-null     float64
 208  ICD10_L71          7 non-null      float64
 209  ICD10_L72          4 non-null      float64
 210  ICD10_L73          1 non-null      float64
 211  ICD10_L81          3 non-null      float64
 212  ICD10_L84          3 non-null      float64
 213  ICD10_L90          1 non-null      float64
 214  ICD10_L91          3 non-null      float64
 215  ICD10_L98          29 non-null     float64
 216  ICD10_M06          29 non-null     float64
 217  ICD10_M10          12 non-null     float64
 218  ICD10_M16          2 non-null      float64
 219  ICD10_M17          7 non-null      float64
 220  ICD10_M19          99 non-null     float64
 221  ICD10_M21          4 non-null      float64
 222  ICD10_M23          1 non-null      float64
 223  ICD10_M25          131 non-null    float64
 224  ICD10_M26          1 non-null      float64
 225  ICD10_M32          9 non-null      float64
 226  ICD10_M35          6 non-null      float64
 227  ICD10_M41          4 non-null      float64
 228  ICD10_M43          6 non-null      float64
 229  ICD10_M46          1 non-null      float64
 230  ICD10_M48          3 non-null      float64
 231  ICD10_M50          1 non-null      float64
 232  ICD10_M51          22 non-null     float64
 233  ICD10_M53          20 non-null     float64
 234  ICD10_M54          117 non-null    float64
 235  ICD10_M62          16 non-null     float64
 236  ICD10_M65          3 non-null      float64
 237  ICD10_M67          4 non-null      float64
 238  ICD10_M71          2 non-null      float64
 239  ICD10_M72          7 non-null      float64
 240  ICD10_M75          6 non-null      float64
 241  ICD10_M76          2 non-null      float64
 242  ICD10_M77          13 non-null     float64
 243  ICD10_M79          76 non-null     float64
 244  ICD10_M81          6 non-null      float64
 245  ICD10_M85          6 non-null      float64
 246  ICD10_M89          1 non-null      float64
 247  ICD10_M99          3 non-null      float64
 248  ICD10_N18          1 non-null      float64
 249  ICD10_N19          1 non-null      float64
 250  ICD10_N20          11 non-null     float64
 251  ICD10_N28          14 non-null     float64
 252  ICD10_N30          12 non-null     float64
 253  ICD10_N32          5 non-null      float64
 254  ICD10_N39          44 non-null     float64
 255  ICD10_N40          2 non-null      float64
 256  ICD10_N41          1 non-null      float64
 257  ICD10_N42          8 non-null      float64
 258  ICD10_N50          2 non-null      float64
 259  ICD10_N52          4 non-null      float64
 260  ICD10_N60          5 non-null      float64
 261  ICD10_N63          10 non-null     float64
 262  ICD10_N64          6 non-null      float64
 263  ICD10_N76          4 non-null      float64
 264  ICD10_N80          3 non-null      float64
 265  ICD10_N81          3 non-null      float64
 266  ICD10_N83          10 non-null     float64
 267  ICD10_N85          2 non-null      float64
 268  ICD10_N89          7 non-null      float64
 269  ICD10_N92          10 non-null     float64
 270  ICD10_N93          2 non-null      float64
 271  ICD10_N94          6 non-null      float64
 272  ICD10_N95          26 non-null     float64
 273  ICD10_O03          2 non-null      float64
 274  ICD10_O80          4 non-null      float64
 275  ICD10_R00          16 non-null     float64
 276  ICD10_R01          6 non-null      float64
 277  ICD10_R03          1 non-null      float64
 278  ICD10_R04          6 non-null      float64
 279  ICD10_R05          18 non-null     float64
 280  ICD10_R06          9 non-null      float64
 281  ICD10_R07          18 non-null     float64
 282  ICD10_R09          3 non-null      float64
 283  ICD10_R10          20 non-null     float64
 284  ICD10_R11          16 non-null     float64
 285  ICD10_R12          8 non-null      float64
 286  ICD10_R13          3 non-null      float64
 287  ICD10_R14          1 non-null      float64
 288  ICD10_R19          13 non-null     float64
 289  ICD10_R20          4 non-null      float64
 290  ICD10_R21          23 non-null     float64
 291  ICD10_R22          13 non-null     float64
 292  ICD10_R25          6 non-null      float64
 293  ICD10_R31          6 non-null      float64
 294  ICD10_R32          4 non-null      float64
 295  ICD10_R33          3 non-null      float64
 296  ICD10_R35          4 non-null      float64
 297  ICD10_R39          3 non-null      float64
 298  ICD10_R41          2 non-null      float64
 299  ICD10_R42          30 non-null     float64
 300  ICD10_R47          2 non-null      float64
 301  ICD10_R50          6 non-null      float64
 302  ICD10_R51          26 non-null     float64
 303  ICD10_R52          34 non-null     float64
 304  ICD10_R53          11 non-null     float64
 305  ICD10_R55          2 non-null      float64
 306  ICD10_R56          11 non-null     float64
 307  ICD10_R58          1 non-null      float64
 308  ICD10_R59          1 non-null      float64
 309  ICD10_R60          30 non-null     float64
 310  ICD10_R63          9 non-null      float64
 311  ICD10_R68          3 non-null      float64
 312  ICD10_R73          14 non-null     float64
 313  ICD10_R79          4 non-null      float64
 314  ICD10_R87          7 non-null      float64
 315  ICD10_R91          4 non-null      float64
 316  ICD10_R94          2 non-null      float64
 317  ICD10_S01          7 non-null      float64
 318  ICD10_S02          3 non-null      float64
 319  ICD10_S05          6 non-null      float64
 320  ICD10_S06          5 non-null      float64
 321  ICD10_S09          5 non-null      float64
 322  ICD10_S13          5 non-null      float64
 323  ICD10_S19          3 non-null      float64
 324  ICD10_S20          1 non-null      float64
 325  ICD10_S22          5 non-null      float64
 326  ICD10_S29          1 non-null      float64
 327  ICD10_S32          5 non-null      float64
 328  ICD10_S39          13 non-null     float64
 329  ICD10_S42          6 non-null      float64
 330  ICD10_S46          2 non-null      float64
 331  ICD10_S49          7 non-null      float64
 332  ICD10_S61          9 non-null      float64
 333  ICD10_S62          11 non-null     float64
 334  ICD10_S63          3 non-null      float64
 335  ICD10_S69          4 non-null      float64
 336  ICD10_S72          2 non-null      float64
 337  ICD10_S73          1 non-null      float64
 338  ICD10_S79          3 non-null      float64
 339  ICD10_S80          2 non-null      float64
 340  ICD10_S81          4 non-null      float64
 341  ICD10_S82          5 non-null      float64
 342  ICD10_S83          5 non-null      float64
 343  ICD10_S86          1 non-null      float64
 344  ICD10_S89          7 non-null      float64
 345  ICD10_S91          2 non-null      float64
 346  ICD10_S92          8 non-null      float64
 347  ICD10_S93          11 non-null     float64
 348  ICD10_S99          7 non-null      float64
 349  ICD10_T07          1 non-null      float64
 350  ICD10_T14          23 non-null     float64
 351  ICD10_T63          6 non-null      float64
 352  ICD10_T78          75 non-null     float64
 353  ICD10_T88          2 non-null      float64
 354  ICD10_U07          20 non-null     float64
dtypes: float64(353), int64(2)
memory usage: 5.5 MB

</pre>
###  Regression Modeling Result Summary 
The following results were collected using  R version 4.2.2 (2022-10-31 ucrt) 

####  Regression Step 1: Import and Clean Data 

Source:  _data//Race_MEPS//alpha_dev_20221216152657//analytical_Q1.csv 

W (ID variables):  PERSON_ID <br>
X (Predictor variables):  NON_WHITE AGE SEX FPL_PERCENT CONDITIONS <br>
Y (Outcome variables):  PAID_TOTAL ALWD_TOTAL <br>
Z (Subgroup variables):  YEAR <br>


<pre>
── Data Summary ────────────────────────
                           Values 
Name                       df_WXYZ
Number of rows             2024   
Number of columns          383    
_______________________           
Column type frequency:            
  numeric                  383    
________________________          
Group variables            None   

── Variable type: numeric ──────────────────────────────────────────────────────
    skim_variable     n_missing complete_rate    mean            sd       p0
  1 PERSON_ID                 0             1 2.38e+9 90986093.      2.29e+9
  2 YEAR                      0             1 2.02e+3        0.825   2.02e+3
  3 HEALTH_STATUS             0             1 2.30e+0        1.12   -8   e+0
  4 HEALTH_BAD                0             1 9.75e-1        0.155   0      
  5 PAID_OOP                  0             1 8.74e+2     1954.      0      
  6 PAID_INS                  0             1 4.25e+3    16856.      0      
  7 ALWD_TOTAL                0             1 5.12e+3    17388.      0      
  8 SDOH_FPL                  0             1 3.48e+2      304.     -5.83e+1
  9 SDOH_EDUCATION            0             1 5.60e-1        0.496   0      
 10 SDOH_MARITAL              0             1 4.91e-1        0.500   0      
 11 SDOH_FOOD                 0             1 6.72e-2        0.250   0      
 12 AGE                       0             1 4.61e+1       13.5     1.9 e+1
 13 SEX                       0             1 1.59e+0        0.492   1   e+0
 14 RACE                      0             1 2.05e+0        0.852   1   e+0
 15 FPL_PERCENT               0             1 3.48e+2      304.     -5.83e+1
 16 ICD10_TOTAL               0             1 2.29e+0        2.80    0      
 17 ER_PAID                   0             1 1.98e+2     1209.      0      
 18 HOME_PAID                 0             1 1.07e+1      263.     -4   e+0
 19 INPATIENT_PAID            0             1 1.31e+3    18865.      0      
 20 OFFICE_PAID               0             1 1.62e+3    12612.      0      
 21 OUTPATIENT_PAID           0             1 6.84e+2     7153.      0      
 22 RX_PAID                   0             1 5.24e+2     2676.      0      
 23 PAID_TOTAL                0             1 4.34e+3    25899.      0      
 24 ER_VISITS                 0             1 1.91e-1        0.709   0      
 25 HOME_VISITS               0             1 4.30e-2        0.708   0      
 26 INPATIENT_VISITS          0             1 7.86e-2        0.375   0      
 27 OFFICE_VISITS             0             1 6.87e+0       34.1     0      
 28 OUTPATIENT_VISITS         0             1 6.04e-1        4.78    0      
 29 RX_VISITS                 0             1 5.41e+0        9.06    0      
 30 VISITS_TOTAL              0             1 1.32e+1       38.5     0      
 31 ICD10_A04                 0             1 9.88e-4        0.0314  0      
 32 ICD10_A08                 0             1 1.48e-3        0.0385  0      
 33 ICD10_A09                 0             1 2.47e-3        0.0497  0      
 34 ICD10_A41                 0             1 4.94e-4        0.0222  0      
 35 ICD10_A49                 0             1 5.43e-3        0.0735  0      
 36 ICD10_A69                 0             1 4.94e-4        0.0222  0      
 37 ICD10_B00                 0             1 8.89e-3        0.0939  0      
 38 ICD10_B02                 0             1 2.47e-3        0.0497  0      
 39 ICD10_B07                 0             1 2.96e-3        0.0544  0      
 40 ICD10_B19                 0             1 1.98e-3        0.0444  0      
 41 ICD10_B34                 0             1 3.46e-3        0.0587  0      
 42 ICD10_B35                 0             1 4.45e-3        0.0666  0      
 43 ICD10_B37                 0             1 1.33e-2        0.115   0      
 44 ICD10_B49                 0             1 4.94e-4        0.0222  0      
 45 ICD10_B99                 0             1 1.98e-3        0.0444  0      
 46 ICD10_C18                 0             1 9.88e-4        0.0314  0      
 47 ICD10_C34                 0             1 9.88e-4        0.0314  0      
 48 ICD10_C43                 0             1 2.96e-3        0.0544  0      
 49 ICD10_C44                 0             1 9.88e-3        0.0989  0      
 50 ICD10_C50                 0             1 8.89e-3        0.0939  0      
 51 ICD10_C55                 0             1 4.94e-4        0.0222  0      
 52 ICD10_C61                 0             1 4.94e-4        0.0222  0      
 53 ICD10_C64                 0             1 1.48e-3        0.0385  0      
 54 ICD10_C67                 0             1 4.94e-4        0.0222  0      
 55 ICD10_C73                 0             1 2.47e-3        0.0497  0      
 56 ICD10_C85                 0             1 1.98e-3        0.0444  0      
 57 ICD10_C95                 0             1 2.96e-3        0.0544  0      
 58 ICD10_D04                 0             1 4.94e-4        0.0222  0      
 59 ICD10_D17                 0             1 1.48e-3        0.0385  0      
 60 ICD10_D21                 0             1 1.98e-3        0.0444  0      
 61 ICD10_D22                 0             1 4.94e-3        0.0701  0      
 62 ICD10_D48                 0             1 9.88e-4        0.0314  0      
 63 ICD10_D49                 0             1 3.46e-3        0.0587  0      
 64 ICD10_D50                 0             1 1.48e-3        0.0385  0      
 65 ICD10_D64                 0             1 9.88e-3        0.0989  0      
 66 ICD10_D68                 0             1 4.94e-4        0.0222  0      
 67 ICD10_E03                 0             1 4.25e-2        0.202   0      
 68 ICD10_E04                 0             1 3.95e-3        0.0628  0      
 69 ICD10_E05                 0             1 4.94e-3        0.0701  0      
 70 ICD10_E06                 0             1 2.96e-3        0.0544  0      
 71 ICD10_E07                 0             1 3.95e-2        0.195   0      
 72 ICD10_E11                 0             1 7.31e-2        0.260   0      
 73 ICD10_E28                 0             1 2.47e-3        0.0497  0      
 74 ICD10_E29                 0             1 4.94e-4        0.0222  0      
 75 ICD10_E34                 0             1 7.91e-3        0.0886  0      
 76 ICD10_E53                 0             1 1.98e-3        0.0444  0      
 77 ICD10_E55                 0             1 1.38e-2        0.117   0      
 78 ICD10_E56                 0             1 9.88e-4        0.0314  0      
 79 ICD10_E58                 0             1 4.94e-4        0.0222  0      
 80 ICD10_E61                 0             1 2.96e-3        0.0544  0      
 81 ICD10_E66                 0             1 4.45e-3        0.0666  0      
 82 ICD10_E78                 0             1 1.35e-1        0.342   0      
 83 ICD10_E83                 0             1 4.94e-4        0.0222  0      
 84 ICD10_E86                 0             1 2.47e-3        0.0497  0      
 85 ICD10_E87                 0             1 6.92e-3        0.0829  0      
 86 ICD10_F10                 0             1 3.46e-3        0.0587  0      
 87 ICD10_F11                 0             1 9.88e-4        0.0314  0      
 88 ICD10_F17                 0             1 4.94e-4        0.0222  0      
 89 ICD10_F19                 0             1 1.48e-3        0.0385  0      
 90 ICD10_F20                 0             1 2.96e-3        0.0544  0      
 91 ICD10_F31                 0             1 7.41e-3        0.0858  0      
 92 ICD10_F32                 0             1 7.66e-2        0.266   0      
 93 ICD10_F34                 0             1 9.88e-4        0.0314  0      
 94 ICD10_F39                 0             1 1.98e-3        0.0444  0      
 95 ICD10_F41                 0             1 8.70e-2        0.282   0      
 96 ICD10_F42                 0             1 4.94e-3        0.0701  0      
 97 ICD10_F43                 0             1 2.08e-2        0.143   0      
 98 ICD10_F51                 0             1 4.94e-4        0.0222  0      
 99 ICD10_F80                 0             1 4.94e-4        0.0222  0      
100 ICD10_F84                 0             1 9.88e-4        0.0314  0      
101 ICD10_F90                 0             1 2.12e-2        0.144   0      
102 ICD10_F99                 0             1 8.40e-3        0.0913  0      
103 ICD10_G25                 0             1 1.14e-2        0.106   0      
104 ICD10_G35                 0             1 4.94e-4        0.0222  0      
105 ICD10_G40                 0             1 4.45e-3        0.0666  0      
106 ICD10_G43                 0             1 2.12e-2        0.144   0      
107 ICD10_G44                 0             1 4.94e-4        0.0222  0      
108 ICD10_G45                 0             1 3.95e-3        0.0628  0      
109 ICD10_G47                 0             1 4.99e-2        0.218   0      
110 ICD10_G54                 0             1 9.88e-4        0.0314  0      
111 ICD10_G56                 0             1 2.47e-3        0.0497  0      
112 ICD10_G57                 0             1 2.96e-3        0.0544  0      
113 ICD10_G58                 0             1 1.48e-3        0.0385  0      
114 ICD10_G62                 0             1 2.96e-3        0.0544  0      
115 ICD10_G89                 0             1 7.41e-3        0.0858  0      
116 ICD10_H00                 0             1 4.94e-4        0.0222  0      
117 ICD10_H02                 0             1 1.48e-3        0.0385  0      
118 ICD10_H04                 0             1 3.95e-3        0.0628  0      
119 ICD10_H10                 0             1 1.98e-3        0.0444  0      
120 ICD10_H18                 0             1 4.94e-4        0.0222  0      
121 ICD10_H26                 0             1 7.41e-3        0.0858  0      
122 ICD10_H33                 0             1 2.96e-3        0.0544  0      
123 ICD10_H35                 0             1 4.45e-3        0.0666  0      
124 ICD10_H40                 0             1 7.91e-3        0.0886  0      
125 ICD10_H43                 0             1 2.47e-3        0.0497  0      
126 ICD10_H44                 0             1 1.98e-3        0.0444  0      
127 ICD10_H52                 0             1 1.68e-2        0.129   0      
128 ICD10_H53                 0             1 5.43e-3        0.0735  0      
129 ICD10_H54                 0             1 2.47e-3        0.0497  0      
130 ICD10_H57                 0             1 8.40e-3        0.0913  0      
131 ICD10_H61                 0             1 1.48e-3        0.0385  0      
132 ICD10_H65                 0             1 4.94e-4        0.0222  0      
133 ICD10_H66                 0             1 8.89e-3        0.0939  0      
134 ICD10_H72                 0             1 4.94e-4        0.0222  0      
135 ICD10_H81                 0             1 4.94e-4        0.0222  0      
136 ICD10_H91                 0             1 1.48e-3        0.0385  0      
137 ICD10_H92                 0             1 6.42e-3        0.0799  0      
138 ICD10_H93                 0             1 9.88e-4        0.0314  0      
139 ICD10_I10                 0             1 2.00e-1        0.400   0      
140 ICD10_I20                 0             1 1.48e-3        0.0385  0      
141 ICD10_I21                 0             1 1.24e-2        0.110   0      
142 ICD10_I25                 0             1 1.19e-2        0.108   0      
143 ICD10_I34                 0             1 2.47e-3        0.0497  0      
144 ICD10_I38                 0             1 9.88e-4        0.0314  0      
145 ICD10_I48                 0             1 3.46e-3        0.0587  0      
146 ICD10_I49                 0             1 4.45e-3        0.0666  0      
147 ICD10_I50                 0             1 1.98e-3        0.0444  0      
148 ICD10_I51                 0             1 4.45e-3        0.0666  0      
149 ICD10_I63                 0             1 9.88e-4        0.0314  0      
150 ICD10_I72                 0             1 9.88e-4        0.0314  0      
151 ICD10_I73                 0             1 2.96e-3        0.0544  0      
152 ICD10_I74                 0             1 3.95e-3        0.0628  0      
153 ICD10_I82                 0             1 4.94e-4        0.0222  0      
154 ICD10_I83                 0             1 1.48e-3        0.0385  0      
155 ICD10_I87                 0             1 4.94e-4        0.0222  0      
156 ICD10_I89                 0             1 1.98e-3        0.0444  0      
157 ICD10_I95                 0             1 4.94e-4        0.0222  0      
158 ICD10_J00                 0             1 1.48e-2        0.121   0      
159 ICD10_J02                 0             1 1.28e-2        0.113   0      
160 ICD10_J03                 0             1 1.48e-3        0.0385  0      
161 ICD10_J06                 0             1 4.45e-3        0.0666  0      
162 ICD10_J09                 0             1 1.48e-3        0.0385  0      
163 ICD10_J11                 0             1 2.62e-2        0.160   0      
164 ICD10_J18                 0             1 3.95e-3        0.0628  0      
165 ICD10_J20                 0             1 1.98e-3        0.0444  0      
166 ICD10_J30                 0             1 1.48e-2        0.121   0      
167 ICD10_J32                 0             1 1.98e-2        0.139   0      
168 ICD10_J34                 0             1 6.92e-3        0.0829  0      
169 ICD10_J35                 0             1 4.94e-4        0.0222  0      
170 ICD10_J39                 0             1 3.46e-3        0.0587  0      
171 ICD10_J40                 0             1 9.88e-3        0.0989  0      
172 ICD10_J42                 0             1 4.45e-3        0.0666  0      
173 ICD10_J43                 0             1 3.46e-3        0.0587  0      
174 ICD10_J44                 0             1 5.43e-3        0.0735  0      
175 ICD10_J45                 0             1 4.94e-2        0.217   0      
176 ICD10_J98                 0             1 3.46e-3        0.0587  0      
177 ICD10_K01                 0             1 1.48e-3        0.0385  0      
178 ICD10_K02                 0             1 4.94e-4        0.0222  0      
179 ICD10_K04                 0             1 5.43e-3        0.0735  0      
180 ICD10_K05                 0             1 4.94e-4        0.0222  0      
181 ICD10_K08                 0             1 9.88e-3        0.0989  0      
182 ICD10_K21                 0             1 3.90e-2        0.194   0      
183 ICD10_K22                 0             1 1.48e-3        0.0385  0      
184 ICD10_K25                 0             1 9.88e-4        0.0314  0      
185 ICD10_K29                 0             1 5.93e-3        0.0768  0      
186 ICD10_K30                 0             1 7.41e-3        0.0858  0      
187 ICD10_K31                 0             1 4.45e-3        0.0666  0      
188 ICD10_K37                 0             1 2.47e-3        0.0497  0      
189 ICD10_K44                 0             1 1.48e-3        0.0385  0      
190 ICD10_K46                 0             1 2.96e-3        0.0544  0      
191 ICD10_K51                 0             1 9.88e-4        0.0314  0      
192 ICD10_K52                 0             1 9.88e-4        0.0314  0      
193 ICD10_K56                 0             1 4.94e-4        0.0222  0      
194 ICD10_K57                 0             1 4.45e-3        0.0666  0      
195 ICD10_K58                 0             1 5.43e-3        0.0735  0      
196 ICD10_K59                 0             1 2.47e-3        0.0497  0      
197 ICD10_K63                 0             1 2.96e-3        0.0544  0      
198 ICD10_K64                 0             1 3.95e-3        0.0628  0      
199 ICD10_K74                 0             1 9.88e-4        0.0314  0      
200 ICD10_K76                 0             1 4.45e-3        0.0666  0      
201 ICD10_K80                 0             1 1.48e-3        0.0385  0      
202 ICD10_K82                 0             1 3.46e-3        0.0587  0      
203 ICD10_K85                 0             1 2.47e-3        0.0497  0      
204 ICD10_K92                 0             1 3.95e-3        0.0628  0      
205 ICD10_L02                 0             1 3.46e-3        0.0587  0      
206 ICD10_L03                 0             1 1.48e-3        0.0385  0      
207 ICD10_L08                 0             1 3.46e-3        0.0587  0      
208 ICD10_L21                 0             1 4.94e-4        0.0222  0      
209 ICD10_L23                 0             1 3.95e-3        0.0628  0      
210 ICD10_L29                 0             1 4.94e-4        0.0222  0      
211 ICD10_L30                 0             1 1.09e-2        0.104   0      
212 ICD10_L40                 0             1 3.46e-3        0.0587  0      
213 ICD10_L50                 0             1 2.96e-3        0.0544  0      
214 ICD10_L57                 0             1 9.88e-4        0.0314  0      
215 ICD10_L60                 0             1 3.46e-3        0.0587  0      
216 ICD10_L65                 0             1 3.46e-3        0.0587  0      
217 ICD10_L70                 0             1 8.40e-3        0.0913  0      
218 ICD10_L71                 0             1 3.46e-3        0.0587  0      
219 ICD10_L72                 0             1 1.98e-3        0.0444  0      
220 ICD10_L73                 0             1 4.94e-4        0.0222  0      
221 ICD10_L81                 0             1 1.48e-3        0.0385  0      
222 ICD10_L84                 0             1 1.48e-3        0.0385  0      
223 ICD10_L90                 0             1 4.94e-4        0.0222  0      
224 ICD10_L91                 0             1 1.48e-3        0.0385  0      
225 ICD10_L98                 0             1 1.43e-2        0.119   0      
226 ICD10_M06                 0             1 1.43e-2        0.119   0      
227 ICD10_M10                 0             1 5.93e-3        0.0768  0      
228 ICD10_M16                 0             1 9.88e-4        0.0314  0      
229 ICD10_M17                 0             1 3.46e-3        0.0587  0      
230 ICD10_M19                 0             1 4.89e-2        0.216   0      
231 ICD10_M21                 0             1 1.98e-3        0.0444  0      
232 ICD10_M23                 0             1 4.94e-4        0.0222  0      
233 ICD10_M25                 0             1 6.47e-2        0.246   0      
234 ICD10_M26                 0             1 4.94e-4        0.0222  0      
235 ICD10_M32                 0             1 4.45e-3        0.0666  0      
236 ICD10_M35                 0             1 2.96e-3        0.0544  0      
237 ICD10_M41                 0             1 1.98e-3        0.0444  0      
238 ICD10_M43                 0             1 2.96e-3        0.0544  0      
239 ICD10_M46                 0             1 4.94e-4        0.0222  0      
240 ICD10_M48                 0             1 1.48e-3        0.0385  0      
241 ICD10_M50                 0             1 4.94e-4        0.0222  0      
242 ICD10_M51                 0             1 1.09e-2        0.104   0      
243 ICD10_M53                 0             1 9.88e-3        0.0989  0      
244 ICD10_M54                 0             1 5.78e-2        0.233   0      
245 ICD10_M62                 0             1 7.91e-3        0.0886  0      
246 ICD10_M65                 0             1 1.48e-3        0.0385  0      
247 ICD10_M67                 0             1 1.98e-3        0.0444  0      
248 ICD10_M71                 0             1 9.88e-4        0.0314  0      
249 ICD10_M72                 0             1 3.46e-3        0.0587  0      
250 ICD10_M75                 0             1 2.96e-3        0.0544  0      
251 ICD10_M76                 0             1 9.88e-4        0.0314  0      
252 ICD10_M77                 0             1 6.42e-3        0.0799  0      
253 ICD10_M79                 0             1 3.75e-2        0.190   0      
254 ICD10_M81                 0             1 2.96e-3        0.0544  0      
255 ICD10_M85                 0             1 2.96e-3        0.0544  0      
256 ICD10_M89                 0             1 4.94e-4        0.0222  0      
257 ICD10_M99                 0             1 1.48e-3        0.0385  0      
258 ICD10_N18                 0             1 4.94e-4        0.0222  0      
259 ICD10_N19                 0             1 4.94e-4        0.0222  0      
260 ICD10_N20                 0             1 5.43e-3        0.0735  0      
261 ICD10_N28                 0             1 6.92e-3        0.0829  0      
262 ICD10_N30                 0             1 5.93e-3        0.0768  0      
263 ICD10_N32                 0             1 2.47e-3        0.0497  0      
264 ICD10_N39                 0             1 2.17e-2        0.146   0      
265 ICD10_N40                 0             1 9.88e-4        0.0314  0      
266 ICD10_N41                 0             1 4.94e-4        0.0222  0      
267 ICD10_N42                 0             1 3.95e-3        0.0628  0      
268 ICD10_N50                 0             1 9.88e-4        0.0314  0      
269 ICD10_N52                 0             1 1.98e-3        0.0444  0      
270 ICD10_N60                 0             1 2.47e-3        0.0497  0      
271 ICD10_N63                 0             1 4.94e-3        0.0701  0      
272 ICD10_N64                 0             1 2.96e-3        0.0544  0      
273 ICD10_N76                 0             1 1.98e-3        0.0444  0      
274 ICD10_N80                 0             1 1.48e-3        0.0385  0      
275 ICD10_N81                 0             1 1.48e-3        0.0385  0      
276 ICD10_N83                 0             1 4.94e-3        0.0701  0      
277 ICD10_N85                 0             1 9.88e-4        0.0314  0      
278 ICD10_N89                 0             1 3.46e-3        0.0587  0      
279 ICD10_N92                 0             1 4.94e-3        0.0701  0      
280 ICD10_N93                 0             1 9.88e-4        0.0314  0      
281 ICD10_N94                 0             1 2.96e-3        0.0544  0      
282 ICD10_N95                 0             1 1.28e-2        0.113   0      
283 ICD10_O03                 0             1 9.88e-4        0.0314  0      
284 ICD10_O80                 0             1 1.98e-3        0.0444  0      
285 ICD10_R00                 0             1 7.91e-3        0.0886  0      
286 ICD10_R01                 0             1 2.96e-3        0.0544  0      
287 ICD10_R03                 0             1 4.94e-4        0.0222  0      
288 ICD10_R04                 0             1 2.96e-3        0.0544  0      
289 ICD10_R05                 0             1 8.89e-3        0.0939  0      
290 ICD10_R06                 0             1 4.45e-3        0.0666  0      
291 ICD10_R07                 0             1 8.89e-3        0.0939  0      
292 ICD10_R09                 0             1 1.48e-3        0.0385  0      
293 ICD10_R10                 0             1 9.88e-3        0.0989  0      
294 ICD10_R11                 0             1 7.91e-3        0.0886  0      
295 ICD10_R12                 0             1 3.95e-3        0.0628  0      
296 ICD10_R13                 0             1 1.48e-3        0.0385  0      
297 ICD10_R14                 0             1 4.94e-4        0.0222  0      
298 ICD10_R19                 0             1 6.42e-3        0.0799  0      
299 ICD10_R20                 0             1 1.98e-3        0.0444  0      
300 ICD10_R21                 0             1 1.14e-2        0.106   0      
301 ICD10_R22                 0             1 6.42e-3        0.0799  0      
302 ICD10_R25                 0             1 2.96e-3        0.0544  0      
303 ICD10_R31                 0             1 2.96e-3        0.0544  0      
304 ICD10_R32                 0             1 1.98e-3        0.0444  0      
305 ICD10_R33                 0             1 1.48e-3        0.0385  0      
306 ICD10_R35                 0             1 1.98e-3        0.0444  0      
307 ICD10_R39                 0             1 1.48e-3        0.0385  0      
308 ICD10_R41                 0             1 9.88e-4        0.0314  0      
309 ICD10_R42                 0             1 1.48e-2        0.121   0      
310 ICD10_R47                 0             1 9.88e-4        0.0314  0      
311 ICD10_R50                 0             1 2.96e-3        0.0544  0      
312 ICD10_R51                 0             1 1.28e-2        0.113   0      
313 ICD10_R52                 0             1 1.68e-2        0.129   0      
314 ICD10_R53                 0             1 5.43e-3        0.0735  0      
315 ICD10_R55                 0             1 9.88e-4        0.0314  0      
316 ICD10_R56                 0             1 5.43e-3        0.0735  0      
317 ICD10_R58                 0             1 4.94e-4        0.0222  0      
318 ICD10_R59                 0             1 4.94e-4        0.0222  0      
319 ICD10_R60                 0             1 1.48e-2        0.121   0      
320 ICD10_R63                 0             1 4.45e-3        0.0666  0      
321 ICD10_R68                 0             1 1.48e-3        0.0385  0      
322 ICD10_R73                 0             1 6.92e-3        0.0829  0      
323 ICD10_R79                 0             1 1.98e-3        0.0444  0      
324 ICD10_R87                 0             1 3.46e-3        0.0587  0      
325 ICD10_R91                 0             1 1.98e-3        0.0444  0      
326 ICD10_R94                 0             1 9.88e-4        0.0314  0      
327 ICD10_S01                 0             1 3.46e-3        0.0587  0      
328 ICD10_S02                 0             1 1.48e-3        0.0385  0      
329 ICD10_S05                 0             1 2.96e-3        0.0544  0      
330 ICD10_S06                 0             1 2.47e-3        0.0497  0      
331 ICD10_S09                 0             1 2.47e-3        0.0497  0      
332 ICD10_S13                 0             1 2.47e-3        0.0497  0      
333 ICD10_S19                 0             1 1.48e-3        0.0385  0      
334 ICD10_S20                 0             1 4.94e-4        0.0222  0      
335 ICD10_S22                 0             1 2.47e-3        0.0497  0      
336 ICD10_S29                 0             1 4.94e-4        0.0222  0      
337 ICD10_S32                 0             1 2.47e-3        0.0497  0      
338 ICD10_S39                 0             1 6.42e-3        0.0799  0      
339 ICD10_S42                 0             1 2.96e-3        0.0544  0      
340 ICD10_S46                 0             1 9.88e-4        0.0314  0      
341 ICD10_S49                 0             1 3.46e-3        0.0587  0      
342 ICD10_S61                 0             1 4.45e-3        0.0666  0      
343 ICD10_S62                 0             1 5.43e-3        0.0735  0      
344 ICD10_S63                 0             1 1.48e-3        0.0385  0      
345 ICD10_S69                 0             1 1.98e-3        0.0444  0      
346 ICD10_S72                 0             1 9.88e-4        0.0314  0      
347 ICD10_S73                 0             1 4.94e-4        0.0222  0      
348 ICD10_S79                 0             1 1.48e-3        0.0385  0      
349 ICD10_S80                 0             1 9.88e-4        0.0314  0      
350 ICD10_S81                 0             1 1.98e-3        0.0444  0      
351 ICD10_S82                 0             1 2.47e-3        0.0497  0      
352 ICD10_S83                 0             1 2.47e-3        0.0497  0      
353 ICD10_S86                 0             1 4.94e-4        0.0222  0      
354 ICD10_S89                 0             1 3.46e-3        0.0587  0      
355 ICD10_S91                 0             1 9.88e-4        0.0314  0      
356 ICD10_S92                 0             1 3.95e-3        0.0628  0      
357 ICD10_S93                 0             1 5.43e-3        0.0735  0      
358 ICD10_S99                 0             1 3.46e-3        0.0587  0      
359 ICD10_T07                 0             1 4.94e-4        0.0222  0      
360 ICD10_T14                 0             1 1.14e-2        0.106   0      
361 ICD10_T63                 0             1 2.96e-3        0.0544  0      
362 ICD10_T78                 0             1 3.71e-2        0.189   0      
363 ICD10_T88                 0             1 9.88e-4        0.0314  0      
364 ICD10_U07                 0             1 9.88e-3        0.0989  0      
365 CONDITIONS                0             1 2.29e+0        2.80    0      
366 HISPANIC                  0             1 2.45e-1        0.430   0      
367 WHITE                     0             1 5.48e-1        0.498   0      
368 BLACK                     0             1 1.15e-1        0.319   0      
369 ASIAN                     0             1 9.24e-2        0.290   0      
370 OTHER                     0             1 0              0       0      
371 NON_WHITE                 0             1 4.52e-1        0.498   0      
372 PAID_raw                  0             1 4.34e+3    25899.      0      
373 PAID_binary               0             1 6.31e-1        0.483   0      
374 PAID_sqrt                 0             1 3.09e+1       58.2     0      
375 PAID_ZERO                 0             1 4.34e+3    25899.      1   e-3
376 PAID_log                  0             1 1.63e+0        6.77   -6.91e+0
377 PAID_scale                0             1 1   e+0        5.96    2.30e-7
378 ALWD_raw                  0             1 5.12e+3    17388.      0      
379 ALWD_binary               0             1 8.45e-1        0.362   0      
380 ALWD_sqrt                 0             1 4.57e+1       55.1     0      
381 ALWD_ZERO                 0             1 5.12e+3    17388.      1   e-3
382 ALWD_log                  0             1 5.04e+0        5.36   -6.91e+0
383 ALWD_scale                0             1 1   e+0        3.40    1.95e-7
         p25     p50     p75         p100 hist 
  1  2.32e+9 2.33e+9 2.46e+9 2579815101   ▇▁▂▂▁
  2  2.02e+3 2.02e+3 2.02e+3       2020   ▇▁▇▁▇
  3  2   e+0 2   e+0 3   e+0          5   ▁▁▁▇▆
  4  1   e+0 1   e+0 1   e+0          1   ▁▁▁▁▇
  5  1   e+1 2.10e+2 8.64e+2      31785   ▇▁▁▁▁
  6  1.98e+1 4.61e+2 2.15e+3     290465   ▇▁▁▁▁
  7  1.70e+2 9.64e+2 3.38e+3     290708   ▇▁▁▁▁
  8  1.58e+2 2.65e+2 4.32e+2       2728.  ▇▂▁▁▁
  9  0       1   e+0 1   e+0          1   ▆▁▁▁▇
 10  0       0       1   e+0          1   ▇▁▁▁▇
 11  0       0       0                1   ▇▁▁▁▁
 12  3.5 e+1 4.9 e+1 5.8 e+1         64   ▃▃▅▅▇
 13  1   e+0 2   e+0 2   e+0          2   ▆▁▁▁▇
 14  2   e+0 2   e+0 2   e+0          4   ▃▇▁▂▂
 15  1.58e+2 2.65e+2 4.32e+2       2728.  ▇▂▁▁▁
 16  0       1   e+0 3   e+0         25   ▇▁▁▁▁
 17  0       0       0            26634   ▇▁▁▁▁
 18  0       0       0            10668   ▇▁▁▁▁
 19  0       0       0           786696   ▇▁▁▁▁
 20  0       0       4.5 e+2     326334   ▇▁▁▁▁
 21  0       0       0           214193   ▇▁▁▁▁
 22  0       0       9.12e+1      59891   ▇▁▁▁▁
 23  0       1.44e+2 1.39e+3     788296.  ▇▁▁▁▁
 24  0       0       0               13   ▇▁▁▁▁
 25  0       0       0               24   ▇▁▁▁▁
 26  0       0       0                4   ▇▁▁▁▁
 27  0       1   e+0 5   e+0       1291   ▇▁▁▁▁
 28  0       0       0              123   ▇▁▁▁▁
 29  0       2   e+0 7   e+0         87   ▇▁▁▁▁
 30  0       4   e+0 1.4 e+1       1322   ▇▁▁▁▁
 31  0       0       0                1   ▇▁▁▁▁
 32  0       0       0                1   ▇▁▁▁▁
 33  0       0       0                1   ▇▁▁▁▁
 34  0       0       0                1   ▇▁▁▁▁
 35  0       0       0                1   ▇▁▁▁▁
 36  0       0       0                1   ▇▁▁▁▁
 37  0       0       0                1   ▇▁▁▁▁
 38  0       0       0                1   ▇▁▁▁▁
 39  0       0       0                1   ▇▁▁▁▁
 40  0       0       0                1   ▇▁▁▁▁
 41  0       0       0                1   ▇▁▁▁▁
 42  0       0       0                1   ▇▁▁▁▁
 43  0       0       0                1   ▇▁▁▁▁
 44  0       0       0                1   ▇▁▁▁▁
 45  0       0       0                1   ▇▁▁▁▁
 46  0       0       0                1   ▇▁▁▁▁
 47  0       0       0                1   ▇▁▁▁▁
 48  0       0       0                1   ▇▁▁▁▁
 49  0       0       0                1   ▇▁▁▁▁
 50  0       0       0                1   ▇▁▁▁▁
 51  0       0       0                1   ▇▁▁▁▁
 52  0       0       0                1   ▇▁▁▁▁
 53  0       0       0                1   ▇▁▁▁▁
 54  0       0       0                1   ▇▁▁▁▁
 55  0       0       0                1   ▇▁▁▁▁
 56  0       0       0                1   ▇▁▁▁▁
 57  0       0       0                1   ▇▁▁▁▁
 58  0       0       0                1   ▇▁▁▁▁
 59  0       0       0                1   ▇▁▁▁▁
 60  0       0       0                1   ▇▁▁▁▁
 61  0       0       0                1   ▇▁▁▁▁
 62  0       0       0                1   ▇▁▁▁▁
 63  0       0       0                1   ▇▁▁▁▁
 64  0       0       0                1   ▇▁▁▁▁
 65  0       0       0                1   ▇▁▁▁▁
 66  0       0       0                1   ▇▁▁▁▁
 67  0       0       0                1   ▇▁▁▁▁
 68  0       0       0                1   ▇▁▁▁▁
 69  0       0       0                1   ▇▁▁▁▁
 70  0       0       0                1   ▇▁▁▁▁
 71  0       0       0                1   ▇▁▁▁▁
 72  0       0       0                1   ▇▁▁▁▁
 73  0       0       0                1   ▇▁▁▁▁
 74  0       0       0                1   ▇▁▁▁▁
 75  0       0       0                1   ▇▁▁▁▁
 76  0       0       0                1   ▇▁▁▁▁
 77  0       0       0                1   ▇▁▁▁▁
 78  0       0       0                1   ▇▁▁▁▁
 79  0       0       0                1   ▇▁▁▁▁
 80  0       0       0                1   ▇▁▁▁▁
 81  0       0       0                1   ▇▁▁▁▁
 82  0       0       0                1   ▇▁▁▁▁
 83  0       0       0                1   ▇▁▁▁▁
 84  0       0       0                1   ▇▁▁▁▁
 85  0       0       0                1   ▇▁▁▁▁
 86  0       0       0                1   ▇▁▁▁▁
 87  0       0       0                1   ▇▁▁▁▁
 88  0       0       0                1   ▇▁▁▁▁
 89  0       0       0                1   ▇▁▁▁▁
 90  0       0       0                1   ▇▁▁▁▁
 91  0       0       0                1   ▇▁▁▁▁
 92  0       0       0                1   ▇▁▁▁▁
 93  0       0       0                1   ▇▁▁▁▁
 94  0       0       0                1   ▇▁▁▁▁
 95  0       0       0                1   ▇▁▁▁▁
 96  0       0       0                1   ▇▁▁▁▁
 97  0       0       0                1   ▇▁▁▁▁
 98  0       0       0                1   ▇▁▁▁▁
 99  0       0       0                1   ▇▁▁▁▁
100  0       0       0                1   ▇▁▁▁▁
101  0       0       0                1   ▇▁▁▁▁
102  0       0       0                1   ▇▁▁▁▁
103  0       0       0                1   ▇▁▁▁▁
104  0       0       0                1   ▇▁▁▁▁
105  0       0       0                1   ▇▁▁▁▁
106  0       0       0                1   ▇▁▁▁▁
107  0       0       0                1   ▇▁▁▁▁
108  0       0       0                1   ▇▁▁▁▁
109  0       0       0                1   ▇▁▁▁▁
110  0       0       0                1   ▇▁▁▁▁
111  0       0       0                1   ▇▁▁▁▁
112  0       0       0                1   ▇▁▁▁▁
113  0       0       0                1   ▇▁▁▁▁
114  0       0       0                1   ▇▁▁▁▁
115  0       0       0                1   ▇▁▁▁▁
116  0       0       0                1   ▇▁▁▁▁
117  0       0       0                1   ▇▁▁▁▁
118  0       0       0                1   ▇▁▁▁▁
119  0       0       0                1   ▇▁▁▁▁
120  0       0       0                1   ▇▁▁▁▁
121  0       0       0                1   ▇▁▁▁▁
122  0       0       0                1   ▇▁▁▁▁
123  0       0       0                1   ▇▁▁▁▁
124  0       0       0                1   ▇▁▁▁▁
125  0       0       0                1   ▇▁▁▁▁
126  0       0       0                1   ▇▁▁▁▁
127  0       0       0                1   ▇▁▁▁▁
128  0       0       0                1   ▇▁▁▁▁
129  0       0       0                1   ▇▁▁▁▁
130  0       0       0                1   ▇▁▁▁▁
131  0       0       0                1   ▇▁▁▁▁
132  0       0       0                1   ▇▁▁▁▁
133  0       0       0                1   ▇▁▁▁▁
134  0       0       0                1   ▇▁▁▁▁
135  0       0       0                1   ▇▁▁▁▁
136  0       0       0                1   ▇▁▁▁▁
137  0       0       0                1   ▇▁▁▁▁
138  0       0       0                1   ▇▁▁▁▁
139  0       0       0                1   ▇▁▁▁▂
140  0       0       0                1   ▇▁▁▁▁
141  0       0       0                1   ▇▁▁▁▁
142  0       0       0                1   ▇▁▁▁▁
143  0       0       0                1   ▇▁▁▁▁
144  0       0       0                1   ▇▁▁▁▁
145  0       0       0                1   ▇▁▁▁▁
146  0       0       0                1   ▇▁▁▁▁
147  0       0       0                1   ▇▁▁▁▁
148  0       0       0                1   ▇▁▁▁▁
149  0       0       0                1   ▇▁▁▁▁
150  0       0       0                1   ▇▁▁▁▁
151  0       0       0                1   ▇▁▁▁▁
152  0       0       0                1   ▇▁▁▁▁
153  0       0       0                1   ▇▁▁▁▁
154  0       0       0                1   ▇▁▁▁▁
155  0       0       0                1   ▇▁▁▁▁
156  0       0       0                1   ▇▁▁▁▁
157  0       0       0                1   ▇▁▁▁▁
158  0       0       0                1   ▇▁▁▁▁
159  0       0       0                1   ▇▁▁▁▁
160  0       0       0                1   ▇▁▁▁▁
161  0       0       0                1   ▇▁▁▁▁
162  0       0       0                1   ▇▁▁▁▁
163  0       0       0                1   ▇▁▁▁▁
164  0       0       0                1   ▇▁▁▁▁
165  0       0       0                1   ▇▁▁▁▁
166  0       0       0                1   ▇▁▁▁▁
167  0       0       0                1   ▇▁▁▁▁
168  0       0       0                1   ▇▁▁▁▁
169  0       0       0                1   ▇▁▁▁▁
170  0       0       0                1   ▇▁▁▁▁
171  0       0       0                1   ▇▁▁▁▁
172  0       0       0                1   ▇▁▁▁▁
173  0       0       0                1   ▇▁▁▁▁
174  0       0       0                1   ▇▁▁▁▁
175  0       0       0                1   ▇▁▁▁▁
176  0       0       0                1   ▇▁▁▁▁
177  0       0       0                1   ▇▁▁▁▁
178  0       0       0                1   ▇▁▁▁▁
179  0       0       0                1   ▇▁▁▁▁
180  0       0       0                1   ▇▁▁▁▁
181  0       0       0                1   ▇▁▁▁▁
182  0       0       0                1   ▇▁▁▁▁
183  0       0       0                1   ▇▁▁▁▁
184  0       0       0                1   ▇▁▁▁▁
185  0       0       0                1   ▇▁▁▁▁
186  0       0       0                1   ▇▁▁▁▁
187  0       0       0                1   ▇▁▁▁▁
188  0       0       0                1   ▇▁▁▁▁
189  0       0       0                1   ▇▁▁▁▁
190  0       0       0                1   ▇▁▁▁▁
191  0       0       0                1   ▇▁▁▁▁
192  0       0       0                1   ▇▁▁▁▁
193  0       0       0                1   ▇▁▁▁▁
194  0       0       0                1   ▇▁▁▁▁
195  0       0       0                1   ▇▁▁▁▁
196  0       0       0                1   ▇▁▁▁▁
197  0       0       0                1   ▇▁▁▁▁
198  0       0       0                1   ▇▁▁▁▁
199  0       0       0                1   ▇▁▁▁▁
200  0       0       0                1   ▇▁▁▁▁
201  0       0       0                1   ▇▁▁▁▁
202  0       0       0                1   ▇▁▁▁▁
203  0       0       0                1   ▇▁▁▁▁
204  0       0       0                1   ▇▁▁▁▁
205  0       0       0                1   ▇▁▁▁▁
206  0       0       0                1   ▇▁▁▁▁
207  0       0       0                1   ▇▁▁▁▁
208  0       0       0                1   ▇▁▁▁▁
209  0       0       0                1   ▇▁▁▁▁
210  0       0       0                1   ▇▁▁▁▁
211  0       0       0                1   ▇▁▁▁▁
212  0       0       0                1   ▇▁▁▁▁
213  0       0       0                1   ▇▁▁▁▁
214  0       0       0                1   ▇▁▁▁▁
215  0       0       0                1   ▇▁▁▁▁
216  0       0       0                1   ▇▁▁▁▁
217  0       0       0                1   ▇▁▁▁▁
218  0       0       0                1   ▇▁▁▁▁
219  0       0       0                1   ▇▁▁▁▁
220  0       0       0                1   ▇▁▁▁▁
221  0       0       0                1   ▇▁▁▁▁
222  0       0       0                1   ▇▁▁▁▁
223  0       0       0                1   ▇▁▁▁▁
224  0       0       0                1   ▇▁▁▁▁
225  0       0       0                1   ▇▁▁▁▁
226  0       0       0                1   ▇▁▁▁▁
227  0       0       0                1   ▇▁▁▁▁
228  0       0       0                1   ▇▁▁▁▁
229  0       0       0                1   ▇▁▁▁▁
230  0       0       0                1   ▇▁▁▁▁
231  0       0       0                1   ▇▁▁▁▁
232  0       0       0                1   ▇▁▁▁▁
233  0       0       0                1   ▇▁▁▁▁
234  0       0       0                1   ▇▁▁▁▁
235  0       0       0                1   ▇▁▁▁▁
236  0       0       0                1   ▇▁▁▁▁
237  0       0       0                1   ▇▁▁▁▁
238  0       0       0                1   ▇▁▁▁▁
239  0       0       0                1   ▇▁▁▁▁
240  0       0       0                1   ▇▁▁▁▁
241  0       0       0                1   ▇▁▁▁▁
242  0       0       0                1   ▇▁▁▁▁
243  0       0       0                1   ▇▁▁▁▁
244  0       0       0                1   ▇▁▁▁▁
245  0       0       0                1   ▇▁▁▁▁
246  0       0       0                1   ▇▁▁▁▁
247  0       0       0                1   ▇▁▁▁▁
248  0       0       0                1   ▇▁▁▁▁
249  0       0       0                1   ▇▁▁▁▁
250  0       0       0                1   ▇▁▁▁▁
251  0       0       0                1   ▇▁▁▁▁
252  0       0       0                1   ▇▁▁▁▁
253  0       0       0                1   ▇▁▁▁▁
254  0       0       0                1   ▇▁▁▁▁
255  0       0       0                1   ▇▁▁▁▁
256  0       0       0                1   ▇▁▁▁▁
257  0       0       0                1   ▇▁▁▁▁
258  0       0       0                1   ▇▁▁▁▁
259  0       0       0                1   ▇▁▁▁▁
260  0       0       0                1   ▇▁▁▁▁
261  0       0       0                1   ▇▁▁▁▁
262  0       0       0                1   ▇▁▁▁▁
263  0       0       0                1   ▇▁▁▁▁
264  0       0       0                1   ▇▁▁▁▁
265  0       0       0                1   ▇▁▁▁▁
266  0       0       0                1   ▇▁▁▁▁
267  0       0       0                1   ▇▁▁▁▁
268  0       0       0                1   ▇▁▁▁▁
269  0       0       0                1   ▇▁▁▁▁
270  0       0       0                1   ▇▁▁▁▁
271  0       0       0                1   ▇▁▁▁▁
272  0       0       0                1   ▇▁▁▁▁
273  0       0       0                1   ▇▁▁▁▁
274  0       0       0                1   ▇▁▁▁▁
275  0       0       0                1   ▇▁▁▁▁
276  0       0       0                1   ▇▁▁▁▁
277  0       0       0                1   ▇▁▁▁▁
278  0       0       0                1   ▇▁▁▁▁
279  0       0       0                1   ▇▁▁▁▁
280  0       0       0                1   ▇▁▁▁▁
281  0       0       0                1   ▇▁▁▁▁
282  0       0       0                1   ▇▁▁▁▁
283  0       0       0                1   ▇▁▁▁▁
284  0       0       0                1   ▇▁▁▁▁
285  0       0       0                1   ▇▁▁▁▁
286  0       0       0                1   ▇▁▁▁▁
287  0       0       0                1   ▇▁▁▁▁
288  0       0       0                1   ▇▁▁▁▁
289  0       0       0                1   ▇▁▁▁▁
290  0       0       0                1   ▇▁▁▁▁
291  0       0       0                1   ▇▁▁▁▁
292  0       0       0                1   ▇▁▁▁▁
293  0       0       0                1   ▇▁▁▁▁
294  0       0       0                1   ▇▁▁▁▁
295  0       0       0                1   ▇▁▁▁▁
296  0       0       0                1   ▇▁▁▁▁
297  0       0       0                1   ▇▁▁▁▁
298  0       0       0                1   ▇▁▁▁▁
299  0       0       0                1   ▇▁▁▁▁
300  0       0       0                1   ▇▁▁▁▁
301  0       0       0                1   ▇▁▁▁▁
302  0       0       0                1   ▇▁▁▁▁
303  0       0       0                1   ▇▁▁▁▁
304  0       0       0                1   ▇▁▁▁▁
305  0       0       0                1   ▇▁▁▁▁
306  0       0       0                1   ▇▁▁▁▁
307  0       0       0                1   ▇▁▁▁▁
308  0       0       0                1   ▇▁▁▁▁
309  0       0       0                1   ▇▁▁▁▁
310  0       0       0                1   ▇▁▁▁▁
311  0       0       0                1   ▇▁▁▁▁
312  0       0       0                1   ▇▁▁▁▁
313  0       0       0                1   ▇▁▁▁▁
314  0       0       0                1   ▇▁▁▁▁
315  0       0       0                1   ▇▁▁▁▁
316  0       0       0                1   ▇▁▁▁▁
317  0       0       0                1   ▇▁▁▁▁
318  0       0       0                1   ▇▁▁▁▁
319  0       0       0                1   ▇▁▁▁▁
320  0       0       0                1   ▇▁▁▁▁
321  0       0       0                1   ▇▁▁▁▁
322  0       0       0                1   ▇▁▁▁▁
323  0       0       0                1   ▇▁▁▁▁
324  0       0       0                1   ▇▁▁▁▁
325  0       0       0                1   ▇▁▁▁▁
326  0       0       0                1   ▇▁▁▁▁
327  0       0       0                1   ▇▁▁▁▁
328  0       0       0                1   ▇▁▁▁▁
329  0       0       0                1   ▇▁▁▁▁
330  0       0       0                1   ▇▁▁▁▁
331  0       0       0                1   ▇▁▁▁▁
332  0       0       0                1   ▇▁▁▁▁
333  0       0       0                1   ▇▁▁▁▁
334  0       0       0                1   ▇▁▁▁▁
335  0       0       0                1   ▇▁▁▁▁
336  0       0       0                1   ▇▁▁▁▁
337  0       0       0                1   ▇▁▁▁▁
338  0       0       0                1   ▇▁▁▁▁
339  0       0       0                1   ▇▁▁▁▁
340  0       0       0                1   ▇▁▁▁▁
341  0       0       0                1   ▇▁▁▁▁
342  0       0       0                1   ▇▁▁▁▁
343  0       0       0                1   ▇▁▁▁▁
344  0       0       0                1   ▇▁▁▁▁
345  0       0       0                1   ▇▁▁▁▁
346  0       0       0                1   ▇▁▁▁▁
347  0       0       0                1   ▇▁▁▁▁
348  0       0       0                1   ▇▁▁▁▁
349  0       0       0                1   ▇▁▁▁▁
350  0       0       0                1   ▇▁▁▁▁
351  0       0       0                1   ▇▁▁▁▁
352  0       0       0                1   ▇▁▁▁▁
353  0       0       0                1   ▇▁▁▁▁
354  0       0       0                1   ▇▁▁▁▁
355  0       0       0                1   ▇▁▁▁▁
356  0       0       0                1   ▇▁▁▁▁
357  0       0       0                1   ▇▁▁▁▁
358  0       0       0                1   ▇▁▁▁▁
359  0       0       0                1   ▇▁▁▁▁
360  0       0       0                1   ▇▁▁▁▁
361  0       0       0                1   ▇▁▁▁▁
362  0       0       0                1   ▇▁▁▁▁
363  0       0       0                1   ▇▁▁▁▁
364  0       0       0                1   ▇▁▁▁▁
365  0       1   e+0 3   e+0         25   ▇▁▁▁▁
366  0       0       0                1   ▇▁▁▁▂
367  0       1   e+0 1   e+0          1   ▆▁▁▁▇
368  0       0       0                1   ▇▁▁▁▁
369  0       0       0                1   ▇▁▁▁▁
370  0       0       0                0   ▁▁▇▁▁
371  0       0       1   e+0          1   ▇▁▁▁▆
372  0       1.44e+2 1.39e+3     788296.  ▇▁▁▁▁
373  0       1   e+0 1   e+0          1   ▅▁▁▁▇
374  0       1.20e+1 3.72e+1        888.  ▇▁▁▁▁
375  1   e-3 1.44e+2 1.39e+3     788296.  ▇▁▁▁▁
376 -6.91e+0 4.97e+0 7.24e+0         13.6 ▇▁▃▇▁
377  2.30e-7 3.32e-2 3.19e-1        182.  ▇▁▁▁▁
378  1.70e+2 9.64e+2 3.38e+3     290708   ▇▁▁▁▁
379  1   e+0 1   e+0 1   e+0          1   ▂▁▁▁▇
380  1.30e+1 3.11e+1 5.81e+1        539.  ▇▁▁▁▁
381  1.70e+2 9.64e+2 3.38e+3     290708   ▇▁▁▁▁
382  5.13e+0 6.87e+0 8.13e+0         12.6 ▂▁▁▇▂
383  3.32e-2 1.88e-1 6.60e-1         56.8 ▇▁▁▁▁

</pre>

####  OLS on Log costs 

#####  OLS Assumption 0: Sampling (Random sample, observations > predictors, predictor is independent) 


<pre>

Call:
lm(formula = F, data = D)

Residuals:
     Min       1Q   Median       3Q      Max 
-24.4085  -4.8811   0.8782   4.5915  13.2833 

Coefficients:
              Estimate Std. Error t value Pr(>|t|)    
(Intercept) -2.2940849  0.6000889  -3.823 0.000136 ***
NON_WHITE   -1.0150293  0.2440262  -4.160 3.32e-05 ***
AGE          0.0157353  0.0091808   1.714 0.086695 .  
SEX          0.3416215  0.2445122   1.397 0.162520    
FPL_PERCENT -0.0004224  0.0003952  -1.069 0.285342    
CONDITIONS   1.4278794  0.0452794  31.535  < 2e-16 ***
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Residual standard error: 5.297 on 2018 degrees of freedom
Multiple R-squared:  0.3885,	Adjusted R-squared:  0.387 
F-statistic: 256.4 on 5 and 2018 DF,  p-value: < 2.2e-16


</pre>

#####  OLS Assumption 1: Specification (Relationship between predictor and outcome is linear) 

<pre>

	Rainbow test

data:  OLS
Rain = 0.98729, df1 = 1012, df2 = 1006, p-value = 0.5805

[1] "Significant = Non-linearity"

</pre>
#####  OLS Assumption 2:  Normality (Errors are normal with a mean = 0) 


<pre>

	Robust Jarque Bera Test

data:  resid(OLS)
X-squared = 88.531, df = 2, p-value < 2.2e-16

[1] "Significant = Non-normal"

</pre>

<pre>

	Anderson-Darling test of goodness-of-fit
	Null hypothesis: uniform distribution

data:  resid(OLS)
An = Inf, p-value = 2.964e-07

[1] "Signficiant = Non-normal"

</pre>

#####  OLS Assumption 3: No Autocorrelation (Error terms are not correlated with each other) 


<pre>

	Durbin-Watson test

data:  OLS
DW = 1.9245, p-value = 0.04356
alternative hypothesis: true autocorrelation is greater than 0

[1] "Signficiant = Autocorrelation"

</pre>

#####  OLS Assumption 4: Homoskedasticity (Error is even across observations) 


<pre>

	studentized Breusch-Pagan test

data:  OLS
BP = 42.021, df = 5, p-value = 5.833e-08

[1] "Signficiant = Homoscedastic"

</pre>

#####  OLS Assumption 5: No Colinearity (Predictors are not correlated with each other) 


<pre>

	Goldfeld-Quandt test

data:  OLS
GQ = 0.9924, df1 = 1006, df2 = 1006, p-value = 0.5482
alternative hypothesis: variance increases from segment 1 to 2

[1] "Signficiant = Heteroscedastic"

</pre>

###  Paid Amount: Visit Based Paid Amounts 

####  OLS on Square Root costs 

#####  OLS Assumption 0: Sampling (Random sample, observations > predictors, predictor is independent) 


<pre>

Call:
lm(formula = F, data = D)

Residuals:
    Min      1Q  Median      3Q     Max 
-125.75  -15.83   -7.91   -0.77  813.20 

Coefficients:
             Estimate Std. Error t value Pr(>|t|)    
(Intercept) 20.500363   5.730557   3.577 0.000355 ***
NON_WHITE   -4.637047   2.330332  -1.990 0.046740 *  
AGE         -0.062916   0.087673  -0.718 0.473074    
SEX         -5.068871   2.334972  -2.171 0.030059 *  
FPL_PERCENT -0.001002   0.003774  -0.265 0.790683    
CONDITIONS  10.388033   0.432396  24.024  < 2e-16 ***
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Residual standard error: 50.59 on 2018 degrees of freedom
Multiple R-squared:  0.2473,	Adjusted R-squared:  0.2455 
F-statistic: 132.6 on 5 and 2018 DF,  p-value: < 2.2e-16


</pre>

#####  OLS Assumption 1: Specification (Relationship between predictor and outcome is linear) 

<pre>

	Rainbow test

data:  OLS
Rain = 0.64372, df1 = 1012, df2 = 1006, p-value = 1

[1] "Significant = Non-linearity"

</pre>
#####  OLS Assumption 2:  Normality (Errors are normal with a mean = 0) 


<pre>

	Robust Jarque Bera Test

data:  resid(OLS)
X-squared = 16449832, df = 2, p-value < 2.2e-16

[1] "Significant = Non-normal"

</pre>

<pre>

	Anderson-Darling test of goodness-of-fit
	Null hypothesis: uniform distribution

data:  resid(OLS)
An = Inf, p-value = 2.964e-07

[1] "Signficiant = Non-normal"

</pre>

#####  OLS Assumption 3: No Autocorrelation (Error terms are not correlated with each other) 


<pre>

	Durbin-Watson test

data:  OLS
DW = 2.013, p-value = 0.6107
alternative hypothesis: true autocorrelation is greater than 0

[1] "Signficiant = Autocorrelation"

</pre>

#####  OLS Assumption 4: Homoskedasticity (Error is even across observations) 


<pre>

	studentized Breusch-Pagan test

data:  OLS
BP = 40.807, df = 5, p-value = 1.026e-07

[1] "Signficiant = Homoscedastic"

</pre>

#####  OLS Assumption 5: No Colinearity (Predictors are not correlated with each other) 


<pre>

	Goldfeld-Quandt test

data:  OLS
GQ = 0.92879, df1 = 1006, df2 = 1006, p-value = 0.8792
alternative hypothesis: variance increases from segment 1 to 2

[1] "Signficiant = Heteroscedastic"

</pre>

####  Two Part Model (Logistic for non-zero, then Log link) 

#####  Two part model: logistic and poisson 


<pre>
$Firstpart.model

Call:
glm(formula = nonzero ~ NON_WHITE + AGE + SEX + FPL_PERCENT + 
    CONDITIONS, family = binomial(link = "logit"), data = D)

Deviance Residuals: 
    Min       1Q   Median       3Q      Max  
-5.3547  -0.5765   0.0222   0.4258   2.1284  

Coefficients:
              Estimate Std. Error z value Pr(>|z|)    
(Intercept) -1.2286588  0.3329280  -3.690 0.000224 ***
NON_WHITE   -0.2056304  0.1411403  -1.457 0.145138    
AGE         -0.0058846  0.0052915  -1.112 0.266105    
SEX          0.0622418  0.1391154   0.447 0.654578    
FPL_PERCENT -0.0005318  0.0002375  -2.239 0.025166 *  
CONDITIONS   1.9882384  0.0983395  20.218  < 2e-16 ***
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

(Dispersion parameter for binomial family taken to be 1)

    Null deviance: 2665.4  on 2023  degrees of freedom
Residual deviance: 1320.5  on 2018  degrees of freedom
AIC: 1332.5

Number of Fisher Scoring iterations: 7


$Secondpart.model

Call:
glm(formula = Y_raw ~ NON_WHITE + AGE + SEX + FPL_PERCENT + CONDITIONS, 
    family = poisson(link = "log"), data = D)

Deviance Residuals: 
    Min       1Q   Median       3Q      Max  
-402.69   -94.48   -76.28   -44.64  2368.18  

Coefficients:
              Estimate Std. Error z value Pr(>|z|)    
(Intercept)  8.996e+00  1.858e-03 4841.73   <2e-16 ***
NON_WHITE   -8.465e-02  7.213e-04 -117.34   <2e-16 ***
AGE         -3.036e-03  2.840e-05 -106.90   <2e-16 ***
SEX         -4.353e-01  7.286e-04 -597.42   <2e-16 ***
FPL_PERCENT -5.337e-05  1.212e-06  -44.02   <2e-16 ***
CONDITIONS   1.677e-01  6.957e-05 2410.62   <2e-16 ***
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

(Dispersion parameter for poisson family taken to be 1)

    Null deviance: 34770303  on 1276  degrees of freedom
Residual deviance: 30270956  on 1271  degrees of freedom
AIC: Inf

Number of Fisher Scoring iterations: 7



</pre>

###  Allowed Amount: Insurance plus out of pocket 

####  OLS on Log costs 

#####  OLS Assumption 0: Sampling (Random sample, observations > predictors, predictor is independent) 


<pre>

Call:
lm(formula = F, data = D)

Residuals:
    Min      1Q  Median      3Q     Max 
-15.636  -0.868   1.380   2.945   8.779 

Coefficients:
             Estimate Std. Error t value Pr(>|t|)    
(Intercept)  0.531899   0.519213   1.024  0.30575    
NON_WHITE   -1.672911   0.211138  -7.923 3.79e-15 ***
AGE          0.037607   0.007943   4.734 2.35e-06 ***
SEX          0.874644   0.211559   4.134 3.71e-05 ***
FPL_PERCENT  0.001000   0.000342   2.925  0.00348 ** 
CONDITIONS   0.786194   0.039177  20.068  < 2e-16 ***
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Residual standard error: 4.583 on 2018 degrees of freedom
Multiple R-squared:  0.2699,	Adjusted R-squared:  0.2681 
F-statistic: 149.2 on 5 and 2018 DF,  p-value: < 2.2e-16


</pre>

#####  OLS Assumption 1: Specification (Relationship between predictor and outcome is linear) 

<pre>

	Rainbow test

data:  OLS
Rain = 1.0495, df1 = 1012, df2 = 1006, p-value = 0.2216

[1] "Significant = Non-linearity"

</pre>
#####  OLS Assumption 2:  Normality (Errors are normal with a mean = 0) 


<pre>

	Robust Jarque Bera Test

data:  resid(OLS)
X-squared = 1373.1, df = 2, p-value < 2.2e-16

[1] "Significant = Non-normal"

</pre>

<pre>

	Anderson-Darling test of goodness-of-fit
	Null hypothesis: uniform distribution

data:  resid(OLS)
An = Inf, p-value = 2.964e-07

[1] "Signficiant = Non-normal"

</pre>

#####  OLS Assumption 3: No Autocorrelation (Error terms are not correlated with each other) 


<pre>

	Durbin-Watson test

data:  OLS
DW = 1.8107, p-value = 9.686e-06
alternative hypothesis: true autocorrelation is greater than 0

[1] "Signficiant = Autocorrelation"

</pre>

#####  OLS Assumption 4: Homoskedasticity (Error is even across observations) 


<pre>

	studentized Breusch-Pagan test

data:  OLS
BP = 233.71, df = 5, p-value < 2.2e-16

[1] "Signficiant = Homoscedastic"

</pre>

#####  OLS Assumption 5: No Colinearity (Predictors are not correlated with each other) 


<pre>

	Goldfeld-Quandt test

data:  OLS
GQ = 0.94324, df1 = 1006, df2 = 1006, p-value = 0.8229
alternative hypothesis: variance increases from segment 1 to 2

[1] "Signficiant = Heteroscedastic"

</pre>

####  OLS on Square Root costs 

#####  OLS Assumption 0: Sampling (Random sample, observations > predictors, predictor is independent) 


<pre>

Call:
lm(formula = F, data = D)

Residuals:
    Min      1Q  Median      3Q     Max 
-128.29  -20.53  -11.04    7.75  483.43 

Coefficients:
             Estimate Std. Error t value Pr(>|t|)    
(Intercept) 21.539786   5.264013   4.092 4.45e-05 ***
NON_WHITE   -9.436029   2.140612  -4.408 1.10e-05 ***
AGE          0.094622   0.080535   1.175   0.2402    
SEX         -1.131351   2.144875  -0.527   0.5979    
FPL_PERCENT  0.007997   0.003467   2.307   0.0212 *  
CONDITIONS  10.080718   0.397193  25.380  < 2e-16 ***
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Residual standard error: 46.47 on 2018 degrees of freedom
Multiple R-squared:  0.2903,	Adjusted R-squared:  0.2885 
F-statistic: 165.1 on 5 and 2018 DF,  p-value: < 2.2e-16


</pre>

#####  OLS Assumption 1: Specification (Relationship between predictor and outcome is linear) 

<pre>

	Rainbow test

data:  OLS
Rain = 0.77213, df1 = 1012, df2 = 1006, p-value = 1

[1] "Significant = Non-linearity"

</pre>
#####  OLS Assumption 2:  Normality (Errors are normal with a mean = 0) 


<pre>

	Robust Jarque Bera Test

data:  resid(OLS)
X-squared = 558954, df = 2, p-value < 2.2e-16

[1] "Significant = Non-normal"

</pre>

<pre>

	Anderson-Darling test of goodness-of-fit
	Null hypothesis: uniform distribution

data:  resid(OLS)
An = Inf, p-value = 2.964e-07

[1] "Signficiant = Non-normal"

</pre>

#####  OLS Assumption 3: No Autocorrelation (Error terms are not correlated with each other) 


<pre>

	Durbin-Watson test

data:  OLS
DW = 2.0212, p-value = 0.6789
alternative hypothesis: true autocorrelation is greater than 0

[1] "Signficiant = Autocorrelation"

</pre>

#####  OLS Assumption 4: Homoskedasticity (Error is even across observations) 


<pre>

	studentized Breusch-Pagan test

data:  OLS
BP = 51.382, df = 5, p-value = 7.223e-10

[1] "Signficiant = Homoscedastic"

</pre>

#####  OLS Assumption 5: No Colinearity (Predictors are not correlated with each other) 


<pre>

	Goldfeld-Quandt test

data:  OLS
GQ = 0.87219, df1 = 1006, df2 = 1006, p-value = 0.9849
alternative hypothesis: variance increases from segment 1 to 2

[1] "Signficiant = Heteroscedastic"

</pre>

####  Two Part Model (Logistic for non-zero, then Log link) 

#####  Two part model: logistic and poisson 


<pre>
$Firstpart.model

Call:
glm(formula = nonzero ~ NON_WHITE + AGE + SEX + FPL_PERCENT + 
    CONDITIONS, family = binomial(link = "logit"), data = D)

Deviance Residuals: 
    Min       1Q   Median       3Q      Max  
-6.1161   0.0000   0.0232   0.2209   1.5515  

Coefficients:
              Estimate Std. Error z value Pr(>|z|)    
(Intercept) -0.7156364  0.3823376  -1.872  0.06124 .  
NON_WHITE   -0.8730683  0.1638364  -5.329 9.88e-08 ***
AGE          0.0111123  0.0059595   1.865  0.06223 .  
SEX          0.4975721  0.1593653   3.122  0.00179 ** 
FPL_PERCENT  0.0004678  0.0002953   1.584  0.11311    
CONDITIONS   3.5231967  0.3249341  10.843  < 2e-16 ***
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

(Dispersion parameter for binomial family taken to be 1)

    Null deviance: 1743.40  on 2023  degrees of freedom
Residual deviance:  943.08  on 2018  degrees of freedom
AIC: 955.08

Number of Fisher Scoring iterations: 10


$Secondpart.model

Call:
glm(formula = ALWD_TOTAL ~ NON_WHITE + AGE + SEX + FPL_PERCENT + 
    CONDITIONS, family = poisson(link = "log"), data = D)

Deviance Residuals: 
    Min       1Q   Median       3Q      Max  
-414.23   -75.64   -58.87   -23.47  1337.09  

Coefficients:
              Estimate Std. Error z value Pr(>|z|)    
(Intercept)  8.411e+00  1.718e-03  4895.5   <2e-16 ***
NON_WHITE   -1.960e-01  6.741e-04  -290.8   <2e-16 ***
AGE          2.650e-03  2.634e-05   100.6   <2e-16 ***
SEX         -2.419e-01  6.725e-04  -359.7   <2e-16 ***
FPL_PERCENT  9.931e-05  1.008e-06    98.5   <2e-16 ***
CONDITIONS   1.619e-01  6.439e-05  2515.1   <2e-16 ***
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

(Dispersion parameter for poisson family taken to be 1)

    Null deviance: 29150742  on 1710  degrees of freedom
Residual deviance: 23893688  on 1705  degrees of freedom
AIC: 23909218

Number of Fisher Scoring iterations: 7



</pre>

### Machine Learning Result Summary
Various machine learning models were trained on a reference population and then used to predict values from a focus populaiton. The difference in predicted to actual values for the focus group then to reflects the impact of group identification. This is an adaptation of the Kitigawa-Oaxaca-Blinder method.<br>
The following results used the scikit-learn and keras libraries for Python version 3.9.13 (tags/v3.9.13:6de2ca5, May 17 2022, 16:36:42) [MSC v.1929 64 bit (AMD64)]

#### Machine Learning Step 1: Data Processing of Predictors and Outcomes
Source: _data//Race_MEPS//alpha_dev_20221216152657//analytical_Q2.csv

W (ID variables): PERSON_ID<br>
Z (Subgroup variables): YEAR<br>

Reference group: Non-Hispanic White (RACETH == 2)<br>
Focus group: Not Non-Hispanic White (RACETH != 2)<br>


<pre>
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 2024 entries, 0 to 2023
Columns: 365 entries, PERSON_ID to CONDITIONS
dtypes: float64(22), int64(343)
memory usage: 5.6 MB

##### Linear Regression Model for All Groups

      WHITE  ...  CONDITIONS
0  0.434167  ...    0.284923

[1 rows x 5 columns]

</pre>

#### Learn Step 2: Decomposition Paid amount Using Machine Learning Models

##### Random Forests

        AGE       SEX  CONDITIONS  SDOH_FPL
0 -0.010835 -0.770117    0.639617 -0.000826

</pre>
['White Average = 5.5123', 'Non-White Average = 5.1205', 'Non-White Predicted = 5.2745', 'Difference in Bs = 0.3919', 'Difference in Xs = 0.154', 'R-squared + 0.1956']<br>

        Variables  Importances
0        SDOH_FPL     0.582250
4             AGE     0.269482
1  SDOH_EDUCATION     0.053430
5             SEX     0.042507
2    SDOH_MARITAL     0.042317
3       SDOH_FOOD     0.010013

</pre>
['White Average = 5.5123', 'Non-White Average = 5.1205', 'Non-White Predicted = 5.4783', 'Difference in Bs = 0.3919', 'Difference in Xs = 0.3579', 'R-squared + 0.5723']<br>

     Variables  Importances
0          AGE     0.100938
53   ICD10_E78     0.086533
63   ICD10_F32     0.063301
201  ICD10_M19     0.054986
204  ICD10_M25     0.035454
..         ...          ...
254  ICD10_O03     0.000000
258  ICD10_R03     0.000000
282  ICD10_R50     0.000000
286  ICD10_R55     0.000000
203  ICD10_M23     0.000000

[336 rows x 2 columns]

</pre>
['White Average = 5.5123', 'Non-White Average = 5.1205', 'Non-White Predicted = 5.2803', 'Difference in Bs = 0.3919', 'Difference in Xs = 0.1598', 'R-squared + 0.3285']<br>

           Variables  Importances
5      OFFICE_VISITS     0.303003
7          RX_VISITS     0.287500
0                AGE     0.228124
6  OUTPATIENT_VISITS     0.068909
2          ER_VISITS     0.049892
4   INPATIENT_VISITS     0.030930
1                SEX     0.030563
3        HOME_VISITS     0.001079

</pre>
['White Average = 5.5123', 'Non-White Average = 5.1205', 'Non-White Predicted = 4.7862', 'Difference in Bs = 0.3919', 'Difference in Xs = -0.3343', 'R-squared + 0.8053']<br>

##### Gradient Boosting

        Variables  Importances
0        SDOH_FPL     0.688149
4             AGE     0.234533
1  SDOH_EDUCATION     0.025410
2    SDOH_MARITAL     0.021700
5             SEX     0.016075
3       SDOH_FOOD     0.014133

</pre>
['White Average = 5.5123', 'Non-White Average = 5.1205', 'Non-White Predicted = 5.6191', 'Difference in Bs = 0.3919', 'Difference in Xs = 0.4986', 'R-squared + 0.2893']<br>

     Variables  Importances
53   ICD10_E78     0.082688
63   ICD10_F32     0.059815
201  ICD10_M19     0.057758
204  ICD10_M25     0.040978
0          AGE     0.040074
..         ...          ...
170  ICD10_K74     0.000000
171  ICD10_K76     0.000000
172  ICD10_K80     0.000000
174  ICD10_K85     0.000000
188  ICD10_L70     0.000000

[336 rows x 2 columns]

</pre>
['White Average = 5.5123', 'Non-White Average = 5.1205', 'Non-White Predicted = 5.3086', 'Difference in Bs = 0.3919', 'Difference in Xs = 0.1881', 'R-squared + 0.3005']<br>

           Variables  Importances
5      OFFICE_VISITS     0.358868
7          RX_VISITS     0.339052
6  OUTPATIENT_VISITS     0.101971
0                AGE     0.082351
2          ER_VISITS     0.057792
4   INPATIENT_VISITS     0.053922
1                SEX     0.005232
3        HOME_VISITS     0.000812

</pre>
['White Average = 5.5123', 'Non-White Average = 5.1205', 'Non-White Predicted = 4.7483', 'Difference in Bs = 0.3919', 'Difference in Xs = -0.3722', 'R-squared + 0.5905']<br>

##### Ridge Regression (with Cross Validation)

        Variables  Coefficients
3       SDOH_FOOD      0.799767
2    SDOH_MARITAL      0.097803
4             AGE      0.027528
0        SDOH_FPL     -0.001288
1  SDOH_EDUCATION     -0.018546
5             SEX     -0.214214

</pre>
['White Average = 5.5123', 'Non-White Average = 5.1205', 'Non-White Predicted = 5.6224', 'Difference in Bs = 0.3919', 'Difference in Xs = 0.5019', 'R-squared + 0.0201']<br>

     Variables  Coefficients
21   ICD10_C50      2.055176
46   ICD10_E34      1.411262
247  ICD10_N83      1.256830
72   ICD10_F90      1.210083
43   ICD10_E11      1.180790
..         ...           ...
133  ICD10_J09     -0.739588
184  ICD10_L50     -0.850364
273  ICD10_R25     -0.893235
155  ICD10_K25     -1.066067
198  ICD10_M10     -1.119535

[336 rows x 2 columns]

</pre>
['White Average = 5.5123', 'Non-White Average = 5.1205', 'Non-White Predicted = 5.2137', 'Difference in Bs = 0.3919', 'Difference in Xs = 0.0932', 'R-squared + 0.2756']<br>

           Variables  Coefficients
4   INPATIENT_VISITS      1.452032
2          ER_VISITS      0.244232
7          RX_VISITS      0.139614
6  OUTPATIENT_VISITS      0.052833
3        HOME_VISITS      0.039073
5      OFFICE_VISITS      0.007957
0                AGE     -0.000341
1                SEX     -0.324354

</pre>
['White Average = 5.5123', 'Non-White Average = 5.1205', 'Non-White Predicted = 5.1851', 'Difference in Bs = 0.3919', 'Difference in Xs = 0.0647', 'R-squared + 0.226']<br>

##### Least absolute shrinkage and selection operator

        Variables  Coefficients
4             AGE      0.025987
1  SDOH_EDUCATION     -0.000000
2    SDOH_MARITAL      0.000000
3       SDOH_FOOD      0.000000
5             SEX     -0.000000
0        SDOH_FPL     -0.001329

</pre>
['White Average = 5.5123', 'Non-White Average = 5.1205', 'Non-White Predicted = 5.6023', 'Difference in Bs = 0.3919', 'Difference in Xs = 0.4818', 'R-squared + 0.017']<br>

     Variables  Coefficients
21   ICD10_C50      2.055176
46   ICD10_E34      1.411262
247  ICD10_N83      1.256830
72   ICD10_F90      1.210083
43   ICD10_E11      1.180790
..         ...           ...
133  ICD10_J09     -0.739588
184  ICD10_L50     -0.850364
273  ICD10_R25     -0.893235
155  ICD10_K25     -1.066067
198  ICD10_M10     -1.119535

[336 rows x 2 columns]

</pre>
['White Average = 5.5123', 'Non-White Average = 5.1205', 'Non-White Predicted = 5.2137', 'Difference in Bs = 0.3919', 'Difference in Xs = 0.0932', 'R-squared + 0.2756']<br>

           Variables  Coefficients
4   INPATIENT_VISITS      1.452032
2          ER_VISITS      0.244232
7          RX_VISITS      0.139614
6  OUTPATIENT_VISITS      0.052833
3        HOME_VISITS      0.039073
5      OFFICE_VISITS      0.007957
0                AGE     -0.000341
1                SEX     -0.324354

</pre>
['White Average = 5.5123', 'Non-White Average = 5.1205', 'Non-White Predicted = 5.1851', 'Difference in Bs = 0.3919', 'Difference in Xs = 0.0647', 'R-squared + 0.226']<br>

##### Multi-Layer Perceptron

         Loss
0    3.544198
1    3.071435
2    2.832519
3    2.715207
4    2.811593
..        ...
495  0.683220
496  0.696989
497  0.782873
498  0.660523
499  0.686674

[500 rows x 1 columns]

</pre>
['White Average = 5.5123', 'Non-White Average = 5.1205', 'Non-White Predicted = 5.6092', 'Difference in Bs = 0.3919', 'Difference in Xs = 0.4888', 'R-squared + 0.8387']<br>

#### Learn Step 2: Decomposition Using Machine Learning Models

##### Random Forests

        AGE      SEX  CONDITIONS  SDOH_FPL
0  0.006754 -0.05776    0.275156  0.000343

</pre>
['White Average = 7.6875', 'Non-White Average = 7.0618', 'Non-White Predicted = 7.5087', 'Difference in Bs = 0.6257', 'Difference in Xs = 0.4469', 'R-squared + 0.1987']<br>

        Variables  Importances
0        SDOH_FPL     0.567689
4             AGE     0.276226
5             SEX     0.054055
1  SDOH_EDUCATION     0.046670
2    SDOH_MARITAL     0.043207
3       SDOH_FOOD     0.012154

</pre>
['White Average = 7.6875', 'Non-White Average = 7.0618', 'Non-White Predicted = 7.5595', 'Difference in Bs = 0.6257', 'Difference in Xs = 0.4977', 'R-squared + 0.677']<br>

     Variables  Importances
0          AGE     0.208390
133  ICD10_J09     0.078167
214  ICD10_M53     0.054795
66   ICD10_F41     0.050110
43   ICD10_E11     0.035708
..         ...          ...
248  ICD10_N85     0.000000
305  ICD10_S20     0.000000
307  ICD10_S29     0.000000
126  ICD10_I87     0.000000
237  ICD10_N41     0.000000

[336 rows x 2 columns]

</pre>
['White Average = 7.6875', 'Non-White Average = 7.0618', 'Non-White Predicted = 7.493', 'Difference in Bs = 0.6257', 'Difference in Xs = 0.4312', 'R-squared + 0.4664']<br>

           Variables  Importances
5      OFFICE_VISITS     0.354730
7          RX_VISITS     0.228025
0                AGE     0.206176
6  OUTPATIENT_VISITS     0.084191
4   INPATIENT_VISITS     0.054750
2          ER_VISITS     0.042580
1                SEX     0.024182
3        HOME_VISITS     0.005368

</pre>
['White Average = 7.6875', 'Non-White Average = 7.0618', 'Non-White Predicted = 7.3387', 'Difference in Bs = 0.6257', 'Difference in Xs = 0.2769', 'R-squared + 0.7858']<br>

##### Gradient Boosting

        Variables  Importances
0        SDOH_FPL     0.586552
4             AGE     0.326545
2    SDOH_MARITAL     0.030766
1  SDOH_EDUCATION     0.028003
5             SEX     0.023047
3       SDOH_FOOD     0.005087

</pre>
['White Average = 7.6875', 'Non-White Average = 7.0618', 'Non-White Predicted = 7.5365', 'Difference in Bs = 0.6257', 'Difference in Xs = 0.4747', 'R-squared + 0.3261']<br>

     Variables  Importances
0          AGE     0.115948
133  ICD10_J09     0.108863
66   ICD10_F41     0.057747
43   ICD10_E11     0.047580
72   ICD10_F90     0.045197
..         ...          ...
147  ICD10_J98     0.000000
149  ICD10_K02     0.000000
150  ICD10_K04     0.000000
151  ICD10_K05     0.000000
335  ICD10_U07     0.000000

[336 rows x 2 columns]

</pre>
['White Average = 7.6875', 'Non-White Average = 7.0618', 'Non-White Predicted = 7.5137', 'Difference in Bs = 0.6257', 'Difference in Xs = 0.4519', 'R-squared + 0.4038']<br>

           Variables  Importances
5      OFFICE_VISITS     0.405402
7          RX_VISITS     0.246435
0                AGE     0.111153
6  OUTPATIENT_VISITS     0.088422
4   INPATIENT_VISITS     0.075675
2          ER_VISITS     0.061196
3        HOME_VISITS     0.007244
1                SEX     0.004473

</pre>
['White Average = 7.6875', 'Non-White Average = 7.0618', 'Non-White Predicted = 7.3325', 'Difference in Bs = 0.6257', 'Difference in Xs = 0.2707', 'R-squared + 0.5833']<br>

##### Ridge Regression (with Cross Validation)

        Variables  Coefficients
2    SDOH_MARITAL      0.190235
5             SEX      0.168737
3       SDOH_FOOD      0.078411
4             AGE      0.023777
0        SDOH_FPL      0.000144
1  SDOH_EDUCATION     -0.049788

</pre>
['White Average = 7.6875', 'Non-White Average = 7.0618', 'Non-White Predicted = 7.6264', 'Difference in Bs = 0.6257', 'Difference in Xs = 0.5646', 'R-squared + 0.033']<br>

     Variables  Coefficients
21   ICD10_C50      0.756602
43   ICD10_E11      0.743104
72   ICD10_F90      0.740985
247  ICD10_N83      0.722187
284  ICD10_R52      0.662059
..         ...           ...
266  ICD10_R12     -0.320411
36   ICD10_D64     -0.323280
198  ICD10_M10     -0.362099
214  ICD10_M53     -0.511099
133  ICD10_J09     -0.983439

[336 rows x 2 columns]

</pre>
['White Average = 7.6875', 'Non-White Average = 7.0618', 'Non-White Predicted = 7.4976', 'Difference in Bs = 0.6257', 'Difference in Xs = 0.4358', 'R-squared + 0.3079']<br>

           Variables  Coefficients
4   INPATIENT_VISITS      0.720393
2          ER_VISITS      0.107840
1                SEX      0.078017
7          RX_VISITS      0.058982
6  OUTPATIENT_VISITS      0.030091
3        HOME_VISITS      0.020296
0                AGE      0.013602
5      OFFICE_VISITS      0.005487

</pre>
['White Average = 7.6875', 'Non-White Average = 7.0618', 'Non-White Predicted = 7.5205', 'Difference in Bs = 0.6257', 'Difference in Xs = 0.4587', 'R-squared + 0.2789']<br>

##### Least absolute shrinkage and selection operator

        Variables  Coefficients
4             AGE      0.023030
0        SDOH_FPL      0.000075
1  SDOH_EDUCATION     -0.000000
2    SDOH_MARITAL      0.000000
3       SDOH_FOOD      0.000000
5             SEX      0.000000

</pre>
['White Average = 7.6875', 'Non-White Average = 7.0618', 'Non-White Predicted = 7.6408', 'Difference in Bs = 0.6257', 'Difference in Xs = 0.579', 'R-squared + 0.0275']<br>

     Variables  Coefficients
21   ICD10_C50      0.756602
43   ICD10_E11      0.743104
72   ICD10_F90      0.740985
247  ICD10_N83      0.722187
284  ICD10_R52      0.662059
..         ...           ...
266  ICD10_R12     -0.320411
36   ICD10_D64     -0.323280
198  ICD10_M10     -0.362099
214  ICD10_M53     -0.511099
133  ICD10_J09     -0.983439

[336 rows x 2 columns]

</pre>
['White Average = 7.6875', 'Non-White Average = 7.0618', 'Non-White Predicted = 7.4976', 'Difference in Bs = 0.6257', 'Difference in Xs = 0.4358', 'R-squared + 0.3079']<br>

           Variables  Coefficients
4   INPATIENT_VISITS      0.720393
2          ER_VISITS      0.107840
1                SEX      0.078017
7          RX_VISITS      0.058982
6  OUTPATIENT_VISITS      0.030091
3        HOME_VISITS      0.020296
0                AGE      0.013602
5      OFFICE_VISITS      0.005487

</pre>
['White Average = 7.6875', 'Non-White Average = 7.0618', 'Non-White Predicted = 7.5205', 'Difference in Bs = 0.6257', 'Difference in Xs = 0.4587', 'R-squared + 0.2789']<br>

##### Multi-Layer Perceptron

         Loss
0    2.821078
1    1.664096
2    1.711197
3    1.500776
4    1.518384
..        ...
495  0.355434
496  0.356035
497  0.386294
498  0.365152
499  0.417769

[500 rows x 1 columns]

</pre>
['White Average = 7.6875', 'Non-White Average = 7.0618', 'Non-White Predicted = 7.3304', 'Difference in Bs = 0.6257', 'Difference in Xs = 0.2686', 'R-squared + 0.7273']<br>

