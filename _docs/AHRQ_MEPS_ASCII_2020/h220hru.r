# -----------------------------------------------------------------------------             
# R programming statements for h220H data                                              
#                                                                                           
# This file contains programming statements needed to import the ASCII data                 
# file (.dat) into R. The R programming language has the capability to produce              
# appropriate standard errors for estimates from a survey with a complex sample             
# design such as the Medical Expenditure Panel Survey (MEPS).                               
#                                                       
# The input file is the ASCII data file (h220H.dat) supplied in this PUF                
# release, which can be extracted from the .zip file supplied at the MEPS                   
# website: https://meps.ahrq.gov/mepsweb/data_stats/download_data_files.jsp                 
#                                                       
# This code imports the MEPS data into R as a data frame called 'h220H'.            
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
#         of the h220H.dat file.)                                   
#                                                       
#     meps_path <- "C:/MEPS/h220H.dat"                             
#     source("https://meps.ahrq.gov/mepsweb/data_stats/download_data/pufs/h220H/h220Hru.txt")
#     head(h220H) # view data                                       
#                                                       
#  (b) Alternatively, the ASCII (.dat) file can be downloaded directly from                 
#         the MEPS website. The following code can be used to download and                  
#         import the h220H data into R without having to manually download,             
#         unzip, and store the file on your local computer.                         
#                                                       
#           url <- "https://meps.ahrq.gov/mepsweb/data_files/pufs/h220Hdat.zip" 
#           download.file(url, temp <- tempfile())                              
#                                                       
#     meps_path <- unzip(temp, exdir = tempdir())                               
#     source("https://meps.ahrq.gov/mepsweb/data_stats/download_data/pufs/h220H/h220Hru.txt")
#                                                       
#           unlink(temp)  # Unlink to delete temporary file                         
#                                                       
#           head(h220H) # view data                                 
#                                                       
# -----------------------------------------------------------------------------             
                                                        
# DEFINE 'meps_path' -----------------------------------------------------------            
# 'meps_path' should point to the file path of the ASCII file (h220H.dat)               
# Here, the 'exists' function checks whether meps_path is already defined. This             
# feature is useful if calling this file from an external source.                           
if(!exists("meps_path"))  meps_path = "C:/MEPS/h220H.dat"      

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
1, 8, 11, 21, 37, 38, 40, 44, 46, 47, 
49, 50, 52, 54, 56, 58, 60, 62, 64, 66, 
68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 
88, 90, 92, 94, 96, 99, 107, 115, 123, 130, 
137, 144, 151, 159, 166, 173, 181, 189, 190, 202, 
206)


pos_end <- c(
7, 10, 20, 36, 37, 39, 43, 45, 46, 48, 
49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 
69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 
89, 91, 93, 95, 98, 106, 114, 122, 129, 136, 
143, 150, 158, 165, 172, 180, 188, 189, 201, 205, 
206)


var_names <- c(
"DUID", "PID", "DUPERSID", "EVNTIDX", "EVENTRN", "PANEL", "HHDATEYR", "HHDATEMM", "MPCELIG", "SELFAGEN", 
"HHTYPE", "CNA_M18", "DIETICN_M18", "IVTHP_M18", "MEDLDOC_M18", "NURPRACT_M18", "OCCUPTHP_M18", "PHYSLTHP_M18", "RESPTHP_M18", "SOCIALW_M18", 
"SPEECTHP_M18", "HCARWRKRPROFNONE_M18", "COMPANN_M18", "HMEMAKER_M18", "HHAIDE_M18", "HOSPICE_M18", "NURAIDE_M18", "PERSONAL_M18", "HCARWRKRNONPROFNONE_M18", "VSTRELCN", 
"FREQCY", "DAYSPWK", "DAYSPMO", "SAMESVCE_M18", "HHDAYS", "HHSF20X", "HHMR20X", "HHMD20X", "HHPV20X", "HHVA20X", 
"HHTR20X", "HHOF20X", "HHSL20X", "HHWC20X", "HHOT20X", "HHXP20X", "HHTC20X", "IMPFLAG", "PERWT20F", "VARSTR", 
"VARPSU")


var_types <- c(
"n", "n", "c", "c", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n")


var_types <- setNames(var_types, var_names)

# IMPORT ASCII file -----------------------

h220H <- read_fwf(                      
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
# save(h220H, file ="h220H.Rdata")  
                                           
# -----------------------------------------------------------------------------
# NOTES:                                       
#                                          
#  1. This program has been tested on R version 3.6.0              
#                                          
#  2. This program will create a temporary data frame in R called 'h220H'.      
#     You must run the 'save' command to permanently save the data to a local  
#     folder                                   
# -----------------------------------------------------------------------------

