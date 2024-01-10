#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import necessary libaries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# # Read data

# In[4]:


df = pd.read_csv('flights.txt', sep='|')


# In[5]:


pd.set_option('display.max_columns', None)


# In[6]:


df.head()


# In[7]:


df.columns


# In[8]:


new_df=df.copy()


# In[9]:


col=['AIRLINECODE', 'TAILNUM', 'FLIGHTNUM', 'ORIGAIRPORTNAME',
     'ORIGINSTATE', 'DESTAIRPORTNAME',
    'DESTSTATE', 'CRSDEPTIME', 'DEPTIME', 'TAXIOUT', 'WHEELSOFF', 
     'WHEELSON', 'TAXIIN', 'CRSARRTIME','ARRTIME', 'CRSELAPSEDTIME']


# In[10]:


#drop some columns
new_df=new_df.drop(columns=col)


# In[11]:


new_df.head()


# In[12]:


new_df.info()


# # Data cleansing

# ## Change column's data type

# In[13]:


new_df['FLIGHTDATE']=pd.to_datetime(new_df['FLIGHTDATE'], format='%Y%m%d')
new_df['FLIGHTDATE']


# ## Replace inconsistent values

# In[14]:


new_df['CANCELLED'].unique()


# In[15]:


new_df['DIVERTED'].unique()


# In[16]:


# Replace False, 0 with F, replace True, 1 with T
new_df.replace({'False':'F', 'True':'T'}, inplace=True)
new_df.replace({'CANCELLED':'0', 'DIVERTED':'0'}, 'F', inplace=True)
new_df.replace({'CANCELLED':'1', 'DIVERTED':'1'}, 'T', inplace=True)

#check CANCELLED và DIVERTED
new_df['CANCELLED'].unique()

new_df['DIVERTED'].unique()


# ## Separate numbers from units of measurement

# In[17]:


#remove units of measurement
new_df['DISTANCE']=new_df['DISTANCE'].map(lambda x: x.rstrip(' miles'))
new_df['DISTANCE']


# In[18]:


#change data type of DISTANCE
new_df['DISTANCE']=pd.to_numeric(new_df['DISTANCE'])
new_df['DISTANCE']


# ## Handle missing values

# In[19]:


new_df.info()


# the above shows that there are 5 columns that include missing value: ORIGINSTATENAME, DESTSTATENAME,DEPDELAY,ARRDELAY,ACTUALELAPSEDTIME

# ### Fill missing values in column ORIGINSTATENAME
# Each airport has only one airportcode and is in only one state. 
# So we can use the ORIGINAIRPORTCODE to fill null values in column ORIGINSTATENAME.

# In[20]:


#list all ORIGINAIRPORTCODEs of rows that have null ORIGINSTATENAMEs 
new_df.loc[new_df['ORIGINSTATENAME'].isnull(), 'ORIGINAIRPORTCODE'].unique()


# In[21]:


aircode_state_dict = {
'LAW' : 'Oklahoma', 'MHK' : 'Kansas',
'HYS' : 'Kansas', 'OKC' : 'Oklahoma',
'FOE' : 'Kansas', 'TUL' : 'Oklahoma',
'ICT' : 'Kansas', 'GCK' : 'Kansas'
}


# In[22]:


#use fillna() and map() function to deal with missing value in ORIGINSTATENAME
new_df['ORIGINSTATENAME'] = new_df['ORIGINSTATENAME'].fillna(new_df['ORIGINAIRPORTCODE'].map(aircode_state_dict))
new_df['ORIGINSTATENAME'].isnull().sum()


# ### Fill missing values in column DESTSTATENAME

# In[23]:


#list all DESTAIRPORTCODEs of rows that have null DESTSTATENAMEs 
new_df.loc[new_df['DESTSTATENAME'].isnull(), 'DESTAIRPORTCODE'].unique()


# In[24]:


aircode_deststate_dict = {
'OKC' : "Oklahoma", 'TUL' : "Oklahoma",
'ICT' : "Kansas", 'LAW' : "Oklahoma",    
'MHK' : "Kansas", 'FOE' : "Kansas",  
'GCK' : "Kansas", 'HYS' : "Kansas"
}


# In[25]:


#use fillna() and map() function to deal with missing value in DESTSTATENAME
new_df['DESTSTATENAME'] = new_df['DESTSTATENAME'].fillna(new_df['DESTAIRPORTCODE'].map(aircode_state_dict))
new_df['DESTSTATENAME'].isnull().sum()


# ### Fill missing values in column DEPDELAY

# In[26]:


#how many null values are there in DEPDELAY?
new_df['DEPDELAY'].isnull().sum()


# In[27]:


#If a flight was cancelled, then DEPDELAY time is 0
new_df.loc[new_df['CANCELLED']=='T', 'DEPDELAY']=0


# In[28]:


new_df['DEPDELAY'].isnull().sum()


# We can see that all null DEPDELAY values was caused by cancellation. Now all of them are replaced with 0. But if there is some other
# reason causing null values in DEPDELAY, we can handle with these missing values as follows:

# In[29]:


#Replace the rest of null DEPDELAY values with the mean values of the corresponding airlines
depDelay_dict = new_df.groupby('AIRLINENAME')['AIRLINENAME','DEPDELAY'].mean().round(2).to_dict()['DEPDELAY']
depDelay_dict


# In[30]:


new_df['DEPDELAY']=new_df['DEPDELAY'].fillna(new_df['AIRLINENAME'].map(depDelay_dict))


# ### Fill missing values in column ARRDELAY
# Replace null ARRDELAY values with the mean values of ARRDELAY of the corresponding airlines

# In[31]:


#how many null values are there in ARRDELAY?
new_df['ARRDELAY'].isnull().sum()


# In[32]:


#If a flight was cancelled, then ARRDELAY time is 0
new_df.loc[new_df['CANCELLED']=='T', 'ARRDELAY']=0


# In[33]:


new_df['ARRDELAY'].isnull().sum()


# In[34]:


#Replace null ARRDELAY values with the mean values of ARRDELAY of the corresponding airlines
arrDelay_dict = new_df.groupby('AIRLINENAME')['AIRLINENAME','ARRDELAY'].mean().round(2).to_dict()['ARRDELAY']
arrDelay_dict


# In[35]:


new_df['ARRDELAY']=new_df['ARRDELAY'].fillna(new_df['AIRLINENAME'].map(depDelay_dict))
new_df['ARRDELAY'].isnull().sum()


# ### Fill missing values in column ACTUALELAPSEDTIME

# In[36]:


#how many null values are there in ACTUALELAPSEDTIME?
new_df['ACTUALELAPSEDTIME'].isnull().sum()


# In[37]:


#If a flight was cancelled, then ACTUALELAPSEDTIME time is 0
new_df.loc[new_df['CANCELLED']=='T', 'ACTUALELAPSEDTIME']=0


# In[38]:


new_df['ACTUALELAPSEDTIME'].isnull().sum()


# In[39]:


#Replace null ACTUALELAPSEDTIME values with the mean values of ACTUALELAPSEDTIME of the corresponding airlines
elapDelay_dict = new_df.groupby('AIRLINENAME')['AIRLINENAME','ACTUALELAPSEDTIME'].mean().round(2).to_dict()['ACTUALELAPSEDTIME']
elapDelay_dict


# In[40]:


new_df['ACTUALELAPSEDTIME']=new_df['ACTUALELAPSEDTIME'].fillna(new_df['AIRLINENAME'].map(depDelay_dict))
new_df['ACTUALELAPSEDTIME'].isnull().sum()


# In[41]:


new_df.info()


# ## Create some new columns showing the status of arrival delay and departure delay

# ### create ARRSTATUS showing the status of arrival delay

# In[42]:


new_df['ARRDELAY'].max()


# In[43]:


new_df['ARRDELAY'].min()


# In[44]:


new_df.loc[new_df['ARRDELAY'] <=15 , 'ARRSTATUS']='on time'
new_df.loc[(new_df['ARRDELAY'] > 15) & (new_df['ARRDELAY'] <=60) , 'ARRSTATUS']='a bit late'
new_df.loc[new_df['ARRDELAY'] >60, 'ARRSTATUS']='very late'
new_df.loc[(new_df['ARRDELAY'] ==0) & (new_df['CANCELLED']=='T'), 'ARRSTATUS']='cancelled'
new_df.loc[(new_df['ARRDELAY'] ==0) & (new_df['CANCELLED']=='F'), 'ARRSTATUS']='on time'


# In[45]:


new_df['ARRSTATUS'].value_counts()


# In[46]:


new_df['CANCELLED'].value_counts()


# ### create DEPSTATUS showing the status of departure delay

# In[47]:


new_df['DEPDELAY'].max()


# In[48]:


new_df['DEPDELAY'].min()


# In[49]:


new_df.loc[new_df['DEPDELAY'] <=15 , 'DEPSTATUS']='on time'
new_df.loc[(new_df['DEPDELAY'] > 15) & (new_df['DEPDELAY'] <=60) , 'DEPSTATUS']='a bit late'
new_df.loc[new_df['DEPDELAY'] >60, 'DEPSTATUS']='very late'
new_df.loc[(new_df['DEPDELAY'] ==0) & (new_df['CANCELLED']=='T'), 'DEPSTATUS']='cancelled'
new_df.loc[(new_df['DEPDELAY'] ==0) & (new_df['CANCELLED']=='F'), 'DEPSTATUS']='on time'


# In[50]:


new_df['DEPSTATUS'].value_counts()


# ## Explore data

# In[51]:


new_df.head()


# In[52]:


#number of flights per year

flight_year=df.groupby(new_df['FLIGHTDATE'].dt.year)['TRANSACTIONID'].agg('count').reset_index()
flight_year.rename(columns={'TRANSACTIONID': "NUMBEROFPFLIGHT"}, inplace=True)


# In[53]:


flight_year


# In[54]:


#number of flights per month
flight_month=new_df.groupby(new_df['FLIGHTDATE'].dt.month)['TRANSACTIONID'].agg('count').reset_index()
flight_month.rename(columns={'TRANSACTIONID': "NUMBEROFPFLIGHT"}, inplace=True)


# In[55]:


flight_month


# In[56]:


fig, (ax1, ax2)=plt.subplots(figsize=(12, 6), nrows=1, ncols=2)
ax1.plot(flight_year['FLIGHTDATE'], flight_year['NUMBEROFPFLIGHT'])
ax1.set(xlabel='Year', ylabel='Number of Flight')

ax2.pie(flight_month['NUMBEROFPFLIGHT'], labels=['JAN', 'May', 'SEP'], autopct='%.2f%%')
ax2.set(title='Number of flights per month');


# In[57]:


#Number of flights, ACTUALELAPSEDTIME, DISTANCE per airline
df1=new_df.groupby('AIRLINENAME')['TRANSACTIONID'].agg('count').reset_index()
df1.rename(columns={'TRANSACTIONID': "NUMBEROFPFLIGHTs"}, inplace=True)
df2=new_df.groupby('AIRLINENAME')['ACTUALELAPSEDTIME'].agg('sum').reset_index()
df3=new_df.groupby('AIRLINENAME')['DISTANCE'].agg('sum').reset_index()

df4=pd.merge(df1, df2, on='AIRLINENAME')
flight_airline=pd.merge(df3, df4, on='AIRLINENAME')


# In[58]:


flight_airline.sort_values(by='NUMBEROFPFLIGHTs').set_index('AIRLINENAME')


# In[59]:


#number of flights per original state
flight_state=new_df.groupby('ORIGINSTATENAME')['TRANSACTIONID'].agg('count').reset_index()
flight_state.rename(columns={'TRANSACTIONID': "NUMBEROFPFLIGHTs"}, inplace=True)
flight_state


# In[60]:


plt.figure(figsize=(14, 9))
sns.barplot(data=flight_state, y='ORIGINSTATENAME', x='NUMBEROFPFLIGHTs');


# In[61]:


# arrival status and departure status
fig, (ax1, ax2)=plt.subplots(figsize=(12, 6), nrows=1, ncols=2)
ax1.plot(flight_year['FLIGHTDATE'], flight_year['NUMBEROFPFLIGHT'])
ax1.set(xlabel='Year', ylabel='Number of Flight')

ax2.pie(flight_month['NUMBEROFPFLIGHT'], labels=['JAN', 'May', 'SEP'], autopct='%.2f%%')
ax2.set(title='Number of flights per month');


# In[62]:


arrival_status=new_df.groupby('ARRSTATUS')['TRANSACTIONID'].agg('count').reset_index()
arrival_status.rename(columns={'TRANSACTIONID':'count'}, inplace=True)
arrival_status


# In[63]:


departure_status=new_df.groupby('DEPSTATUS')['TRANSACTIONID'].agg('count').reset_index()
departure_status.rename(columns={'TRANSACTIONID':'count'}, inplace=True)
departure_status


# In[64]:


fig, (ax1, ax2)=plt.subplots(figsize=(12, 6), nrows=1, ncols=2)
ax1.pie(departure_status['count'], labels=list(departure_status['DEPSTATUS']), autopct='%.2f%%', explode=[0.0, 0.2, 0.0, 0.0])
ax1.set(title='Departure Status')

ax2.pie(arrival_status['count'], labels=list(arrival_status['ARRSTATUS']), autopct='%.2f%%', explode=[0.0, 0.2, 0.1, 0.0])
ax2.set(title='Arrival Status');


# In[ ]:





# In[ ]:




