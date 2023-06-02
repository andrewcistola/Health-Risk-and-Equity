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
        AGE                                                    
      count       mean        std   min   25%   50%   75%   max
YEAR                                                           
2018  695.0  45.282014  13.662182  19.0  34.0  47.0  58.0  64.0
2019  646.0  46.202786  13.497771  19.0  36.0  49.0  58.0  64.0
2020  683.0  46.838946  13.225779  19.0  36.0  50.0  58.0  64.0
</pre>

<pre>
                  AGE                                                      
                count       mean        std   min    25%   50%    75%   max
YEAR RACE_DESC                                                             
2018 ASIAN       60.0  41.050000  12.675112  19.0  30.75  43.0  50.00  64.0
     BLACK       80.0  45.237500  13.521894  19.0  37.00  47.0  57.00  64.0
     HISPANIC   164.0  43.359756  13.483408  19.0  31.00  44.0  55.00  64.0
     WHITE      391.0  46.746803  13.724574  19.0  36.00  50.0  59.00  64.0
2019 ASIAN       63.0  40.031746  13.353709  20.0  27.50  39.0  51.50  64.0
     BLACK       70.0  47.928571  13.961979  19.0  38.50  53.5  58.00  64.0
     HISPANIC   154.0  44.110390  13.563967  19.0  32.00  46.0  56.75  64.0
     WHITE      359.0  47.846797  13.011015  19.0  38.00  51.0  59.00  64.0
2020 ASIAN       64.0  41.421875  13.080708  19.0  31.50  43.0  52.25  63.0
     BLACK       82.0  48.865854  13.335891  21.0  37.25  53.0  59.00  64.0
     HISPANIC   177.0  45.225989  13.315866  19.0  35.00  48.0  57.00  64.0
     WHITE      360.0  48.133333  12.887514  19.0  38.00  51.5  60.00  64.0
</pre>

<pre>
     PERCENT_FEMALE                                             
              count      mean       std  min  25%  50%  75%  max
YEAR                                                            
2018          695.0  0.592806  0.491665  0.0  0.0  1.0  1.0  1.0
2019          646.0  0.591331  0.491969  0.0  0.0  1.0  1.0  1.0
2020          683.0  0.578331  0.494188  0.0  0.0  1.0  1.0  1.0
</pre>

<pre>
               PERCENT_FEMALE                                             
                        count      mean       std  min  25%  50%  75%  max
YEAR RACE_DESC                                                            
2018 ASIAN               60.0  0.616667  0.490301  0.0  0.0  1.0  1.0  1.0
     BLACK               80.0  0.587500  0.495390  0.0  0.0  1.0  1.0  1.0
     HISPANIC           164.0  0.591463  0.493069  0.0  0.0  1.0  1.0  1.0
     WHITE              391.0  0.590793  0.492318  0.0  0.0  1.0  1.0  1.0
2019 ASIAN               63.0  0.555556  0.500895  0.0  0.0  1.0  1.0  1.0
     BLACK               70.0  0.685714  0.467583  0.0  0.0  1.0  1.0  1.0
     HISPANIC           154.0  0.571429  0.496486  0.0  0.0  1.0  1.0  1.0
     WHITE              359.0  0.587744  0.492928  0.0  0.0  1.0  1.0  1.0
2020 ASIAN               64.0  0.578125  0.497763  0.0  0.0  1.0  1.0  1.0
     BLACK               82.0  0.670732  0.472840  0.0  0.0  1.0  1.0  1.0
     HISPANIC           177.0  0.610169  0.489095  0.0  0.0  1.0  1.0  1.0
     WHITE              360.0  0.541667  0.498954  0.0  0.0  1.0  1.0  1.0
</pre>

<pre>
     FPL_PERCENT                                                                 
           count        mean         std    min     25%     50%      75%      max
YEAR                                                                             
2018       695.0  349.779813  309.562007 -46.96  172.58  260.03  422.475  2411.90
2019       646.0  345.253839  308.471502   0.00  149.28  263.16  433.720  2727.94
2020       683.0  348.440600  295.034237 -58.32  156.21  279.26  438.170  2100.47
</pre>

<pre>
               FPL_PERCENT                                                                     
                     count        mean         std    min       25%      50%       75%      max
YEAR RACE_DESC                                                                                 
2018 ASIAN            60.0  384.298333  369.612659  39.91  158.9000  264.050  444.6175  2215.54
     BLACK            80.0  287.427875  235.614083   0.00  120.3100  233.560  344.6175  1011.36
     HISPANIC        164.0  289.530610  223.243713  59.47  152.3600  232.935  337.4975  1753.15
     WHITE           391.0  382.511049  337.938688 -46.96  184.8700  290.770  493.5300  2411.90
2019 ASIAN            63.0  396.950794  416.497255   0.00  138.0500  237.210  527.4100  2239.65
     BLACK            70.0  272.013000  209.789125   0.00  110.7325  244.470  343.4950   965.99
     HISPANIC        154.0  245.754286  157.578763   0.00  130.1475  189.610  335.3100   852.80
     WHITE           359.0  393.144875  337.968795   0.00  188.6900  302.250  489.1800  2727.94
2020 ASIAN            64.0  382.180313  274.466177   0.00  192.2725  303.370  454.3175  1269.53
     BLACK            82.0  256.267561  225.206381 -58.32  116.8275  185.670  298.4500   997.19
     HISPANIC        177.0  262.795537  205.400576 -20.52  126.9400  192.950  349.0500  1186.10
     WHITE           360.0  405.546222  333.144225 -10.19  193.4875  308.600  518.2000  2100.47
</pre>

<pre>
     ICD10_TOTAL                                              
           count      mean       std  min  25%  50%  75%   max
YEAR                                                          
2018       695.0  2.427338  2.941328  0.0  0.0  1.0  4.0  21.0
2019       646.0  2.272446  2.886496  0.0  0.0  1.0  3.0  25.0
2020       683.0  2.156662  2.564773  0.0  0.0  1.0  3.0  19.0
</pre>

<pre>
               ICD10_TOTAL                                               
                     count      mean       std  min   25%  50%  75%   max
YEAR RACE_DESC                                                           
2018 ASIAN            60.0  1.283333  1.992287  0.0  0.00  1.0  2.0  11.0
     BLACK            80.0  2.150000  2.551247  0.0  0.00  1.0  3.0  14.0
     HISPANIC        164.0  1.774390  2.586720  0.0  0.00  1.0  3.0  14.0
     WHITE           391.0  2.933504  3.166439  0.0  0.00  2.0  4.0  21.0
2019 ASIAN            63.0  1.396825  1.930566  0.0  0.00  1.0  2.0   7.0
     BLACK            70.0  2.614286  2.788656  0.0  0.25  2.0  4.0  11.0
     HISPANIC        154.0  1.707792  2.943754  0.0  0.00  1.0  2.0  23.0
     WHITE           359.0  2.601671  2.959710  0.0  0.00  2.0  4.0  25.0
2020 ASIAN            64.0  1.265625  1.692581  0.0  0.00  1.0  2.0   7.0
     BLACK            82.0  2.756098  2.835232  0.0  0.00  2.0  4.0  13.0
     HISPANIC        177.0  1.593220  2.304531  0.0  0.00  1.0  2.0  17.0
     WHITE           360.0  2.455556  2.665831  0.0  1.00  2.0  4.0  19.0
</pre>

<pre>
     PAID_TOTAL                                                                   
          count         mean           std  min  25%     50%        75%        max
YEAR                                                                              
2018      695.0  4293.347885  23362.324376  0.0  0.0  135.38  1460.5000  358442.35
2019      646.0  5313.464690  36371.287006  0.0  0.0  149.07  1421.1425  788295.78
2020      683.0  3474.370410  13474.055004  0.0  0.0  142.06  1275.0100  160834.52
</pre>

