# Clean

### Query all individuals with marketplace coverage for full year in age range
label_query = 'households'
QUERY = """
    SELECT
        2020 AS YEAR
        , W.DUPERSID AS PERSON_ID
        , W.AGELAST AS AGE
        , W.SEX
        , W.RACETHX AS RACE
        , W.POVCAT20 AS FPL_GROUP
        , W.POVLEV20 AS FPL_PERCENT
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
        , W.AGELAST AS AGE
        , W.SEX
        , W.RACETHX AS RACE
        , W.POVCAT19 AS FPL_GROUP
        , W.POVLEV19 AS FPL_PERCENT
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
        , W.AGELAST AS AGE
        , W.SEX
        , W.RACETHX AS RACE
        , W.POVCAT18 AS FPL_GROUP
        , W.POVLEV18 AS FPL_PERCENT
    FROM h209 W
    WHERE
        W.AGELAST > 18
        AND W.AGELAST < 65
        AND W.RACETHX IN (1, 2, 3, 4)
        AND W.PRSTX18 = 1
        AND W.INSCOV18 = 1
    """
df_W = pd.read_sql_query(QUERY, db_con)
df_W
df_W.to_csv('_data//' + label_name + '//' + label_run + '//' + label_query + '.csv', index = False)

### Query all events that match ID for given year from each setting
label_query = 'conditions'
QUERY = """
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , X.ICD10CDX AS ICD10
        , CONDIDX AS CONDITION_ID
    FROM (
        SELECT DISTINCT DUPERSID 
        FROM h224
        WHERE
            AGELAST > 18
            AND AGELAST < 65
            AND RACETHX IN (1, 2, 3, 4)
            AND PRSTX20 = 1
            AND INSCOV20 = 1
        ) SQ
    LEFT JOIN h222 X
        ON SQ.DUPERSID = X.DUPERSID
    UNION
    SELECT
        2019 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , X.ICD10CDX AS ICD10
        , CONDIDX AS CONDITION_ID
    FROM (
        SELECT DISTINCT DUPERSID 
        FROM h216
        WHERE
            AGELAST > 18
            AND AGELAST < 65
            AND RACETHX IN (1, 2, 3, 4)
            AND PRSTX19 = 1
            AND INSCOV19 = 1
        ) SQ
    LEFT JOIN h214 X
        ON SQ.DUPERSID = X.DUPERSID
    UNION
    SELECT
        2018 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , X.ICD10CDX AS ICD10
        , CONDIDX AS CONDITION_ID
    FROM (
        SELECT DISTINCT DUPERSID 
        FROM h209
        WHERE
            AGELAST > 18
            AND AGELAST < 65
            AND RACETHX IN (1, 2, 3, 4)
            AND PRSTX18 = 1
            AND INSCOV18 = 1
        ) SQ
    LEFT JOIN h207 X
        ON SQ.DUPERSID = X.DUPERSID
    """
df_X = pd.read_sql_query(QUERY, db_con)
df_X
df_X.to_csv('_data//' + label_name + '//' + label_run + '//' + label_query + '.csv', index = False)

