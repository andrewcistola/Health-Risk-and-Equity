# -----------------------------------------------------------------------------             
# R programming statements for H212 data                                              
#                                                                                           
# This file contains programming statements needed to import the ASCII data                 
# file (.dat) into R. The R programming language has the capability to produce              
# appropriate standard errors for estimates from a survey with a complex sample             
# design such as the Medical Expenditure Panel Survey (MEPS).                               
#                                                       
# The input file is the ASCII data file (h212.dat) supplied in this PUF                
# release, which can be extracted from the .zip file supplied at the MEPS                   
# website: https://meps.ahrq.gov/mepsweb/data_stats/download_data_files.jsp                 
#                                                       
# This code imports the MEPS data into R as a data frame called h212.                  
#                                                       
# Note that additional packages are needed to successfully run this code. To                
# install these packages, run the 'install.packages' function (shown below).                
# Once installed, the packages can be called using the 'library' function.                  
# Packages only need to be installed once, but they must be called using the                
# 'library' function every time a new R session is started.                                 
#                                                       
# Two options are available to run this code:                                               
#                                                       
#  1. Copy and paste the code into an interactive R session.                                
#                                                       
#     The user must first download the ASCII (.dat) file from the MEPS website              
#     and save it to a local directory, which must be defined in the                        
#     'meps_path' variable below. In this example, the local directory is                   
#     called 'C:/MEPS'. Note that the path structure will differ on Mac and PC.             
#                                                       
#                                                       
#  2. Call this code directly from an interactive R session.                                
#                                                       
#  (a) If the ASCII (.dat) file has already been downloaded from the MEPS                   
#         website and saved to a local directory, the following code can be run             
#         (after re-defining the 'meps_path' variable to point to the location              
#         of the h212.dat file.)                                   
#                                                       
#     meps_path <- C:/MEPS/h212.dat                                
#     source(https://meps.ahrq.gov/mepsweb/data_stats/download_data/pufs/{foldername}/h212ru.txt)  
#     head(h212) # view data                                       
#                                                       
#  (b) Alternatively, the ASCII (.dat) file can be downloaded directly from                 
#         the MEPS website. The following code can be used to download and                  
#         import the H212 data into R without having to manually download,             
#         unzip, and store the file on your local computer.                         
#                                                       
#           url <- https://meps.ahrq.gov/mepsweb/data_files/pufs/h212dat.zip           
#           download.file(url, temp <- tempfile())                              
#                                                       
#     meps_path <- unzip(temp, exdir = tempdir())                               
#     source(https://meps.ahrq.gov/mepsweb/data_stats/download_data/pufs/{foldername}/h212ru.txt)  
#                                                       
#           unlink(temp)  # Unlink to delete temporary file                         
#                                                       
#           head(h212) # view data                                 
#                                                       
# -----------------------------------------------------------------------------             
                                                        
# DEFINE 'meps_path' -----------------------------------------------------------            
# 'meps_path' should point to the file path of the ASCII file (h212.dat)               
# Here, the 'exists' function checks whether meps_path is already defined. This             
# feature is useful if calling this file from an external source.                           
if(!exists("meps_path"))  meps_path = "H212.dat"      

# INSTALL PACKAGES ------------------------------------------------------------
# Uncomment and run this portion if packages are not yet installed         
#                                          
# install.packages("readr")                            
                                           
# **************************************
# LOAD PACKAGES ---------------------------------------------------------------

# Run this for every new R session      

library(readr)                          

# DATA FILE INFO ------------------------------------------

# Define start and end positions to read fixed-width file  