<pre>
               PAID_TOTAL                                                                    
                    count         mean           std  min  25%      50%        75%        max
YEAR RACE_DESC                                                                               
2018 ASIAN           60.0   917.819667   3349.415095  0.0  0.0    0.605   634.8025   25184.46
     BLACK           80.0  2432.827375   9381.390895  0.0  0.0   76.970   698.6050   66465.95
     HISPANIC       164.0   964.444146   3328.660441  0.0  0.0   28.565   679.7225   37806.36
     WHITE          391.0  6588.267442  30572.568968  0.0  0.0  451.970  2436.3650  358442.35
2019 ASIAN           63.0  4302.419048  15747.895275  0.0  0.0    5.520   552.4650   93721.43
     BLACK           70.0  6945.746000  36111.193402  0.0  0.0  232.535  1295.7175  289529.17
     HISPANIC       154.0  7257.567922  63697.772758  0.0  0.0    9.170   461.4600  788295.78
     WHITE          359.0  4338.657688  18756.094680  0.0  0.0  265.050  1745.3650  219733.64
2020 ASIAN           64.0  1218.738438   4044.451913  0.0  0.0    4.280   371.2975   27336.65
     BLACK           82.0  3173.430488   9102.738584  0.0  0.0   89.425  1565.6775   51341.60
     HISPANIC       177.0  2400.789774  10997.321557  0.0  0.0   19.590   607.8500  128095.73
     WHITE          360.0  4471.762889  16172.315515  0.0  0.0  259.570  1864.9825  160834.52
</pre>

<pre>
     VISITS_TOTAL                                                   
            count       mean        std  min  25%  50%   75%     max
YEAR                                                                
2018        695.0  15.115108  55.637111  0.0  0.0  5.0  16.0  1322.0
2019        646.0  12.804954  27.626171  0.0  0.0  4.0  13.0   388.0
2020        683.0  11.626647  22.841151  0.0  0.0  4.0  14.0   255.0
</pre>

<pre>
               VISITS_TOTAL                                                    
                      count       mean        std  min  25%  50%    75%     max
YEAR RACE_DESC                                                                 
2018 ASIAN             60.0   7.000000  19.349594  0.0  0.0  1.0   5.25   127.0
     BLACK             80.0   9.337500  15.116379  0.0  0.0  3.0  10.25    80.0
     HISPANIC         164.0   8.615854  18.855407  0.0  0.0  2.0   9.00   174.0
     WHITE            391.0  20.268542  72.079778  0.0  1.0  7.0  22.50  1322.0
2019 ASIAN             63.0   8.777778  20.582991  0.0  0.0  2.0   6.50   130.0
     BLACK             70.0  13.557143  19.711422  0.0  2.0  6.0  14.00    85.0
     HISPANIC         154.0   7.344156  13.825892  0.0  0.0  1.5   6.00    87.0
     WHITE            359.0  15.707521  33.479181  0.0  1.0  6.0  16.50   388.0
2020 ASIAN             64.0   5.015625   7.096818  0.0  0.0  2.0   7.25    29.0
     BLACK             82.0  14.426829  24.913693  0.0  0.0  4.0  20.00   164.0
     HISPANIC         177.0   6.689266  11.111498  0.0  0.0  1.0   9.00    73.0
     WHITE            360.0  14.591667  27.409663  0.0  1.0  6.0  16.00   255.0
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
X (Predictor variables):  NON_WHITE AGE SEX FPL_PERCENT ICD10_TOTAL <br>
Y (Outcome variables):  PAID_TOTAL <br>
Z (Subgroup variables):  YEAR <br>


<pre>
── Data Summary ────────────────────────
                           Values 
