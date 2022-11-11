# Clean

## SQlite Database in data subrepo
db_con = sqlite3.connect('_data//Race_MEPS//alpha_dev_20221110201226//database.db') # Create local database file connection object

### Query all individuals with marketplace coverage for full year in age range
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
        W.AGELAST > 25
        AND W.AGELAST < 65
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
        W.AGELAST > 25
        AND W.AGELAST < 65
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
        W.AGELAST > 25
        AND W.AGELAST < 65
        AND W.PRSTX18 = 1
        AND W.INSCOV18 = 1
    """
df_W = pd.read_sql_query(QUERY, db_con)
df_W
with pd.ExcelWriter('_fig//Race_MEPS//alpha_dev_20221110201226//results.xlsx', mode = 'a', engine = 'xlsxwriter') as writer:
    df_W.to_excel(writer, sheet_name = 'Households', index = False)

### Query all events that match ID for given year from each setting
QUERY = """
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , X.ICD10CDX AS ICD10
    FROM (
        SELECT DISTINCT DUPERSID 
        FROM h224
        WHERE
            AGELAST > 25
            AND AGELAST < 65
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
    FROM (
        SELECT DISTINCT DUPERSID 
        FROM h216
        WHERE
            AGELAST > 25
            AND AGELAST < 65
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
    FROM (
        SELECT DISTINCT DUPERSID 
        FROM h209
        WHERE
            AGELAST > 25
            AND AGELAST < 65
            AND PRSTX18 = 1
            AND INSCOV18 = 1
        ) SQ
    LEFT JOIN h207 X
        ON SQ.DUPERSID = X.DUPERSID
    """
df_X = pd.read_sql_query(QUERY, db_con)
df_X
with pd.ExcelWriter('_fig//Race_MEPS//alpha_dev_20221110201226//results.xlsx', mode = 'a', engine = 'xlsxwriter') as writer:
    df_X.to_excel(writer, sheet_name = 'Conditions', index = False)

### Query all events that match ID for given year from each setting
QUERY = """
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , 'RX' AS SETTING
        , A.LINKIDX AS EVENTID
        , A.RXPV20X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , B.EVNTIDX AS EVENTID
        , B.DVPV20X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , C.EVNTIDX AS EVENTID
        , C.OMPV20X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , D.EVNTIDX AS EVENTID
        , D.IPFPV20X + D.IPDPV20X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , E.EVNTIDX AS EVENTID
        , E.ERFPV20X + E.ERDPV20X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , F.EVNTIDX AS EVENTID
        , F.OPFPV20X + F.OPDPV20X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , G.EVNTIDX AS EVENTID
        , G.OBPV20X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , H.EVNTIDX AS EVENTID
        , H.HHPV20X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h224 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , A.LINKIDX AS EVENTID
        , A.RXPV19X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h216 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , B.EVNTIDX AS EVENTID
        , B.DVPV19X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h216 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , C.EVNTIDX AS EVENTID
        , C.OMPV19X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h216 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , D.EVNTIDX AS EVENTID
        , D.IPFPV19X + D.IPDPV19X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h216 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , E.EVNTIDX AS EVENTID
        , E.ERFPV19X + E.ERDPV19X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h216 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , F.EVNTIDX AS EVENTID
        , F.OPFPV19X + F.OPDPV19X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h216 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , G.EVNTIDX AS EVENTID
        , G.OBPV19X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h216 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , H.EVNTIDX AS EVENTID
        , H.HHPV19X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h216 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , A.LINKIDX AS EVENTID
        , A.RXPV18X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , B.EVNTIDX AS EVENTID
        , B.DVPV18X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , C.EVNTIDX AS EVENTID
        , C.OMPV18X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , D.EVNTIDX AS EVENTID
        , D.IPFPV18X + D.IPDPV18X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , E.EVNTIDX AS EVENTID
        , E.ERFPV18X + E.ERDPV18X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , F.EVNTIDX AS EVENTID
        , F.OPFPV18X + F.OPDPV18X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , G.EVNTIDX AS EVENTID
        , G.OBPV18X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
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
        , H.EVNTIDX AS EVENTID
        , H.HHPV18X AS PAID
    FROM (
        SELECT DISTINCT Y.DUPERSID 
        FROM h209 Y
        WHERE
            Y.AGELAST > 25
            AND Y.AGELAST < 65
            AND Y.PRSTX18 = 1
            AND Y.INSCOV18 = 1
        ) SQ
    LEFT JOIN h206h H
        ON SQ.DUPERSID = H.DUPERSID
    """
df_Y = pd.read_sql_query(QUERY, db_con)
df_Y
with pd.ExcelWriter('_fig//Race_MEPS//alpha_dev_20221110201226//results.xlsx', mode = 'a', engine = 'xlsxwriter') as writer:
    df_Y.to_excel(writer, sheet_name = 'Events', index = False)

### Query all events that match ID for given year from each setting
QUERY = """
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , Z.CLNKIDX AS LINK
    FROM (
        SELECT DISTINCT DUPERSID 
        FROM h224
        WHERE
            AGELAST > 25
            AND AGELAST < 65
            AND PRSTX20 = 1
            AND INSCOV20 = 1
        ) SQ
    LEFT JOIN h220if1 Z
        ON SQ.DUPERSID = Z.DUPERSID
    UNION
    SELECT
        2019 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , Z.CLNKIDX AS LINK
    FROM (
        SELECT DISTINCT DUPERSID 
        FROM h216 Z
        WHERE
            AGELAST > 25
            AND AGELAST < 65
            AND PRSTX19 = 1
            AND INSCOV19 = 1
        ) SQ
    LEFT JOIN h213if1 Z
        ON SQ.DUPERSID = Z.DUPERSID
    UNION
    SELECT
        2018 AS YEAR
        , SQ.DUPERSID AS PERSON_ID
        , Z.CLNKIDX AS LINK
    FROM (
        SELECT DISTINCT DUPERSID 
        FROM h209
        WHERE
            AGELAST > 25
            AND AGELAST < 65
            AND PRSTX18 = 1
            AND INSCOV18 = 1
        ) SQ
    LEFT JOIN h206if1 Z
        ON SQ.DUPERSID = Z.DUPERSID
    """
df_Z = pd.read_sql_query(QUERY, db_con)
df_Z
with pd.ExcelWriter('_fig//Race_MEPS//alpha_dev_20221110201226//results.xlsx', mode = 'a', engine = 'xlsxwriter') as writer:
    df_Z.to_excel(writer, sheet_name = 'Appendix', index = False)