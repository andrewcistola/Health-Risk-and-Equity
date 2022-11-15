# Setup

## Libraries

### Native Python Libraries
import sys # Python version
import os # Operating system navigation
import io # Input output control
import shutil # High level file operations
import datetime # Date and time stamps
import zipfile # Compressed and archive manager in python
import urllib # Url requests with file download functions
import sqlite3 # SQLite database manager
import Python-Markdown

### Data Science Basics
import numpy as np # Widely used matrix library for numerical processes
import pandas as pd # Widely used data manipulation library with R/Excel like tables named 'data frames'
import scipy.stats as st # Statistics package best for t-test, ChiSq, correlation
import statsmodels.api as sm # Statistics package best for regression models
import matplotlib.pyplot as plt # Comprehensive graphing package in python
import geopandas as gp # Simple mapping library for csv shape files with pandas like syntax for creating plots using matplotlib 

### Scikit-learn
from sklearn.preprocessing import StandardScaler # Standard scaling for easier use of machine learning algorithms
from sklearn.impute import SimpleImputer # Univariate imputation for missing data
from sklearn.decomposition import PCA # Principal compnents analysis from sklearn
from sklearn.ensemble import RandomForestRegressor # Random Forest regression component
from sklearn.ensemble import RandomForestClassifier # Random Forest classification component
from sklearn.feature_selection import RFECV # Recursive Feature elimination with cross validation
from sklearn.svm import LinearSVC # Linear Support Vector Classification from sklearn
from sklearn.svm import LinearSVR # Linear Support Vector Regression from sklearn
from sklearn.linear_model import LinearRegression # Used for machine learning with quantitative outcome
from sklearn.linear_model import LogisticRegression # Used for machine learning with quantitative outcome
from sklearn.cluster import KMeans # unsupervised clustering using k-means
from sklearn.model_selection import train_test_split # train test split function for validation
from sklearn.metrics import roc_curve # Reciever operator curve
from sklearn.metrics import auc # Area under the curve 

### keras API for TensorFlow
from tensorflow import keras # keras PAI for using TensorFlow to build deep learening models in python
from keras.models import Sequential # Uses a simple method for building layers in MLPs
from keras.models import Model # Uses a more complex method for building layers in deeper networks
from keras.layers import Dense # Used for creating dense fully connected layers
from keras.layers import Input # Used for designating input layers

### Other Tools
import openpyxl # Engine for accessing .xlsx files from pandas

## Variables

### Descriptive Variables
desc_project = 'Health, Risk, and Equity'
desc_title = 'Risk Heterogeneity between Black and White Individuals Insured through the ACA Marketplaces from 2018-2020'
desc_author = 'Andrew S. Cistola, MPH'
desc_summary = 'Previous research have shown signficiant under-utilization of ambulatory care and signficiantly lower costs among black insured individuals 18-64 from 2014-2018. (doi:10.1001/jamanetworkopen.2022.17383) If these differences persist through the ACA risk adjustment program, under-utilization represents an arbitrage opportunity for insurance providers in the individual market. This would represent how a history of systematic racism and barriers to care could be used for cost-containment measures with the beenfits of overall lower health care costs transferred among the larger population. Health equity efforts should be focused on neutralizing arbitrage opporunties based on defacto discrimination and instead incentivize issuers to address disparities in access to care. With the addition of race and zip code to the EDGE server in 2025, CMS will have the ability to reform the ACA risk adjustmenr program to improve these disparities. The purpose of this study is to identify how the ACA Risk Adjustment program interacts with known health disparities in health care utilization among raical groups. This study uses publcily available data from the Medical Expenditure Panel Survey (MEPS) from Agency for Healthcare Research and Quality (AHRQ) (https://meps.ahrq.gov/mepsweb/data_stats/download_data_files.jsp) from 2018 to 2021 to identify differences in risk that can be attributed to racial group independent of other factors and whether the ACA risk adjustment program excacerbates these diferences. Evidence from this study can identify how racial data can be used by CMS to promote health equity within the ACA marketplaces.'
desc_reference = 'github.com/andrewcistola/Health-Risk-and_Equity'
desc_notes = 'This analysis serves to fulfill part of the the requirements for the PhD in Public Health-Heath Services Research at the University of Florida. The author is also employed by Blue Cross Blue Shield of Florida.'
desc_status = 'In development'
desc_time = str(datetime.datetime.now())