Name                       df_WXYZ
Number of rows             2024   
Number of columns          20     
_______________________           
Column type frequency:            
  numeric                  20     
________________________          
Group variables            None   

── Variable type: numeric ──────────────────────────────────────────────────────
   skim_variable n_missing complete_rate    mean           sd       p0      p25
 1 PERSON_ID             0             1 2.38e+9 90986093.     2.29e+9  2.32e+9
 2 YEAR                  0             1 2.02e+3        0.825  2.02e+3  2.02e+3
 3 AGE                   0             1 4.61e+1       13.5    1.9 e+1  3.5 e+1
 4 SEX                   0             1 1.59e+0        0.492  1   e+0  1   e+0
 5 RACE                  0             1 2.05e+0        0.852  1   e+0  2   e+0
 6 FPL_PERCENT           0             1 3.48e+2      304.    -5.83e+1  1.58e+2
 7 ICD10_TOTAL           0             1 2.29e+0        2.80   0        0      
 8 PAID_TOTAL            0             1 4.34e+3    25899.     0        0      
 9 VISITS_TOTAL          0             1 1.32e+1       38.5    0        0      
10 HISPANIC              0             1 2.45e-1        0.430  0        0      
11 WHITE                 0             1 5.48e-1        0.498  0        0      
12 BLACK                 0             1 1.15e-1        0.319  0        0      
13 ASIAN                 0             1 9.24e-2        0.290  0        0      
14 OTHER                 0             1 0              0      0        0      
15 NON_WHITE             0             1 4.52e-1        0.498  0        0      
16 Y_raw                 0             1 4.34e+3    25899.     0        0      
17 Y_binary              0             1 6.31e-1        0.483  0        0      
18 PAID_ZERO             0             1 4.34e+3    25899.     1   e-3  1   e-3
19 Y_log                 0             1 1.63e+0        6.77  -6.91e+0 -6.91e+0
20 Y_scale               0             1 1   e+0        5.96   2.30e-7  2.30e-7
       p50     p75         p100 hist 
 1 2.33e+9 2.46e+9 2579815101   ▇▁▂▂▁
 2 2.02e+3 2.02e+3       2020   ▇▁▇▁▇
 3 4.9 e+1 5.8 e+1         64   ▃▃▅▅▇
 4 2   e+0 2   e+0          2   ▆▁▁▁▇
 5 2   e+0 2   e+0          4   ▃▇▁▂▂
 6 2.65e+2 4.32e+2       2728.  ▇▂▁▁▁
 7 1   e+0 3   e+0         25   ▇▁▁▁▁
 8 1.44e+2 1.39e+3     788296.  ▇▁▁▁▁
 9 4   e+0 1.4 e+1       1322   ▇▁▁▁▁
10 0       0                1   ▇▁▁▁▂
11 1   e+0 1   e+0          1   ▆▁▁▁▇
12 0       0                1   ▇▁▁▁▁
13 0       0                1   ▇▁▁▁▁
14 0       0                0   ▁▁▇▁▁
15 0       1   e+0          1   ▇▁▁▁▆
16 1.44e+2 1.39e+3     788296.  ▇▁▁▁▁
17 1   e+0 1   e+0          1   ▅▁▁▁▇
18 1.44e+2 1.39e+3     788296.  ▇▁▁▁▁
19 4.97e+0 7.24e+0         13.6 ▇▁▃▇▁
20 3.32e-2 3.19e-1        182.  ▇▁▁▁▁

</pre>

####  Final Model: OLS on Log costs, RACE = Missing excluded, 2018-2020 

#####  OLS Assumption 0: Sampling (Random sample, observations > predictors, predictor is independent) 


<pre>

Call:
lm(formula = F, data = D)

Residuals:
   Min     1Q Median     3Q    Max 
-31464  -4457  -1240    258 775074 

Coefficients:
              Estimate Std. Error t value Pr(>|t|)    
