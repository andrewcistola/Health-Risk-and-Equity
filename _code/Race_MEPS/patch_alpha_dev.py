# Patch

## Query All social determinants from household file
QUERY = """
    SELECT
        2020 AS YEAR
        , W.DUPERSID AS PERSON_ID
        , W.POVLEV20 AS POVLEV
        , W.MARRY20X AS MARRY
        , W.HIDEG
        , W.FOODST20 AS FOODST
    FROM h224 W
    WHERE
        W.AGELAST > 18
        AND W.AGELAST < 65
        AND W.RACETHX IN (1, 2, 3, 4)
        AND W.PRSTX20 = 1
        AND W.INSCOV20 = 1
    UNION
    SELECT
        2019 AS YEAR
        , W.DUPERSID AS PERSON_ID
        , W.POVLEV19 AS POVLEV
        , W.MARRY19X AS MARRY
        , W.HIDEG
        , W.FOODST19 AS FOODST
    FROM h216 W
    WHERE
        W.AGELAST > 18
        AND W.AGELAST < 65
        AND W.RACETHX IN (1, 2, 3, 4)
        AND W.PRSTX19 = 1
        AND W.INSCOV19 = 1
    UNION
    SELECT
        2018 AS YEAR
        , W.DUPERSID AS PERSON_ID
        , W.POVLEV18 AS POVLEV
        , W.MARRY18X AS MARRY
        , W.HIDEG 
        , W.FOODST18 AS FOODST
    FROM h209 W
    WHERE
        W.AGELAST > 18
        AND W.AGELAST < 65
        AND W.RACETHX IN (1, 2, 3, 4)
        AND W.PRSTX18 = 1
        AND W.INSCOV18 = 1
    """
df_V = pd.read_sql_query(QUERY, db_con)
df_V['PERSON_ID'] = df_V['PERSON_ID'].astype('int64')
df_V['SDOH_FPL'] = df_V['POVLEV']
df_V['SDOH_EDUCATION'] = np.where(df_V['HIDEG'] <= 3.0, 1, 0) # Create column based on conditions
df_V['SDOH_MARITAL'] = np.where(df_V['MARRY'] > 1, 1, 0) # Create column based nested conditions
df_V['SDOH_FOOD'] = np.where(df_V['FOODST'] == 1, 1, 0) # Create column based nested conditions
df_V = df_V.filter(['PERSON_ID', 'YEAR', 'SDOH_FPL', 'SDOH_EDUCATION', 'SDOH_MARITAL', 'SDOH_FOOD']) # Keep selected columns
df_WXYZ = pd.read_csv('_data//' + label_name + '//' + label_run + '//analytical_Q2.csv')
df_WXYZ = df_WXYZ.loc[:, ~df_WXYZ.columns.str.contains('SDOH')]
df_VWXYZ = pd.merge(df_V, df_WXYZ, on = ['PERSON_ID', 'YEAR'], how = 'inner') # Inner join
df_VWXYZ.info()
df_VWXYZ.columns
df_VWXYZ['CONDITIONS'] = df_VWXYZ['ICD10_TOTAL']
df_VWXYZ.to_csv('_data//' + label_name + '//' + label_run + '//analytical_Q2.csv', index = False)