### Query all events that match ID for given year from each setting
label_query = 'events'
QUERY = """
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'RX' AS SETTING
        , A.LINKIDX AS EVENT_ID
        , A.RXPV20X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX20 = 1
            AND Y.INSCOV20 = 1
        ) SQ
    LEFT JOIN h220a A
        ON SQ.DUPERSID = A.DUPERSID
    UNION
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'DENTAL' AS SETTING
        , B.EVNTIDX AS EVENT_ID
        , B.DVPV20X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX20 = 1
            AND Y.INSCOV20 = 1
        ) SQ
    LEFT JOIN h220b B
        ON SQ.DUPERSID = B.DUPERSID
    UNION
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'OTHER' AS SETTING
        , C.EVNTIDX AS EVENT_ID
        , C.OMPV20X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX20 = 1
            AND Y.INSCOV20 = 1
        ) SQ
    LEFT JOIN h220c C
        ON SQ.DUPERSID = C.DUPERSID
    UNION
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'INPATIENT' AS SETTING
        , D.EVNTIDX AS EVENT_ID
        , D.IPFPV20X + D.IPDPV20X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX20 = 1
            AND Y.INSCOV20 = 1
        ) SQ
    LEFT JOIN h220d D
        ON SQ.DUPERSID = D.DUPERSID
    UNION
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'ER' AS SETTING
        , E.EVNTIDX AS EVENT_ID
        , E.ERFPV20X + E.ERDPV20X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX20 = 1
            AND Y.INSCOV20 = 1
        ) SQ
    LEFT JOIN h220e E
        ON SQ.DUPERSID = E.DUPERSID
    UNION
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'OUTPATIENT' AS SETTING
        , F.EVNTIDX AS EVENT_ID
        , F.OPFPV20X + F.OPDPV20X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX20 = 1
            AND Y.INSCOV20 = 1
        ) SQ
    LEFT JOIN h220f F
        ON SQ.DUPERSID = F.DUPERSID
    UNION
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'OFFICE' AS SETTING
        , G.EVNTIDX AS EVENT_ID
        , G.OBPV20X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX20 = 1
            AND Y.INSCOV20 = 1
        ) SQ
    LEFT JOIN h220g G
        ON SQ.DUPERSID = G.DUPERSID
    UNION
        SELECT
        2020 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'HOME' AS SETTING
        , H.EVNTIDX AS EVENT_ID
        , H.HHPV20X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX20 = 1
            AND Y.INSCOV20 = 1
        ) SQ
    LEFT JOIN h220h H
        ON SQ.DUPERSID = H.DUPERSID
      
    UNION
    SELECT
        2019 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'RX' AS SETTING
        , A.LINKIDX AS EVENT_ID
        , A.RXPV19X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h216 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX19 = 1
            AND Y.INSCOV19 = 1
        ) SQ
    LEFT JOIN h213a A
        ON SQ.DUPERSID = A.DUPERSID
    UNION
    SELECT
        2019 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'DENTAL' AS SETTING
        , B.EVNTIDX AS EVENT_ID
        , B.DVPV19X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h216 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX19 = 1
            AND Y.INSCOV19 = 1
        ) SQ
    LEFT JOIN h213b B
        ON SQ.DUPERSID = B.DUPERSID
    UNION
    SELECT
        2019 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'OTHER' AS SETTING
        , C.EVNTIDX AS EVENT_ID
        , C.OMPV19X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h216 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX19 = 1
            AND Y.INSCOV19 = 1
        ) SQ
    LEFT JOIN h213c C
        ON SQ.DUPERSID = C.DUPERSID
    UNION
    SELECT
        2019 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'INPATIENT' AS SETTING
        , D.EVNTIDX AS EVENT_ID
        , D.IPFPV19X + D.IPDPV19X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h216 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX19 = 1
            AND Y.INSCOV19 = 1
        ) SQ
    LEFT JOIN h213d D
        ON SQ.DUPERSID = D.DUPERSID
    UNION
    SELECT
        2019 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'ER' AS SETTING
        , E.EVNTIDX AS EVENT_ID
        , E.ERFPV19X + E.ERDPV19X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h216 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX19 = 1
            AND Y.INSCOV19 = 1
        ) SQ
    LEFT JOIN h213e E
        ON SQ.DUPERSID = E.DUPERSID
    UNION
    SELECT
        2019 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'OUTPATIENT' AS SETTING
        , F.EVNTIDX AS EVENT_ID
        , F.OPFPV19X + F.OPDPV19X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h216 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX19 = 1
            AND Y.INSCOV19 = 1
        ) SQ
    LEFT JOIN h213f F
        ON SQ.DUPERSID = F.DUPERSID
    UNION
    SELECT
        2019 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'OFFICE' AS SETTING
        , G.EVNTIDX AS EVENT_ID
        , G.OBPV19X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h216 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX19 = 1
            AND Y.INSCOV19 = 1
        ) SQ
    LEFT JOIN h213g G
        ON SQ.DUPERSID = G.DUPERSID
    UNION
        SELECT
        2019 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'HOME' AS SETTING
        , H.EVNTIDX AS EVENT_ID
        , H.HHPV19X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h216 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX19 = 1
            AND Y.INSCOV19 = 1
        ) SQ
    LEFT JOIN h213h H
        ON SQ.DUPERSID = H.DUPERSID

    UNION
    SELECT
        2018 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'RX' AS SETTING
        , A.LINKIDX AS EVENT_ID
        , A.RXPV18X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX18 = 1
            AND Y.INSCOV18 = 1
        ) SQ
    LEFT JOIN h206a A
        ON SQ.DUPERSID = A.DUPERSID
    UNION
    SELECT
        2018 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'DENTAL' AS SETTING
        , B.EVNTIDX AS EVENT_ID
        , B.DVPV18X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX18 = 1
            AND Y.INSCOV18 = 1
        ) SQ
    LEFT JOIN h206b B
        ON SQ.DUPERSID = B.DUPERSID
    UNION
    SELECT
        2018 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'OTHER' AS SETTING
        , C.EVNTIDX AS EVENT_ID
        , C.OMPV18X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX18 = 1
            AND Y.INSCOV18 = 1
        ) SQ
    LEFT JOIN h206c C
        ON SQ.DUPERSID = C.DUPERSID
    UNION
    SELECT
        2018 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'INPATIENT' AS SETTING
        , D.EVNTIDX AS EVENT_ID
        , D.IPFPV18X + D.IPDPV18X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX18 = 1
            AND Y.INSCOV18 = 1
        ) SQ
    LEFT JOIN h206d D
        ON SQ.DUPERSID = D.DUPERSID
    UNION
    SELECT
        2018 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'ER' AS SETTING
        , E.EVNTIDX AS EVENT_ID
        , E.ERFPV18X + E.ERDPV18X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX18 = 1
            AND Y.INSCOV18 = 1
        ) SQ
    LEFT JOIN h206e E
        ON SQ.DUPERSID = E.DUPERSID
    UNION
    SELECT
        2018 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'OUTPATIENT' AS SETTING
        , F.EVNTIDX AS EVENT_ID
        , F.OPFPV18X + F.OPDPV18X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX18 = 1
            AND Y.INSCOV18 = 1
        ) SQ
    LEFT JOIN h206f F
        ON SQ.DUPERSID = F.DUPERSID
    UNION
    SELECT
        2018 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'OFFICE' AS SETTING
        , G.EVNTIDX AS EVENT_ID
        , G.OBPV18X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX18 = 1
            AND Y.INSCOV18 = 1
        ) SQ
    LEFT JOIN h206g G
        ON SQ.DUPERSID = G.DUPERSID
    UNION
        SELECT
        2018 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'HOME' AS SETTING
        , H.EVNTIDX AS EVENT_ID
        , H.HHPV18X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 18
            AND Y.AGELAST < 65
            AND Y.RACETHX IN (1, 2, 3, 4)
            AND Y.PRSTX18 = 1
            AND Y.INSCOV18 = 1
        ) SQ
    LEFT JOIN h206h H
        ON SQ.DUPERSID = H.DUPERSID
    """