(Intercept)  4007.4195  2864.4113   1.399    0.162    
NON_WHITE    -108.1579  1164.8132  -0.093    0.926    
AGE           -27.7648    43.8230  -0.634    0.526    
SEX         -1919.0515  1167.1328  -1.644    0.100    
FPL_PERCENT    -0.3671     1.8866  -0.195    0.846    
ICD10_TOTAL  2115.8783   216.1325   9.790   <2e-16 ***
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Residual standard error: 25290 on 2018 degrees of freedom
Multiple R-squared:  0.04915,	Adjusted R-squared:  0.04679 
F-statistic: 20.86 on 5 and 2018 DF,  p-value: < 2.2e-16


</pre>

#####  OLS Assumption 1: Specification (Relationship between predictor and outcome is linear) 

<pre>

	Rainbow test

data:  OLS
Rain = 0.23298, df1 = 1012, df2 = 1006, p-value = 1

[1] "Significant = Non-linearity"

</pre>
#####  OLS Assumption 2:  Normality (Errors are normal with a mean = 0) 


<pre>

	Robust Jarque Bera Test

data:  resid(OLS)
X-squared = 1.8887e+11, df = 2, p-value < 2.2e-16

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
DW = 2.0064, p-value = 0.5527
alternative hypothesis: true autocorrelation is greater than 0

[1] "Signficiant = Autocorrelation"

</pre>

#####  OLS Assumption 4: Homoskedasticity (Error is even across observations) 


<pre>

	studentized Breusch-Pagan test

data:  OLS
BP = 10.616, df = 5, p-value = 0.05955

[1] "Signficiant = Homoscedastic"

</pre>

#####  OLS Assumption 5: No Colinearity (Predictors are not correlated with each other) 


<pre>

	Goldfeld-Quandt test

data:  OLS
GQ = 1.3805, df1 = 1006, df2 = 1006, p-value = 1.689e-07
alternative hypothesis: variance increases from segment 1 to 2

[1] "Signficiant = Heteroscedastic"

</pre>

####  Final Model 3: Two Step Model on Costs, RACE = Missing excluded, 2018-2020 

#####  Logistic Regression on Presence Non-Zero Costs 


<pre>

Call:
glm(formula = F1, family = binomial(link = "logit"), data = D1)

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
ICD10_TOTAL  1.9882384  0.0983395  20.218  < 2e-16 ***
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

(Dispersion parameter for binomial family taken to be 1)

    Null deviance: 2665.4  on 2023  degrees of freedom
Residual deviance: 1320.5  on 2018  degrees of freedom
AIC: 1332.5

Number of Fisher Scoring iterations: 7


</pre>
#####  Poisson Regression on Costs 


<pre>

Call:
glm(formula = F2, family = poisson(link = "log"), data = D2)

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
ICD10_TOTAL  1.677e-01  6.957e-05 2410.62   <2e-16 ***
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

(Dispersion parameter for poisson family taken to be 1)

    Null deviance: 34770303  on 1276  degrees of freedom
Residual deviance: 30270956  on 1271  degrees of freedom
AIC: Inf

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
Columns: 360 entries, PERSON_ID to CONDITIONS
dtypes: float64(18), int64(342)
memory usage: 5.6 MB

##### Linear Regression Model for All Groups

      WHITE       AGE      SEX  SDOH_FPL  CONDITIONS
0  0.133997 -0.019806 -0.38675  -0.00066    0.685599

</pre>

##### Random Forests

        AGE       SEX  CONDITIONS  SDOH_FPL
0 -0.012433 -0.880068    0.706917 -0.000985

</pre>
['White Average = 5.2456', 'Non-White Average = 4.8691', 'Non-White Predicted = 4.9894', 'Difference in Bs = 0.3765', 'Difference in Xs = 0.1203', 'R-squared + 0.1797']<br>

        Variables  Importances