pos_start <- c(
1, 8, 11, 21, 23, 25, 27, 29, 31, 33, 
35, 37, 39, 42, 44, 46, 48, 50, 52, 54, 
56, 57, 59, 61, 63, 65, 67, 69, 71, 72, 
74, 76, 78, 80, 83, 86, 89, 92, 93, 94, 
95, 96, 98, 100, 102, 103, 105, 107, 111, 113, 
117, 119, 123, 125, 129, 131, 135, 137, 141, 143, 
147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 
157, 158, 160, 162, 164, 166, 168, 170, 172, 174, 
176, 178, 180, 182, 186, 187, 188, 190, 191, 192, 
193, 194, 195, 196, 198, 200, 202, 204, 207, 210, 
213, 216, 219, 222, 225, 228, 231, 234, 236, 238, 
240, 242, 244, 246, 248, 250, 252, 254, 256, 259, 
261, 263, 266, 268, 270, 272, 274, 276, 278, 280, 
283, 285, 287, 290, 292, 295, 297, 300, 302, 305, 
307, 309, 312, 314, 317, 319, 321, 324, 326, 329, 
331, 333, 335, 337, 339, 341, 343, 345, 347, 349, 
351, 353, 356, 358, 360, 363, 365, 368, 371, 373, 
376, 379, 381, 384, 386, 389, 391, 394, 396, 399, 
402, 404, 406, 408, 410, 412, 414, 416, 418, 420, 
422, 424, 426, 428, 430, 432, 434, 436, 438, 440, 
442, 444, 446, 448, 450, 452, 454, 457, 460, 462, 
464, 467, 469, 471, 474, 476, 478, 481, 483, 485, 
488, 490, 492, 495, 498, 501, 504, 507, 510, 513, 
516, 519, 522, 525, 528, 531, 534, 536, 539, 541, 
544, 546, 548, 550, 552, 554, 557, 559, 562, 565, 
568, 569, 572, 575, 578, 581, 584, 587, 590, 593, 
596, 599, 602, 605, 608, 614, 620, 622, 625, 628, 
631, 634, 637, 640, 643, 646, 649, 652, 655, 658, 
661, 664, 666, 669, 671, 674, 677, 680, 682, 685, 
688, 690, 693, 696, 699, 702, 705, 707, 710, 712, 
715, 718, 722, 724, 727, 730, 733, 735, 737, 739, 
741, 743, 745, 747, 749, 751, 753, 755, 757, 759, 
761, 763, 765, 767, 769, 771, 773, 775, 777, 779, 
781, 783, 785, 787, 789, 791, 793, 796, 799, 802, 
805, 808, 811, 814, 817, 823, 829, 835, 836, 837, 
838, 841, 844, 847, 850, 853, 856, 862, 868, 874, 
877, 880, 883, 886, 889, 892, 895, 898, 901, 904, 
907, 910, 913, 916, 919, 922, 925, 928, 931, 934, 
937, 940, 943, 946, 949, 952, 955, 958, 961, 964, 
967, 970, 972, 975, 978, 981, 984, 987, 991, 994, 
998, 1001, 1005, 1008, 1011, 1014, 1017, 1020, 1023, 1026, 
1029, 1032, 1035, 1038, 1041, 1044, 1047, 1050, 1053, 1056, 
1059, 1062, 1065, 1068, 1071, 1074, 1077, 1080, 1083, 1086, 
1089, 1092, 1095, 1098, 1100, 1102, 1104, 1106, 1108, 1110, 
1112, 1114, 1116, 1118, 1120, 1122, 1124, 1126, 1128, 1130, 
1132, 1134, 1136, 1138, 1140, 1142, 1144, 1146, 1148, 1150, 
1152, 1154, 1156, 1158, 1160, 1162, 1164, 1166, 1168, 1170, 
1172, 1174, 1176, 1178, 1180, 1182, 1184, 1186, 1188, 1190, 
1192, 1194, 1196, 1198, 1200, 1202, 1204, 1206, 1208, 1210, 
1212, 1214, 1216, 1218, 1220, 1222, 1224, 1226, 1228, 1230, 
1232, 1234, 1236, 1238, 1240, 1242, 1244, 1246, 1248, 1250, 
1252, 1254, 1256, 1258, 1260, 1262, 1264, 1266, 1268, 1270, 
1272, 1274, 1276, 1278, 1280, 1282, 1284, 1286, 1288, 1290, 
1292, 1294, 1296, 1298, 1300, 1302, 1304, 1306, 1308, 1310, 
1312, 1314, 1316, 1318, 1320, 1322, 1324, 1326, 1328, 1330, 
1332, 1334, 1336, 1338, 1340, 1342, 1344, 1346, 1348, 1350, 
1352, 1354, 1356, 1358, 1360, 1362, 1364, 1366, 1368, 1370, 
1372, 1374, 1376, 1378, 1380, 1382, 1384, 1386, 1388, 1390, 
1392, 1394, 1396, 1398, 1400, 1402, 1404, 1406, 1408, 1410, 
1412, 1414, 1416, 1418, 1420, 1422, 1424, 1426, 1428, 1430, 
1432, 1434, 1436, 1438, 1440, 1442, 1444, 1446, 1448, 1450, 
1452, 1454, 1456, 1458, 1460, 1462, 1464, 1466, 1468, 1470, 
1472, 1474, 1476, 1478, 1480, 1482, 1484, 1486, 1488, 1490, 
1492, 1494, 1496, 1498, 1500, 1502, 1504, 1506, 1508, 1510, 
1512, 1514, 1516, 1518, 1520, 1522, 1524, 1526, 1528, 1530, 
1532, 1534, 1536, 1538, 1540, 1542, 1544, 1546, 1548, 1550, 
1552, 1554, 1556, 1558, 1560, 1562, 1564, 1566, 1568, 1570, 
1572, 1574, 1576, 1578, 1580, 1582, 1584, 1586, 1588, 1590, 
1592, 1594, 1596, 1598, 1600, 1602, 1604, 1606, 1608, 1610, 
1612, 1614, 1616, 1618, 1620, 1622, 1624, 1626, 1628, 1630, 
1632, 1634, 1636, 1638, 1640, 1642, 1644, 1646, 1648, 1650, 
1652, 1654, 1656, 1658, 1660, 1662, 1664, 1666, 1668, 1670, 
1672, 1674, 1676, 1678, 1680, 1682, 1684, 1686, 1688, 1690, 
1692, 1694, 1696, 1698, 1700, 1702, 1704, 1706, 1708, 1710, 
1712, 1714, 1716, 1718, 1720, 1722, 1723, 1724, 1725, 1726, 
1727, 1728, 1729, 1730, 1731, 1732, 1733, 1735, 1737, 1739, 
1741, 1743, 1745, 1747, 1749, 1751, 1753, 1755, 1757, 1759, 
1761, 1763, 1766, 1769, 1772, 1775, 1778, 1781, 1784, 1787, 
1790, 1793, 1796, 1799, 1802, 1805, 1808, 1811, 1814, 1817, 
1820, 1823, 1826, 1828, 1831, 1838, 1840, 1842, 1844, 1846, 
1848, 1850, 1852, 1854, 1856, 1858, 1860, 1862, 1864, 1866, 
1868, 1870, 1872, 1874, 1876, 1878, 1880, 1882, 1884, 1886, 
1888, 1890, 1892, 1894, 1896, 1898, 1900, 1902, 1904, 1906, 
1908, 1910, 1912, 1914, 1916, 1918, 1920, 1922, 1924, 1926, 
1928, 1930, 1932, 1934, 1936, 1938, 1940, 1942, 1944, 1946, 
1948, 1950, 1952, 1954, 1956, 1958, 1960, 1962, 1964, 1966, 
1968, 1970, 1972, 1974, 1976, 1978, 1980, 1982, 1984, 1986, 
1988, 1990, 1992, 1994, 1996, 1998, 2000, 2002, 2004, 2006, 
2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024, 2026, 
2028, 2030, 2032, 2034, 2036, 2038, 2040, 2042, 2044, 2046, 
2048, 2050, 2052, 2054, 2056, 2058, 2060, 2062, 2064, 2066, 
2068, 2070, 2072, 2074, 2076, 2078, 2080, 2082, 2084, 2086, 
2088, 2090, 2092, 2094, 2096, 2098, 2100, 2102, 2104, 2106, 
2108, 2110, 2112, 2114, 2116, 2118, 2120, 2123, 2126, 2129, 
2132, 2135, 2138, 2141, 2143, 2144, 2147, 2149, 2152, 2155, 
2158, 2161, 2173, 2186, 2190)