df_Y = pd.read_sql_query(QUERY, db_con)
df_Y = df_Y[df_Y['SETTING'] != 'DENTAL'] # Drop rows by condition
df_Y = df_Y.dropna()
df_Y
df_Y.to_csv('_data//' + label_name + '//' + label_run + '//' + label_query + '.csv', index = False)

### Query all events that match ID for given year from each setting
label_query = 'appendix'
QUERY = """
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , Z.CONDIDX AS CONDITION_ID
        , Z.EVNTIDX AS EVENT_ID
    FROM (
        SELECT DISTINCT DUPERSID 
        FROM h224
        WHERE
            AGELAST > 18
            AND AGELAST < 65
            AND RACETHX IN (1, 2, 3, 4)
            AND PRSTX20 = 1
            AND INSCOV20 = 1
        ) SQ
    LEFT JOIN h220if1 Z
        ON SQ.DUPERSID = Z.DUPERSID
    UNION
    SELECT
        2019 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , Z.CONDIDX AS CONDITION_ID
        , Z.EVNTIDX AS EVENT_ID
    FROM (
        SELECT DISTINCT DUPERSID 
        FROM h216 Z
        WHERE
            AGELAST > 18
            AND AGELAST < 65
            AND RACETHX IN (1, 2, 3, 4)
            AND PRSTX19 = 1
            AND INSCOV19 = 1
        ) SQ
    LEFT JOIN h213if1 Z
        ON SQ.DUPERSID = Z.DUPERSID
    UNION
    SELECT
        2018 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , Z.CONDIDX AS CONDITION_ID
        , Z.EVNTIDX AS EVENT_ID
    FROM (
        SELECT DISTINCT DUPERSID 
        FROM h209
        WHERE
            AGELAST > 18
            AND AGELAST < 65
            AND RACETHX IN (1, 2, 3, 4)
            AND PRSTX18 = 1
            AND INSCOV18 = 1
        ) SQ
    LEFT JOIN h206if1 Z
        ON SQ.DUPERSID = Z.DUPERSID
    """
