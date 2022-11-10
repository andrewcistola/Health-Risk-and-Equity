# -----------------------------------------------------------------------------             
# R programming statements for h220G data                                              
#                                                                                           
# This file contains programming statements needed to import the ASCII data                 
# file (.dat) into R. The R programming language has the capability to produce              
# appropriate standard errors for estimates from a survey with a complex sample             
# design such as the Medical Expenditure Panel Survey (MEPS).                               
#                                                       
# The input file is the ASCII data file (h220G.dat) supplied in this PUF                
# release, which can be extracted from the .zip file supplied at the MEPS                   
# website: https://meps.ahrq.gov/mepsweb/data_stats/download_data_files.jsp                 
#                                                       
# This code imports the MEPS data into R as a data frame called 'h220G'.            
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
#         of the h220G.dat file.)                                   
#                                                       
#     meps_path <- "C:/MEPS/h220G.dat"                             
#     source("https://meps.ahrq.gov/mepsweb/data_stats/download_data/pufs/h220G/h220Gru.txt")
#     head(h220G) # view data                                       
#                                                       
#  (b) Alternatively, the ASCII (.dat) file can be downloaded directly from                 
#         the MEPS website. The following code can be used to download and                  
#         import the h220G data into R without having to manually download,             
#         unzip, and store the file on your local computer.                         
#                                                       
#           url <- "https://meps.ahrq.gov/mepsweb/data_files/pufs/h220Gdat.zip" 
#           download.file(url, temp <- tempfile())                              
#                                                       
#     meps_path <- unzip(temp, exdir = tempdir())                               
#     source("https://meps.ahrq.gov/mepsweb/data_stats/download_data/pufs/h220G/h220Gru.txt")
#                                                       
#           unlink(temp)  # Unlink to delete temporary file                         
#                                                       
#           head(h220G) # view data                                 
#                                                       
# -----------------------------------------------------------------------------             
                                                        
# DEFINE 'meps_path' -----------------------------------------------------------            
# 'meps_path' should point to the file path of the ASCII file (h220G.dat)               
# Here, the 'exists' function checks whether meps_path is already defined. This             
# feature is useful if calling this file from an external source.                           
if(!exists("meps_path"))  meps_path = "C:/MEPS/h220G.dat"      

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
1, 8, 11, 21, 37, 38, 52, 54, 55, 56, 
60, 62, 64, 66, 68, 70, 73, 75, 77, 79, 
81, 83, 85, 87, 89, 91, 94, 96, 99, 101, 
104, 107, 115, 123, 131, 140, 148, 155, 162, 169, 
178, 186, 195, 204, 205, 218, 222)


pos_end <- c(
7, 10, 20, 36, 37, 51, 53, 54, 55, 59, 
61, 63, 65, 67, 69, 72, 74, 76, 78, 80, 
82, 84, 86, 88, 90, 93, 95, 98, 100, 103, 
106, 114, 122, 130, 139, 147, 154, 161, 168, 177, 
185, 194, 203, 204, 217, 221, 222)


var_names <- c(
"DUID", "PID", "DUPERSID", "EVNTIDX", "EVENTRN", "FFEEIDX", "PANEL", "MPCELIG", "MPCDATA", "OBDATEYR", 
"OBDATEMM", "SEEDOC_M18", "DRSPLTY_M18", "MEDPTYPE_M18", "DOCATLOC", "VSTCTGRY", "VSTRELCN_M18", "LABTEST_M18", "SONOGRAM_M18", "XRAYS_M18", 
"MAMMOG_M18", "MRI_M18", "EKG_M18", "RCVVAC_M18", "SURGPROC", "MEDPRESC", "VISITTYPE", "TELEHEALTHFLAG", "FFOBTYPE", "FFBEF20", 
"FFTOT21", "OBSF20X", "OBMR20X", "OBMD20X", "OBPV20X", "OBVA20X", "OBTR20X", "OBOF20X", "OBSL20X", "OBWC20X", 
"OBOT20X", "OBXP20X", "OBTC20X", "IMPFLAG", "PERWT20F", "VARSTR", "VARPSU")


var_types <- c(
"n", "n", "c", "c", "n", "c", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n", "n", "n", "n", 
"n", "n", "n", "n", "n", "n", "n")


var_types <- setNames(var_types, var_names)

# IMPORT ASCII file -----------------------

h220G <- read_fwf(                      
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
# save(h220G, file ="h220G.Rdata")  
                                           
# -----------------------------------------------------------------------------
# NOTES:                                       
#                                          
#  1. This program has been tested on R version 3.6.0              
#                                          
#  2. This program will create a temporary data frame in R called 'h220G'.      
#     You must run the 'save' command to permanently save the data to a local  
#     folder                                   
# -----------------------------------------------------------------------------

