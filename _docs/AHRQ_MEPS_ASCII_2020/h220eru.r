# -----------------------------------------------------------------------------             
# R programming statements for h220E data                                              
#                                                                                           
# This file contains programming statements needed to import the ASCII data                 
# file (.dat) into R. The R programming language has the capability to produce              
# appropriate standard errors for estimates from a survey with a complex sample             
# design such as the Medical Expenditure Panel Survey (MEPS).                               
#                                                       
# The input file is the ASCII data file (h220E.dat) supplied in this PUF                
# release, which can be extracted from the .zip file supplied at the MEPS                   
# website: https://meps.ahrq.gov/mepsweb/data_stats/download_data_files.jsp                 
#                                                       
# This code imports the MEPS data into R as a data frame called 'h220E'.            
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
#         of the h220E.dat file.)                                   
#                                                       
#     meps_path <- "C:/MEPS/h220E.dat"                             
#     source("https://meps.ahrq.gov/mepsweb/data_stats/download_data/pufs/h220E/h220Eru.txt")
#     head(h220E) # view data                                       
#                                                       
#  (b) Alternatively, the ASCII (.dat) file can be downloaded directly from                 
#         the MEPS website. The following code can be used to download and                  
#         import the h220E data into R without having to manually download,             
#         unzip, and store the file on your local computer.                         
#                                                       
#           url <- "https://meps.ahrq.gov/mepsweb/data_files/pufs/h220Edat.zip" 
#           download.file(url, temp <- tempfile())                              
#                                                       
#     meps_path <- unzip(temp, exdir = tempdir())                               
#     source("https://meps.ahrq.gov/mepsweb/data_stats/download_data/pufs/h220E/h220Eru.txt")
#                                                       
#           unlink(temp)  # Unlink to delete temporary file                         
#                                                       
#           head(h220E) # view data                                 
#                                                       
# -----------------------------------------------------------------------------             
                                                        
# DEFINE 'meps_path' -----------------------------------------------------------            
# 'meps_path' should point to the file path of the ASCII file (h220E.dat)               
# Here, the 'exists' function checks whether meps_path is already defined. This             
# feature is useful if calling this file from an external source.                           
if(!exists("meps_path"))  meps_path = "C:/MEPS/h220E.dat"      

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
1, 8, 11, 21, 37, 38, 54, 66, 68, 69, 
73, 75, 78, 80, 82, 84, 86, 88, 90, 92, 
94, 96, 98, 100, 108, 117, 125, 133, 141, 149, 
157, 164, 171, 179, 186, 194, 202, 211, 218, 225, 
232, 239, 245, 251, 255, 261, 268, 275, 282, 290, 
291, 303, 307)


pos_end <- c(
7, 10, 20, 36, 37, 53, 65, 67, 68, 72, 
74, 77, 79, 81, 83, 85, 87, 89, 91, 93, 
95, 97, 99, 107, 116, 124, 132, 140, 148, 156, 
163, 170, 178, 185, 193, 201, 210, 217, 224, 231, 
238, 244, 250, 254, 260, 267, 274, 281, 289, 290, 
302, 306, 307)


var_names <- c(
"DUID", "PID", "DUPERSID", "EVNTIDX", "EVENTRN", "ERHEVIDX", "FFEEIDX", "PANEL", "MPCDATA", "ERDATEYR", 
"ERDATEMM", "VSTCTGRY", "VSTRELCN", "LABTEST_M18", "SONOGRAM_M18", "XRAYS_M18", "MAMMOG_M18", "MRI_M18", "EKG_M18", "RCVVAC_M18", 
"SURGPROC", "MEDPRESC", "FFERTYPE", "ERXP20X", "ERTC20X", "ERFSF20X", "ERFMR20X", "ERFMD20X", "ERFPV20X", "ERFVA20X", 
"ERFTR20X", "ERFOF20X", "ERFSL20X", "ERFWC20X", "ERFOT20X", "ERFXP20X", "ERFTC20X", "ERDSF20X", "ERDMR20X", "ERDMD20X", 
"ERDPV20X", "ERDVA20X", "ERDTR20X", "ERDOF20X", "ERDSL20X", "ERDWC20X", "ERDOT20X", "ERDXP20X", "ERDTC20X", "IMPFLAG", 
"PERWT20F", "VARSTR", "VARPSU")


var_types <- c(
"n", "n", "c", "c", "n", "c", "c", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n")


var_types <- setNames(var_types, var_names)

# IMPORT ASCII file -----------------------

h220E <- read_fwf(                      
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
# save(h220E, file ="h220E.Rdata")  
                                           
# -----------------------------------------------------------------------------
# NOTES:                                       
#                                          
#  1. This program has been tested on R version 3.6.0              
#                                          
#  2. This program will create a temporary data frame in R called 'h220E'.      
#     You must run the 'save' command to permanently save the data to a local  
#     folder                                   
# -----------------------------------------------------------------------------