pos_end <- c(
7, 10, 20, 22, 24, 26, 28, 30, 32, 34, 
36, 38, 41, 43, 45, 47, 49, 51, 53, 55, 
56, 58, 60, 62, 64, 66, 68, 70, 71, 73, 
75, 77, 79, 82, 85, 88, 91, 92, 93, 94, 
95, 97, 99, 101, 102, 104, 106, 110, 112, 116, 
118, 122, 124, 128, 130, 134, 136, 140, 142, 146, 
147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 
157, 159, 161, 163, 165, 167, 169, 171, 173, 175, 
177, 179, 181, 185, 186, 187, 189, 190, 191, 192, 
193, 194, 195, 197, 199, 201, 203, 206, 209, 212, 
215, 218, 221, 224, 227, 230, 233, 235, 237, 239, 
241, 243, 245, 247, 249, 251, 253, 255, 258, 260, 
262, 265, 267, 269, 271, 273, 275, 277, 279, 282, 
284, 286, 289, 291, 294, 296, 299, 301, 304, 306, 
308, 311, 313, 316, 318, 320, 323, 325, 328, 330, 
332, 334, 336, 338, 340, 342, 344, 346, 348, 350, 
352, 355, 357, 359, 362, 364, 367, 370, 372, 375, 
378, 380, 383, 385, 388, 390, 393, 395, 398, 401, 
403, 405, 407, 409, 411, 413, 415, 417, 419, 421, 
423, 425, 427, 429, 431, 433, 435, 437, 439, 441, 
443, 445, 447, 449, 451, 453, 456, 459, 461, 463, 
466, 468, 470, 473, 475, 477, 480, 482, 484, 487, 
489, 491, 494, 497, 500, 503, 506, 509, 512, 515, 
518, 521, 524, 527, 530, 533, 535, 538, 540, 543, 
545, 547, 549, 551, 553, 556, 558, 561, 564, 567, 
568, 571, 574, 577, 580, 583, 586, 589, 592, 595, 
598, 601, 604, 607, 613, 619, 621, 624, 627, 630, 
633, 636, 639, 642, 645, 648, 651, 654, 657, 660, 
663, 665, 668, 670, 673, 676, 679, 681, 684, 687, 
689, 692, 695, 698, 701, 704, 706, 709, 711, 714, 
717, 721, 723, 726, 729, 732, 734, 736, 738, 740, 
742, 744, 746, 748, 750, 752, 754, 756, 758, 760, 
762, 764, 766, 768, 770, 772, 774, 776, 778, 780, 
782, 784, 786, 788, 790, 792, 795, 798, 801, 804, 
807, 810, 813, 816, 822, 828, 834, 835, 836, 837, 
840, 843, 846, 849, 852, 855, 861, 867, 873, 876, 
879, 882, 885, 888, 891, 894, 897, 900, 903, 906, 
909, 912, 915, 918, 921, 924, 927, 930, 933, 936, 
939, 942, 945, 948, 951, 954, 957, 960, 963, 966, 
969, 971, 974, 977, 980, 983, 986, 990, 993, 997, 
1000, 1004, 1007, 1010, 1013, 1016, 1019, 1022, 1025, 1028, 
1031, 1034, 1037, 1040, 1043, 1046, 1049, 1052, 1055, 1058, 
1061, 1064, 1067, 1070, 1073, 1076, 1079, 1082, 1085, 1088, 
1091, 1094, 1097, 1099, 1101, 1103, 1105, 1107, 1109, 1111, 
1113, 1115, 1117, 1119, 1121, 1123, 1125, 1127, 1129, 1131, 
1133, 1135, 1137, 1139, 1141, 1143, 1145, 1147, 1149, 1151, 
1153, 1155, 1157, 1159, 1161, 1163, 1165, 1167, 1169, 1171, 
1173, 1175, 1177, 1179, 1181, 1183, 1185, 1187, 1189, 1191, 
1193, 1195, 1197, 1199, 1201, 1203, 1205, 1207, 1209, 1211, 
1213, 1215, 1217, 1219, 1221, 1223, 1225, 1227, 1229, 1231, 
1233, 1235, 1237, 1239, 1241, 1243, 1245, 1247, 1249, 1251, 
1253, 1255, 1257, 1259, 1261, 1263, 1265, 1267, 1269, 1271, 
1273, 1275, 1277, 1279, 1281, 1283, 1285, 1287, 1289, 1291, 
1293, 1295, 1297, 1299, 1301, 1303, 1305, 1307, 1309, 1311, 
1313, 1315, 1317, 1319, 1321, 1323, 1325, 1327, 1329, 1331, 
1333, 1335, 1337, 1339, 1341, 1343, 1345, 1347, 1349, 1351, 
1353, 1355, 1357, 1359, 1361, 1363, 1365, 1367, 1369, 1371, 
1373, 1375, 1377, 1379, 1381, 1383, 1385, 1387, 1389, 1391, 
1393, 1395, 1397, 1399, 1401, 1403, 1405, 1407, 1409, 1411, 
1413, 1415, 1417, 1419, 1421, 1423, 1425, 1427, 1429, 1431, 
1433, 1435, 1437, 1439, 1441, 1443, 1445, 1447, 1449, 1451, 
1453, 1455, 1457, 1459, 1461, 1463, 1465, 1467, 1469, 1471, 
1473, 1475, 1477, 1479, 1481, 1483, 1485, 1487, 1489, 1491, 
1493, 1495, 1497, 1499, 1501, 1503, 1505, 1507, 1509, 1511, 
1513, 1515, 1517, 1519, 1521, 1523, 1525, 1527, 1529, 1531, 
1533, 1535, 1537, 1539, 1541, 1543, 1545, 1547, 1549, 1551, 
1553, 1555, 1557, 1559, 1561, 1563, 1565, 1567, 1569, 1571, 
1573, 1575, 1577, 1579, 1581, 1583, 1585, 1587, 1589, 1591, 
1593, 1595, 1597, 1599, 1601, 1603, 1605, 1607, 1609, 1611, 
1613, 1615, 1617, 1619, 1621, 1623, 1625, 1627, 1629, 1631, 
1633, 1635, 1637, 1639, 1641, 1643, 1645, 1647, 1649, 1651, 
1653, 1655, 1657, 1659, 1661, 1663, 1665, 1667, 1669, 1671, 
1673, 1675, 1677, 1679, 1681, 1683, 1685, 1687, 1689, 1691, 
1693, 1695, 1697, 1699, 1701, 1703, 1705, 1707, 1709, 1711, 
1713, 1715, 1717, 1719, 1721, 1722, 1723, 1724, 1725, 1726, 
1727, 1728, 1729, 1730, 1731, 1732, 1734, 1736, 1738, 1740, 
1742, 1744, 1746, 1748, 1750, 1752, 1754, 1756, 1758, 1760, 
1762, 1765, 1768, 1771, 1774, 1777, 1780, 1783, 1786, 1789, 
1792, 1795, 1798, 1801, 1804, 1807, 1810, 1813, 1816, 1819, 
1822, 1825, 1827, 1830, 1837, 1839, 1841, 1843, 1845, 1847, 
1849, 1851, 1853, 1855, 1857, 1859, 1861, 1863, 1865, 1867, 
1869, 1871, 1873, 1875, 1877, 1879, 1881, 1883, 1885, 1887, 
1889, 1891, 1893, 1895, 1897, 1899, 1901, 1903, 1905, 1907, 
1909, 1911, 1913, 1915, 1917, 1919, 1921, 1923, 1925, 1927, 
1929, 1931, 1933, 1935, 1937, 1939, 1941, 1943, 1945, 1947, 
1949, 1951, 1953, 1955, 1957, 1959, 1961, 1963, 1965, 1967, 
1969, 1971, 1973, 1975, 1977, 1979, 1981, 1983, 1985, 1987, 
1989, 1991, 1993, 1995, 1997, 1999, 2001, 2003, 2005, 2007, 
2009, 2011, 2013, 2015, 2017, 2019, 2021, 2023, 2025, 2027, 
2029, 2031, 2033, 2035, 2037, 2039, 2041, 2043, 2045, 2047, 
2049, 2051, 2053, 2055, 2057, 2059, 2061, 2063, 2065, 2067, 
2069, 2071, 2073, 2075, 2077, 2079, 2081, 2083, 2085, 2087, 
2089, 2091, 2093, 2095, 2097, 2099, 2101, 2103, 2105, 2107, 
2109, 2111, 2113, 2115, 2117, 2119, 2122, 2125, 2128, 2131, 
2134, 2137, 2140, 2142, 2143, 2146, 2148, 2151, 2154, 2157, 
2160, 2172, 2185, 2189, 2190)


var_names <- c(
"DUID", "PID", "DUPERSID", "PANEL", "FAMID31", "FAMID42", "FAMID53", "FAMID19", "FAMIDYR", "RULETR31", 
"RULETR42", "RULETR53", "RULETR19", "RUSIZE31", "RUSIZE42", "RUSIZE53", "RUSIZE19", "RUCLAS31", "RUCLAS42", "RUCLAS53", 
"RUCLAS19", "FAMSZE31", "FAMSZE42", "FAMSZE53", "FAMSZE19", "FMRS1231", "FAMS1231", "FAMSZEYR", "FAMRFPYR", "REGION31", 
"REGION42", "REGION53", "REGION19", "REFPRS31", "REFPRS42", "REFPRS53", "REFPRS19", "RESP31", "RESP42", "RESP53", 
"RESP19", "PROXY31", "PROXY42", "PROXY53", "PROXY19", "INTVLANG", "BEGRFM31", "BEGRFY31", "ENDRFM31", "ENDRFY31", 
"BEGRFM42", "BEGRFY42", "ENDRFM42", "ENDRFY42", "BEGRFM53", "BEGRFY53", "ENDRFM53", "ENDRFY53", "ENDRFM19", "ENDRFY19", 
"KEYNESS", "INSCOP31", "INSCOP42", "INSCOP53", "INSCOP19", "INSC1231", "INSCOPE", "ELGRND31", "ELGRND42", "ELGRND53", 
"ELGRND19", "PSTATS31", "PSTATS42", "PSTATS53", "RURSLT31", "RURSLT42", "RURSLT53", "AGE31X", "AGE42X", "AGE53X", 
"AGE19X", "AGELAST", "DOBMM", "DOBYY", "SEX", "RACEV1X", "RACEV2X", "RACEAX", "RACEBX", "RACEWX", 
"RACETHX", "HISPANX", "HISPNCAT", "MARRY31X", "MARRY42X", "MARRY53X", "MARRY19X", "SPOUID31", "SPOUID42", "SPOUID53", 
"SPOUID19", "SPOUIN31", "SPOUIN42", "SPOUIN53", "SPOUIN19", "EDUCYR", "HIDEG", "FTSTU31X", "FTSTU42X", "FTSTU53X", 
"FTSTU19X", "ACTDTY31", "ACTDTY42", "ACTDTY53", "REFRL31X", "REFRL42X", "REFRL53X", "REFRL19X", "OTHLGSPK", "WHTLGSPK", 
"HWELLSPK", "BORNUSA", "YRSINUS", "RTHLTH31", "RTHLTH42", "RTHLTH53", "MNHLTH31", "MNHLTH42", "MNHLTH53", "HIBPDX", 
"HIBPAGED", "BPMLDX", "CHDDX", "CHDAGED", "ANGIDX", "ANGIAGED", "MIDX", "MIAGED", "OHRTDX", "OHRTAGED", 
"OHRTTYPE", "STRKDX", "STRKAGED", "EMPHDX", "EMPHAGED", "CHBRON31", "CHOLDX", "CHOLAGED", "CANCERDX", "CABLADDR", 
"CABREAST", "CACERVIX", "CACOLON", "CALUNG", "CALYMPH", "CAMELANO", "CAOTHER", "CAPROSTA", "CASKINNM", "CASKINDK", 
"CAUTERUS", "DIABDX_M18", "DIABAGED", "JTPAIN31_M18", "ARTHDX", "ARTHTYPE", "ARTHAGED", "ASTHDX", "ASTHAGED", "ASSTIL31", 
"ASATAK31", "ASTHEP31", "ASACUT31", "ASMRCN31", "ASPREV31", "ASDALY31", "ASPKFL31", "ASEVFL31", "ASWNFL31", "ADHDADDX", 
"ADHDAGED", "IADLHP31", "ADLHLP31", "AIDHLP31", "WLKLIM31", "LFTDIF31", "STPDIF31", "WLKDIF31", "MILDIF31", "STNDIF31", 
"BENDIF31", "RCHDIF31", "FNGRDF31", "ACTLIM31", "WRKLIM31", "HSELIM31", "SCHLIM31", "UNABLE31", "SOCLIM31", "COGLIM31", 
"DFHEAR42", "DFSEE42", "DFCOG42", "DFWLKC42", "DFDRSB42", "DFERND42", "ANYLMI19", "CHPMED42", "CHPMHB42", "CHPMCN42", 
"CHSERV42", "CHSRHB42", "CHSRCN42", "CHLIMI42", "CHLIHB42", "CHLICO42", "CHTHER42", "CHTHHB42", "CHTHCO42", "CHCOUN42", 
"CHEMPB42", "CSHCN42", "GETTRB42", "MOMPRO42", "DADPRO42", "UNHAP42", "SCHLBH42", "HAVFUN42", "ADUPRO42", "NERVAF42", 
"SIBPRO42", "KIDPRO42", "SPRPRO42", "SCHPRO42", "HOMEBH42", "CHILCR42", "CHILWW42", "CHRTCR42", "CHRTWW42", "CHAPPT42", 
"CHLIST42", "CHEXPL42", "CHRESP42", "CHPRTM42", "CHHECR42", "CHSPEC42_M18", "CHEYRE42_M18", "LSTETH53", "PHYEXE53", "OFTSMK53", 
"SAQELIG", "ADPROX42", "ADGENH42", "ADDAYA42", "ADCLIM42", "ADACLS42", "ADWKLM42", "ADEMLS42", "ADMWCF42", "ADPAIN42", 
"ADPCFL42", "ADENGY42", "ADPRST42", "ADSOCA42", "VPCS42", "VMCS42", "VRFLAG42", "ADNERV42", "ADHOPE42", "ADREST42", 
"ADSAD42", "ADEFRT42", "ADWRTH42", "K6SUM42", "ADINTR42", "ADDPRS42", "PHQ242", "ADINSA42", "ADINSB42", "ADRISK42", 
"ADOVER42", "ADILCR42", "ADILWW42", "ADRTCR42", "ADRTWW42", "ADAPPT42", "ADHECR42", "ADINST42", "ADEZUN42", "ADTLHW42", 
"ADFFRM42", "ADFHLP42", "ADEXPL42", "ADLIST42", "ADRESP42", "ADPRTM42", "ADSMOK42", "ADNSMK42", "ADSPCL42", "ADSNSP42", 
"ADCMPM42", "ADCMPY42", "ADLANG42", "DDNWRK19", "OTHDYS19", "OTHNDD19", "ACCELI42", "HAVEUS42", "PRACTP42", "YNOUSC42_M18", 
"PROVTY42_M18", "PLCTYP42", "TMTKUS42", "TYPEPE42", "LOCATN42", "HSPLAP42", "WHITPR42", "BLCKPR42", "ASIANP42", "NATAMP42", 
"PACISP42", "OTHRCP42", "GENDRP42", "PHNREG42", "OFFHOU42", "AFTHOU42", "TREATM42", "DECIDE42", "EXPLOP42", "PRVSPK42", 
"DLAYCA42", "AFRDCA42", "DLAYDN42", "AFRDDN42", "DLAYPM42", "AFRDPM42", "EMPST31", "EMPST42", "EMPST53", "RNDFLG31", 
"MORJOB31", "MORJOB42", "MORJOB53", "EVRWRK", "HRWG31X", "HRWG42X", "HRWG53X", "HRWGIM31", "HRWGIM42", "HRWGIM53", 
"HRHOW31", "HRHOW42", "HRHOW53", "DIFFWG31", "DIFFWG42", "DIFFWG53", "NHRWG31", "NHRWG42", "NHRWG53", "HOUR31", 
"HOUR42", "HOUR53", "TEMPJB31", "TEMPJB42", "TEMPJB53", "SSNLJB31", "SSNLJB42", "SSNLJB53", "SELFCM31", "SELFCM42", 
"SELFCM53", "DISVW31X", "DISVW42X", "DISVW53X", "CHOIC31", "CHOIC42", "CHOIC53", "INDCAT31", "INDCAT42", "INDCAT53", 
"NUMEMP31", "NUMEMP42", "NUMEMP53", "MORE31", "MORE42", "MORE53", "UNION31", "UNION42", "UNION53", "NWK31", 
"NWK42", "NWK53", "CHGJ3142", "CHGJ4253", "YCHJ3142", "YCHJ4253", "STJBMM31", "STJBYY31", "STJBMM42", "STJBYY42", 
"STJBMM53", "STJBYY53", "EVRETIRE", "OCCCAT31", "OCCCAT42", "OCCCAT53", "PAYVAC31", "PAYVAC42", "PAYVAC53", "SICPAY31", 
"SICPAY42", "SICPAY53", "PAYDR31", "PAYDR42", "PAYDR53", "RETPLN31", "RETPLN42", "RETPLN53", "BSNTY31", "BSNTY42", 
"BSNTY53", "JOBORG31", "JOBORG42", "JOBORG53", "HELD31X", "HELD42X", "HELD53X", "OFFER31X", "OFFER42X", "OFFER53X", 
"OFREMP31", "OFREMP42", "OFREMP53", "TRIJA19X", "TRIFE19X", "TRIMA19X", "TRIAP19X", "TRIMY19X", "TRIJU19X", "TRIJL19X", 
"TRIAU19X", "TRISE19X", "TRIOC19X", "TRINO19X", "TRIDE19X", "MCRJA19", "MCRFE19", "MCRMA19", "MCRAP19", "MCRMY19", 
"MCRJU19", "MCRJL19", "MCRAU19", "MCRSE19", "MCROC19", "MCRNO19", "MCRDE19", "MCRJA19X", "MCRFE19X", "MCRMA19X", 
"MCRAP19X", "MCRMY19X", "MCRJU19X", "MCRJL19X", "MCRAU19X", "MCRSE19X", "MCROC19X", "MCRNO19X", "MCRDE19X", "MCDJA19", 
"MCDFE19", "MCDMA19", "MCDAP19", "MCDMY19", "MCDJU19", "MCDJL19", "MCDAU19", "MCDSE19", "MCDOC19", "MCDNO19", 
"MCDDE19", "MCDJA19X", "MCDFE19X", "MCDMA19X", "MCDAP19X", "MCDMY19X", "MCDJU19X", "MCDJL19X", "MCDAU19X", "MCDSE19X", 
"MCDOC19X", "MCDNO19X", "MCDDE19X", "GVAJA19", "GVAFE19", "GVAMA19", "GVAAP19", "GVAMY19", "GVAJU19", "GVAJL19", 
"GVAAU19", "GVASE19", "GVAOC19", "GVANO19", "GVADE19", "GVBJA19", "GVBFE19", "GVBMA19", "GVBAP19", "GVBMY19", 
"GVBJU19", "GVBJL19", "GVBAU19", "GVBSE19", "GVBOC19", "GVBNO19", "GVBDE19", "GVCJA19", "GVCFE19", "GVCMA19", 
"GVCAP19", "GVCMY19", "GVCJU19", "GVCJL19", "GVCAU19", "GVCSE19", "GVCOC19", "GVCNO19", "GVCDE19", "VAPJA19", 
"VAPFE19", "VAPMA19", "VAPAP19", "VAPMY19", "VAPJU19", "VAPJL19", "VAPAU19", "VAPSE19", "VAPOC19", "VAPNO19", 
"VAPDE19", "IHSJA19", "IHSFE19", "IHSMA19", "IHSAP19", "IHSMY19", "IHSJU19", "IHSJL19", "IHSAU19", "IHSSE19", 
"IHSOC19", "IHSNO19", "IHSDE19", "PUBJA19X", "PUBFE19X", "PUBMA19X", "PUBAP19X", "PUBMY19X", "PUBJU19X", "PUBJL19X", 
"PUBAU19X", "PUBSE19X", "PUBOC19X", "PUBNO19X", "PUBDE19X", "PEGJA19", "PEGFE19", "PEGMA19", "PEGAP19", "PEGMY19", 
"PEGJU19", "PEGJL19", "PEGAU19", "PEGSE19", "PEGOC19", "PEGNO19", "PEGDE19", "PDKJA19", "PDKFE19", "PDKMA19", 
"PDKAP19", "PDKMY19", "PDKJU19", "PDKJL19", "PDKAU19", "PDKSE19", "PDKOC19", "PDKNO19", "PDKDE19", "PNGJA19", 
"PNGFE19", "PNGMA19", "PNGAP19", "PNGMY19", "PNGJU19", "PNGJL19", "PNGAU19", "PNGSE19", "PNGOC19", "PNGNO19", 
"PNGDE19", "POGJA19", "POGFE19", "POGMA19", "POGAP19", "POGMY19", "POGJU19", "POGJL19", "POGAU19", "POGSE19", 
"POGOC19", "POGNO19", "POGDE19", "POEJA19", "POEFE19", "POEMA19", "POEAP19", "POEMY19", "POEJU19", "POEJL19", 
"POEAU19", "POESE19", "POEOC19", "POENO19", "POEDE19", "PNEJA19", "PNEFE19", "PNEMA19", "PNEAP19", "PNEMY19", 
"PNEJU19", "PNEJL19", "PNEAU19", "PNESE19", "PNEOC19", "PNENO19", "PNEDE19", "PRXJA19", "PRXFE19", "PRXMA19", 
"PRXAP19", "PRXMY19", "PRXJU19", "PRXJL19", "PRXAU19", "PRXSE19", "PRXOC19", "PRXNO19", "PRXDE19", "PRIJA19", 
"PRIFE19", "PRIMA19", "PRIAP19", "PRIMY19", "PRIJU19", "PRIJL19", "PRIAU19", "PRISE19", "PRIOC19", "PRINO19", 
"PRIDE19", "HPEJA19", "HPEFE19", "HPEMA19", "HPEAP19", "HPEMY19", "HPEJU19", "HPEJL19", "HPEAU19", "HPESE19", 
"HPEOC19", "HPENO19", "HPEDE19", "HPDJA19", "HPDFE19", "HPDMA19", "HPDAP19", "HPDMY19", "HPDJU19", "HPDJL19", 
"HPDAU19", "HPDSE19", "HPDOC19", "HPDNO19", "HPDDE19", "HPNJA19", "HPNFE19", "HPNMA19", "HPNAP19", "HPNMY19", 
"HPNJU19", "HPNJL19", "HPNAU19", "HPNSE19", "HPNOC19", "HPNNO19", "HPNDE19", "HPOJA19", "HPOFE19", "HPOMA19", 
"HPOAP19", "HPOMY19", "HPOJU19", "HPOJL19", "HPOAU19", "HPOSE19", "HPOOC19", "HPONO19", "HPODE19", "HPXJA19", 
"HPXFE19", "HPXMA19", "HPXAP19", "HPXMY19", "HPXJU19", "HPXJL19", "HPXAU19", "HPXSE19", "HPXOC19", "HPXNO19", 
"HPXDE19", "HPRJA19", "HPRFE19", "HPRMA19", "HPRAP19", "HPRMY19", "HPRJU19", "HPRJL19", "HPRAU19", "HPRSE19", 
"HPROC19", "HPRNO19", "HPRDE19", "INSJA19X", "INSFE19X", "INSMA19X", "INSAP19X", "INSMY19X", "INSJU19X", "INSJL19X", 
"INSAU19X", "INSSE19X", "INSOC19X", "INSNO19X", "INSDE19X", "PRVEV19", "TRIEV19", "MCREV19", "MCDEV19", "VAEV19", 
"GVAEV19", "GVBEV19", "GVCEV19", "UNINS19", "INSCOV19", "INSURC19", "TRIST31X", "TRIST42X", "TRIST19X", "TRIPR31X", 
"TRIPR42X", "TRIPR19X", "TRIEX31X", "TRIEX42X", "TRIEX19X", "TRILI31X", "TRILI42X", "TRILI19X", "TRICH31X", "TRICH42X", 
"TRICH19X", "MCRPD31", "MCRPD42", "MCRPD19", "MCRPD31X", "MCRPD42X", "MCRPD19X", "MCRPB31", "MCRPB42", "MCRPB19", 
"MCRPHO31", "MCRPHO42", "MCRPHO19", "MCDHMO31", "MCDHMO42", "MCDHMO19", "MCDMC31", "MCDMC42", "MCDMC19", "PRVHMO31", 
"PRVHMO42", "PRVHMO19", "FSAGT31", "HASFSA31", "PFSAMT31", "PREVCOVR", "MORECOVR", "TRICR31X", "TRICR42X", "TRICR53X", 
"TRICR19X", "TRIAT31X", "TRIAT42X", "TRIAT53X", "TRIAT19X", "MCAID31", "MCAID42", "MCAID53", "MCAID19", "MCAID31X", 
"MCAID42X", "MCAID53X", "MCAID19X", "MCARE31", "MCARE42", "MCARE53", "MCARE19", "MCARE31X", "MCARE42X", "MCARE53X", 
"MCARE19X", "MCDAT31X", "MCDAT42X", "MCDAT53X", "MCDAT19X", "GOVTA31", "GOVTA42", "GOVTA53", "GOVTA19", "GOVAAT31", 
"GOVAAT42", "GOVAAT53", "GOVAAT19", "GOVTB31", "GOVTB42", "GOVTB53", "GOVTB19", "GOVBAT31", "GOVBAT42", "GOVBAT53", 
"GOVBAT19", "GOVTC31", "GOVTC42", "GOVTC53", "GOVTC19", "GOVCAT31", "GOVCAT42", "GOVCAT53", "GOVCAT19", "VAPROG31", 
"VAPROG42", "VAPROG53", "VAPROG19", "VAPRAT31", "VAPRAT42", "VAPRAT53", "VAPRAT19", "IHS31", "IHS42", "IHS53", 
"IHS19", "IHSAT31", "IHSAT42", "IHSAT53", "IHSAT19", "PRIDK31", "PRIDK42", "PRIDK53", "PRIDK19", "PRIEU31", 
"PRIEU42", "PRIEU53", "PRIEU19", "PRING31", "PRING42", "PRING53", "PRING19", "PRIOG31", "PRIOG42", "PRIOG53", 
"PRIOG19", "PRINEO31", "PRINEO42", "PRINEO53", "PRINEO19", "PRIEUO31", "PRIEUO42", "PRIEUO53", "PRIEUO19", "PRSTX31", 
"PRSTX42", "PRSTX53", "PRSTX19", "PRIV31", "PRIV42", "PRIV53", "PRIV19", "PRIVAT31", "PRIVAT42", "PRIVAT53", 
"PRIVAT19", "PUB31X", "PUB42X", "PUB53X", "PUB19X", "PUBAT31X", "PUBAT42X", "PUBAT53X", "PUBAT19X", "VERFLG31", 
"VERFLG42", "VERFLG19", "INS31X", "INS42X", "INS53X", "INS19X", "INSAT31X", "INSAT42X", "INSAT53X", "INSAT19X", 
"DENTIN31", "DENTIN42", "DENTIN53", "DNTINS31", "DNTINS19", "PMEDIN31", "PMEDIN42", "PMEDIN53", "PMDINS31", "PMDINS19", 
"PROBPY42", "CRFMPY42", "PYUNBL42", "PMEDUP31", "PMEDUP42", "PMEDUP53", "PMEDPY31", "PMEDPY42", "PMEDPY53", "OBTOTV19", 
"OBDRV19", "OPTOTV19", "OPDRV19", "ERTOT19", "IPDIS19", "IPNGT19", "DVTOT19", "HHTOTD19", "HHAGD19", "HHINDD19", 
"HHINFD19", "PERWT19P", "SAQWT19P", "VARSTR", "VARPSU")


var_types <- c(
"n", "n", "c", "n", "c", "c", "c", "c", "c", "c", 
"c", "c", "c", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "c", "c", "c", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n")


var_types <- setNames(var_types, var_names)

# IMPORT ASCII file -----------------------

meps_dat <- read_fwf(                      
meps_path,                                 
     col_positions =                       
         fwf_positions(                    
             start = pos_start,            
                 end   = pos_end,          
                 col_names = var_names),   
         col_types = var_types)            

                                           
# OPTIONAL: save as .Rdata file for easier loading ----------------------------
# Run this to save a permanent .Rdata file in the local working directory      
#                                          
save(meps_dat, file = "H212R.rdata")  
                                           
# -----------------------------------------------------------------------------
# NOTES:                                       
#                                          
#  1. This program has been tested on R version 3.6.0              
#                                          
#  2. This program will create a temporary data frame in R called H212.      
#     You must run the 'save' command to permanently save the data to a local  
#     folder                                   
# -----------------------------------------------------------------------------