df_Z = pd.read_sql_query(QUERY, db_con)
df_Z
df_Z.to_csv('_data//' + label_name + '//' + label_run + '//' + label_query + '.csv', index = False)

### Merge to build clean table
df_XZ = pd.merge(df_Z, df_X.filter(['YEAR', 'CONDITION_ID', 'EVENT_ID', 'ICD10']), on = ['YEAR', 'CONDITION_ID'], how = 'left')
df_XZ = df_XZ.filter(['PERSON_ID', 'CONDITION_ID', 'EVENT_ID', 'YEAR', 'ICD10'])
df_XYZ = pd.merge(df_XZ, df_Y.filter(['EVENT_ID', 'SETTING', 'PAID']), on = ['EVENT_ID'], how = 'left')
df_WXYZ = pd.merge(df_W, df_XYZ, on = ['YEAR', 'PERSON_ID'], how = 'left')
df_WXYZ.to_csv('_data//' + label_name + '//' + label_run + '//clean.csv', index = False)

### Save datafram info for output
buffer = io.StringIO()
df_WXYZ.info(buf = buffer)
info = buffer.getvalue()

### Clean Memory
df_W = []
df_X = []
df_Y = []
df_Z = []
df_WY = []
df_XZ = []
#df_WXYZ = []

### Markdown Summary in docs subrepo
text_md = open('_docs//' + label_name + '//' + label_run + '//summary.md', 'a')
text_md.write('### ' + 'Data Cleaning Summary' + '\n')
text_md.write('Raw data was subset for the following conditions:' + '\n')
text_md.write('\n')
text_md.write('##### ' + 'Households' + '\n')
text_md.write('Individuals 26-64 with marketplace coverage for full year' + '\n')
text_md.write("""
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
    """ + '\n')
text_md.write('\n')
text_md.write('##### ' + 'Events' + '\n')
text_md.write('Non-Dental events for year individual has marketpalce coverage' + '\n')
text_md.write(""" 
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

    """ + '\n')
text_md.write('\n')
text_md.write('##### ' + 'Conditions' + '\n')
text_md.write('Any for individual in same year as marketpalce coverage' + '\n')
text_md.write("""
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
    """ + '\n')
text_md.write('\n')
text_md.write('##### Final Analytical Data ' + '\n')
text_md.write('\n')
text_md.write('<pre>')
text_md.write('\n')
text_md.write(info)
text_md.write('\n')
text_md.write('</pre>')
text_md.write('\n')
text_md.write('\n')
text_md.close()