0        SDOH_FPL     0.588699
4             AGE     0.262844
1  SDOH_EDUCATION     0.054171
5             SEX     0.042976
2    SDOH_MARITAL     0.042340
3       SDOH_FOOD     0.008970

</pre>
['White Average = 5.2456', 'Non-White Average = 4.8691', 'Non-White Predicted = 5.1833', 'Difference in Bs = 0.3765', 'Difference in Xs = 0.3141', 'R-squared + 0.5804']<br>

     Variables  Importances
0          AGE     0.109147
53   ICD10_E78     0.087434
63   ICD10_F32     0.064927
201  ICD10_M19     0.051256
204  ICD10_M25     0.028794
..         ...          ...
289  ICD10_R59     0.000000
87   ICD10_H00     0.000000
3    ICD10_A08     0.000000
305  ICD10_S20     0.000000
64   ICD10_F34     0.000000

[336 rows x 2 columns]

</pre>
['White Average = 5.2456', 'Non-White Average = 4.8691', 'Non-White Predicted = 5.0022', 'Difference in Bs = 0.3765', 'Difference in Xs = 0.1331', 'R-squared + 0.3123']<br>

           Variables  Importances
5      OFFICE_VISITS     0.290227
7          RX_VISITS     0.285222
0                AGE     0.254853
6  OUTPATIENT_VISITS     0.065398
2          ER_VISITS     0.044516
1                SEX     0.034032
4   INPATIENT_VISITS     0.025019
3        HOME_VISITS     0.000735

</pre>
['White Average = 5.2456', 'Non-White Average = 4.8691', 'Non-White Predicted = 4.4452', 'Difference in Bs = 0.3765', 'Difference in Xs = -0.424', 'R-squared + 0.7942']<br>

##### Gradient Boosting

        Variables  Importances
0        SDOH_FPL     0.678027
4             AGE     0.259393
1  SDOH_EDUCATION     0.025059
2    SDOH_MARITAL     0.013311
5             SEX     0.013112
3       SDOH_FOOD     0.011098

</pre>
['White Average = 5.2456', 'Non-White Average = 4.8691', 'Non-White Predicted = 5.3885', 'Difference in Bs = 0.3765', 'Difference in Xs = 0.5194', 'R-squared + 0.288']<br>

     Variables  Importances
53   ICD10_E78     0.079916
63   ICD10_F32     0.064130
201  ICD10_M19     0.054123
0          AGE     0.046032
204  ICD10_M25     0.038160
..         ...          ...
183  ICD10_L40     0.000000
22   ICD10_C55     0.000000
185  ICD10_L57     0.000000
20   ICD10_C44     0.000000
193  ICD10_L84     0.000000

[336 rows x 2 columns]

</pre>
['White Average = 5.2456', 'Non-White Average = 4.8691', 'Non-White Predicted = 5.0407', 'Difference in Bs = 0.3765', 'Difference in Xs = 0.1715', 'R-squared + 0.2919']<br>

           Variables  Importances
7          RX_VISITS     0.352573
5      OFFICE_VISITS     0.349782
6  OUTPATIENT_VISITS     0.097721
0                AGE     0.092738
2          ER_VISITS     0.054606
4   INPATIENT_VISITS     0.047750
1                SEX     0.004492
3        HOME_VISITS     0.000338

</pre>
['White Average = 5.2456', 'Non-White Average = 4.8691', 'Non-White Predicted = 4.405', 'Difference in Bs = 0.3765', 'Difference in Xs = -0.4642', 'R-squared + 0.5605']<br>

##### Ridge Regression (with Cross Validation)

        Variables  Coefficients
3       SDOH_FOOD      0.949891
4             AGE      0.029710
2    SDOH_MARITAL      0.014189
0        SDOH_FPL     -0.001513
1  SDOH_EDUCATION     -0.027184
5             SEX     -0.263785

