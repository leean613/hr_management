#!/usr/bin/env python
# coding: utf-8

# In[2]:


import glob
import os
import pandas as pd
import json

from sqlalchemy.engine import create_engine
from sqlalchemy import Table, Column, Integer, String, Date
import gzip


#Get list of filenames
path = input("Please enter a path:\n")
list_filename = []

for x in os.walk(path):
    for y in glob.glob(os.path.join(x[0], '*.gz')):
        list_filename.append(y)

#Convert .gz to dataframe        
dict_list = []
header_list = []
for filename in list_filename:
    f = gzip.open(filename, 'rt', encoding='utf-8')
    rawdata = f.readlines()
    header_list += list(json.loads((rawdata[0])).keys())
    f.close()
    
    for i in rawdata:
        dict_list.append(json.loads(i))
        
header_list = list(dict.fromkeys(header_list))
df = pd.DataFrame(dict_list, columns=header_list)

#Server info
DIALECT = 'oracle'
SQL_DRIVER = 'cx_oracle'
USERNAME = 'DEV' #enter your username
PASSWORD = 'qtdata@2021' #enter your password
HOST = '118.69.32.128' #enter the oracle db host url
PORT = 1521 #enter the oracle port number
SERVICE = 'XE' #enter the oracle db service name
ENGINE_PATH_WIN_AUTH = DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + PASSWORD +'@' + HOST +                        ':' + str(PORT) + '/?service_name=' + SERVICE
print(ENGINE_PATH_WIN_AUTH)
engine = create_engine(ENGINE_PATH_WIN_AUTH, max_identifier_length = 128)
con = engine.connect()

#Run with linkedin data
for col in df.columns:
    df[col] = df[col].str.replace("\u2019", "'")
    if (col == "education") or (col == "also_viewed"):
        df[col] = df[col].astype(str)
    else:
        df[col] = df[col].str.encode('utf-8')


# ### MEMBER_INFO DATA DEMO

# In[19]:


df_memberinfo = pd.DataFrame({
    'NAME':['Minh', 'Chau', 'Chi'],
    'EMAIL_ADDRESS': ['Minh@gmail.com', 'Chau@gmail.com', 'Chi@gmail.com'],
    'ALIAS':['Aiden Smith', 'Chau Satakunta', 'Layla Smith'],
    'TITLE':['Technology', 'HR', 'Cordinator'],
    'STATUS':['pending', 'pending', 'temp'],
    'FULLTIME_PARTIME':['full_time', 'full_time', 'full_time'],
    'TIMESTAMP':['3/4/2020', '4/4/2020', '5/4/2020'],
    'FACEBOOK':['link', 'link', 'link'],
    'CV':['linkcv1', 'linkcv2', 'linkcv3'],
    'INTRODUCER':['henry', 'henry', 'henry'],
    'STARTDAY':['07/01', '07/01', '07/01'],
    'OUTDATE':['na', 'na', 'na'],
    'MINHOUR':[40, 40, 40],
    'SALARY':[30, 30, 30],
    'WISH':['wish1', 'wish2', 'wish3'],
    'EXCEL':['good', 'good', 'good'],
    'ACTION':['action1', 'action2', 'action3'],
    'COMMENT':['comment1', 'comment2', 'comment3'],
    'STT':[1, 2, 3]
    
})


# In[13]:


#Import to Oracle SQL database
df_memberinfo.to_sql('MEMBER_INFO', engine, if_exists='append', index = False)


# In[3]:


#Check
engine.execute("SELECT * FROM MEMBER_INFO").fetchall()


# In[7]:


#pendinglist
engine.execute("SELECT * FROM MEMBER_INFO WHERE TO_CHAR(STATUS)='pending'").fetchall()


# In[10]:


#updateinfo
engine.execute("UPDATE MEMBER_INFO SET STATUS = 'temp' WHERE TO_CHAR(NAME) = 'Minh'")


# In[26]:


#newmemberlist
engine.execute("SELECT * FROM MEMBER_INFO WHERE TO_CHAR(TIMESTAMP) = TO_DATE()")


# In[ ]:




