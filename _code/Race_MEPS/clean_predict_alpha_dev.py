# Clean

### Query all individuals with marketplace coverage for full year in age range
QUERY = """
    SELECT
        2020 AS YEAR
        , W.DUPERSID AS ID
        , W.AGELAST AS AGE
        , W.SEX
        , W.RACETHX AS RACE
        , W.RACEAX
        , W.RACEBX
        , W.RACEWX
        , W.RACEV1X
        , W.RACEV2X
        , W.POVCAT20 AS FPL_GRP
        , W.POVLEV20 AS FPL_PCT
    FROM h224 W
    WHERE
        W.AGELAST > 25
        AND W.AGELAST < 65
        AND W.PRSTX20 = 1
        AND W.INSCOV20 = 1
    UNION
    SELECT
        2019 AS YEAR
        , W.DUPERSID AS ID
        , W.AGELAST AS AGE
        , W.SEX
        , W.RACETHX AS RACE
        , W.RACEAX
        , W.RACEBX
        , W.RACEWX
        , W.RACEV1X
        , W.RACEV2X
        , W.POVCAT19 AS FPL_GRP
        , W.POVLEV19 AS FPL_PCT
    FROM h216 W
    WHERE
        W.AGELAST > 25
        AND W.AGELAST < 65
        AND W.PRSTX19 = 1
        AND W.INSCOV19 = 1
    UNION
    SELECT
        2018 AS YEAR
        , W.DUPERSID AS ID
        , W.AGELAST AS AGE
        , W.SEX
        , W.RACETHX AS RACE
        , W.RACEAX
        , W.RACEBX
        , W.RACEWX
        , W.RACEV1X
        , W.RACEV2X
        , W.POVCAT18 AS FPL_GRP
        , W.POVLEV18 AS FPL_PCT
    FROM h209 W
    WHERE
        W.AGELAST > 25
        AND W.AGELAST < 65
        AND W.PRSTX18 = 1
        AND W.INSCOV18 = 1
    """
df_W = pd.read_sql_query(QUERY, db_con)
df_W

### Query all events that match ID for given year from each setting
QUERY = """
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID
        , 'RX' AS SETTING
        , A.LINKIDX AS LINK
        , A.RXPV20X AS PAID
    FROM (
        SELECT DISTINCT Z.DUPERSID 
        FROM h224 Z
        WHERE
            Z.AGELAST > 25
            AND Z.AGELAST < 65
            AND Z.PRSTX20 = 1
            AND Z.INSCOV20 = 1
        ) SQ
    LEFT JOIN h220a A
        ON SQ.DUPERSID = A.DUPERSID
    UNION
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID
        , 'DENTAL' AS SETTING
        , B.EVNTIDX AS LINK
        , B.DVPV20X AS PAID
    FROM (
        SELECT DISTINCT Z.DUPERSID 
        FROM h224 Z
        WHERE
            Z.AGELAST > 25
            AND Z.AGELAST < 65
            AND Z.PRSTX20 = 1
            AND Z.INSCOV20 = 1
        ) SQ
    LEFT JOIN h220b B
        ON SQ.DUPERSID = B.DUPERSID
    UNION
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID
        , 'OTHER' AS SETTING
        , C.EVNTIDX AS LINK
        , C.OMPV20X AS PAID
    FROM (
        SELECT DISTINCT Z.DUPERSID 
        FROM h224 Z
        WHERE
            Z.AGELAST > 25
            AND Z.AGELAST < 65
            AND Z.PRSTX20 = 1
            AND Z.INSCOV20 = 1
        ) SQ
    LEFT JOIN h220c C
        ON SQ.DUPERSID = C.DUPERSID
    UNION
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID
        , 'INPATIENT' AS SETTING
        , D.EVNTIDX AS LINK
        , D.IPFPV20X + D.IPDPV20X AS PAID
    FROM (
        SELECT DISTINCT Z.DUPERSID 
        FROM h224 Z
        WHERE
            Z.AGELAST > 25
            AND Z.AGELAST < 65
            AND Z.PRSTX20 = 1
            AND Z.INSCOV20 = 1
        ) SQ
    LEFT JOIN h220d D
        ON SQ.DUPERSID = D.DUPERSID
    UNION
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID
        , 'ER' AS SETTING
        , E.EVNTIDX AS LINK
        , E.ERFPV20X + E.ERDPV20X AS PAID
    FROM (
        SELECT DISTINCT Z.DUPERSID 
        FROM h224 Z
        WHERE
            Z.AGELAST > 25
            AND Z.AGELAST < 65
            AND Z.PRSTX20 = 1
            AND Z.INSCOV20 = 1
        ) SQ
    LEFT JOIN h220e E
        ON SQ.DUPERSID = E.DUPERSID
    UNION
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID
        , 'OUTPATIENT' AS SETTING
        , F.EVNTIDX AS LINK
        , F.OPFPV20X + F.OPDPV20X AS PAID
    FROM (
        SELECT DISTINCT Z.DUPERSID 
        FROM h224 Z
        WHERE
            Z.AGELAST > 25
            AND Z.AGELAST < 65
            AND Z.PRSTX20 = 1
            AND Z.INSCOV20 = 1
        ) SQ
    LEFT JOIN h220f F
        ON SQ.DUPERSID = F.DUPERSID
    UNION
    SELECT
        2020 AS YEAR
        , SQ.DUPERSID
        , 'OFFICE' AS SETTING
        , G.EVNTIDX AS LINK
        , G.OBPV20X AS PAID
    FROM (
        SELECT DISTINCT Z.DUPERSID 
        FROM h224 Z
        WHERE
            Z.AGELAST > 25
            AND Z.AGELAST < 65
            AND Z.PRSTX20 = 1
            AND Z.INSCOV20 = 1
        ) SQ
    LEFT JOIN h220g G
        ON SQ.DUPERSID = G.DUPERSID
    UNION
        SELECT
        2020 AS YEAR
        , SQ.DUPERSID
        , 'HOME' AS SETTING
        , H.EVNTIDX AS LINK
        , H.HHPV20X AS PAID
    FROM (
        SELECT DISTINCT Z.DUPERSID 
        FROM h224 Z
        WHERE
            Z.AGELAST > 25
            AND Z.AGELAST < 65
            AND Z.PRSTX20 = 1
            AND Z.INSCOV20 = 1
        ) SQ
    LEFT JOIN h220h H
        ON SQ.DUPERSID = H.DUPERSID
    """
df_Z = pd.read_sql_query(QUERY, db_con)
df_Z