</pre>
['White Average = 5.2456', 'Non-White Average = 4.8691', 'Non-White Predicted = 5.3842', 'Difference in Bs = 0.3765', 'Difference in Xs = 0.5151', 'R-squared + 0.0193']<br>

     Variables  Coefficients
21   ICD10_C50      2.259465
46   ICD10_E34      1.605923
247  ICD10_N83      1.348392
72   ICD10_F90      1.313167
224  ICD10_M79      1.305102
..         ...           ...
29   ICD10_D04     -0.887163
184  ICD10_L50     -0.925361
273  ICD10_R25     -1.065043
155  ICD10_K25     -1.189970
198  ICD10_M10     -1.305746

[336 rows x 2 columns]

</pre>
['White Average = 5.2456', 'Non-White Average = 4.8691', 'Non-White Predicted = 4.9276', 'Difference in Bs = 0.3765', 'Difference in Xs = 0.0585', 'R-squared + 0.2558']<br>

           Variables  Coefficients
4   INPATIENT_VISITS      1.537182
2          ER_VISITS      0.254903
7          RX_VISITS      0.154254
6  OUTPATIENT_VISITS      0.055136
3        HOME_VISITS      0.030546
5      OFFICE_VISITS      0.008236
0                AGE     -0.001154
1                SEX     -0.383812

</pre>
['White Average = 5.2456', 'Non-White Average = 4.8691', 'Non-White Predicted = 4.8877', 'Difference in Bs = 0.3765', 'Difference in Xs = 0.0186', 'R-squared + 0.1989']<br>

##### Least absolute shrinkage and selection operator

        Variables  Coefficients
4             AGE      0.028165
1  SDOH_EDUCATION     -0.000000
2    SDOH_MARITAL      0.000000
3       SDOH_FOOD      0.000000
5             SEX     -0.000000
0        SDOH_FPL     -0.001536

</pre>
['White Average = 5.2456', 'Non-White Average = 4.8691', 'Non-White Predicted = 5.3527', 'Difference in Bs = 0.3765', 'Difference in Xs = 0.4836', 'R-squared + 0.0163']<br>

     Variables  Coefficients
21   ICD10_C50      2.259465
46   ICD10_E34      1.605923
247  ICD10_N83      1.348392
72   ICD10_F90      1.313167
224  ICD10_M79      1.305102
..         ...           ...
29   ICD10_D04     -0.887163
184  ICD10_L50     -0.925361
273  ICD10_R25     -1.065043
155  ICD10_K25     -1.189970
198  ICD10_M10     -1.305746

[336 rows x 2 columns]

</pre>
['White Average = 5.2456', 'Non-White Average = 4.8691', 'Non-White Predicted = 4.9276', 'Difference in Bs = 0.3765', 'Difference in Xs = 0.0585', 'R-squared + 0.2558']<br>

           Variables  Coefficients
4   INPATIENT_VISITS      1.537182
2          ER_VISITS      0.254903
7          RX_VISITS      0.154254
6  OUTPATIENT_VISITS      0.055136
3        HOME_VISITS      0.030546
5      OFFICE_VISITS      0.008236
0                AGE     -0.001154
1                SEX     -0.383812

</pre>
['White Average = 5.2456', 'Non-White Average = 4.8691', 'Non-White Predicted = 4.8877', 'Difference in Bs = 0.3765', 'Difference in Xs = 0.0186', 'R-squared + 0.1989']<br>

##### Multi-Layer Perceptron

         Loss
0    3.733195
1    3.486001
2    3.373617
3    3.288321
4    3.007737
..        ...
495  0.855514
496  0.843388
497  0.839365
498  0.866079
499  0.867566

[500 rows x 1 columns]

</pre>
['White Average = 5.2456', 'Non-White Average = 4.8691', 'Non-White Predicted = 4.5124', 'Difference in Bs = 0.3765', 'Difference in Xs = -0.3567', 'R-squared + 0.8424']<br>