### Label Variables
label_home = 'C://Users'
label_user = 'drewc'
label_character = 'neville'
label_project = 'Health-Risk-and-Equity'
label_topic = 'Race'
label_subject = 'MEPS'
label_version = 'alpha'
label_status = 'dev'
label_reference = 'https://github.com/andrewcistola/Health-Risk-and_Equity.git'
label_dir = label_home + '//' + label_user + '//' + label_character + '//' + label_project + '//'
label_time = str(datetime.datetime.now()).replace('-', '').replace(' ', '').replace(':', '').split('.')[0]
label_name = label_topic + '_' + label_subject
label_run = label_version + '_' + label_status + '_' + label_time

## Repository

### Directories
os.chdir(label_dir) # Set wd
os.mkdir('_data//' + label_name)
os.mkdir('_data//' + label_name + '//' + label_run)
os.mkdir('_docs//' + label_name)
os.mkdir('_docs//' + label_name + '//' + label_run)
os.mkdir('_fig//' + label_name)
os.mkdir('_fig//' + label_name + '//' + label_run)

## Files

### Variable List in tmp subrepo
df = pd.DataFrame(data = {
    'Label': [ 
        'desc_project' 
        ,'desc_title'
        ,'desc_author'
        ,'desc_summary'
        ,'desc_reference'
        ,'desc_notes'
        ,'desc_status'
        ,'desc_time'
        ,'label_home'
        ,'label_user'
        ,'label_character'
        ,'label_project'
        ,'label_topic'
        ,'label_subject'
        ,'label_version'
        ,'label_status'
        ,'label_reference'
        ,'label_dir'
        ,'label_time'
        ,'label_name'
        ,'label_run'
        ]
    , 'Value': [ 
        str(desc_project)
        , str(desc_title)
        , str(desc_author)
        , str(desc_summary)
        , str(desc_reference)
        , str(desc_notes)
        , str(desc_status)
        , str(desc_time)
        , str(label_home)
        , str(label_user)
        , str(label_character)
        , str(label_project)
        , str(label_topic)
        , str(label_subject)
        , str(label_version)
        , str(label_status)
        , str(label_reference)
        , str(label_dir)
        , str(label_time)
        , str(label_name)
        , str(label_run)
        ]
     })
df.to_csv('_tmp//variables.csv', index = False)

## SQlite Database in data subrepo
db_con = sqlite3.connect('_data//' + label_name + '//' + label_run + '//database.db') # Create local database file connection object
db_cur = db_con.cursor() # Create cursor object for modidying connected database

### Markdown Summary in docs subrepo
text_md = open('_docs//' + label_name + '//' + label_run + '//summary.md', 'w')
text_md.write('# ' + desc_project + '\n')
text_md.write('#### ' + desc_title + '\n')
text_md.write('### ' + desc_author + '\n')
text_md.write('\n')
text_md.write('### ' + 'About' + '\n')
text_md.write(desc_summary + '\n')
text_md.write('\n')
text_md.write('#### ' + 'Notes:' + '\n')
text_md.write(desc_notes + '\n')
text_md.write('\n')
text_md.write('#### ' + 'Status: ' + '\n')
text_md.write(desc_status + '\n') 
text_md.write('\n')
text_md.write('#### ' + 'Reference: ' + '\n')
text_md.write(desc_reference + '\n') 
text_md.write('\n')
text_md.write('#### ' + 'Updated:' + '\n')
text_md.write(desc_time + '\n')
text_md.write('\n')
text_md.close()

### Results Workbook in figs subrepo
df = pd.DataFrame(data = {
    'Info':             ['Project',     'Author',       'Summary',      'Reference',    'Notes',        'Updated']
    , 'Descriptive':    [desc_project,  desc_author,    desc_summary,   desc_reference, desc_notes,     desc_time]
     })
with pd.ExcelWriter('_fig//' + label_name + '//' + label_run + '//results.xlsx', mode = 'w', engine = 'openpyxl') as writer:
    df.to_excel(writer, sheet_name = 'Info', index = False)