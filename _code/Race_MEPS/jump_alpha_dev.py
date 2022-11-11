# Setup

## Libraries

### Native Python Libraries
import os # Operating system navigation
import io # Input output control
import shutil # High level file operations
import datetime # Date and time stamps
import zipfile # Compressed and archive manager in python
import urllib # Url requests with file download functions
import sqlite3 # SQLite database manager

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
import xlsxwriter # Python module for writing files in the Excel 2007+ XLSX file format (engine for pandas ExcelWriter class)

## Variables

### Label Variables
label_home = 'C://Users'
label_user = 'drewc'
label_character = 'neville'
label_project = 'Health-Risk-and-Equity'

### Import Variables
os.chdir(label_home + '//' + label_user  + '//' + label_character  + '//' + label_project) # Set wd
df = pd.read_csv('_tmp//variables.csv')
df = df.set_axis(df['Label']).drop(columns = ['Label']) # Set column as index
desc_project = df.loc['desc_project', 'Value']
desc_title = df.loc['desc_title', 'Value']
desc_author = df.loc['desc_author', 'Value']
desc_summary = df.loc['desc_summary', 'Value']
desc_reference = df.loc['desc_reference', 'Value']
desc_notes = df.loc['desc_notes', 'Value']
desc_status = df.loc['desc_status', 'Value']
desc_time = df.loc['desc_time', 'Value']
label_subject = df.loc['label_subject', 'Value']
label_version = df.loc['label_version', 'Value']
label_status = df.loc['label_status', 'Value']
label_reference = df.loc['label_reference', 'Value']
label_time = df.loc['label_time', 'Value']
label_name = df.loc['label_name', 'Value']
label_run = df.loc['label_run', 'Value']

## SQlite Database in data subrepo
db_con = sqlite3.connect('_data//' + label_name + '//' + label_run + '//database.db') # Create local database file connection object
db_cur = db_con.cursor() # Create cursor object for modidying connected database