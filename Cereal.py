#!/usr/bin/env python
# coding: utf-8

# In[26]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[27]:


#load dữ liệu
cereal_df = pd.read_csv('https://raw.githubusercontent.com/CodexploreRepo/data-science/main/Code/A6_Seaborn/data/cereal.csv')


# In[28]:


#xem 5 dòng đầu tiên của data frame
cereal_df.head()


# In[29]:


#Xem một số thông số thống kê
cereal_df.describe()
# bảng thống kê này cho thấy một số loại ngũ cốc có hàm lượng carbo, sugars, potass < 0.
# điều này không hợp lý, vì vậy ta sẽ thay hững giá trị âm này bằng 0


# In[31]:


#Thay các giá trị carbo <0 bằng 0
for x in cereal_df.index:
    if cereal_df.loc[x, 'carbo'] <0:
        cereal_df.loc[x, 'carbo']=0
#xem min của carbo:
cereal_df['carbo'].min()


# In[32]:


#Thay các giá trị sugars <0 bằng 0
for x in cereal_df.index:
    if cereal_df.loc[x, 'sugars'] <0:
        cereal_df.loc[x, 'sugars']=0
#xem min của sugars:
cereal_df['sugars'].min()


# In[33]:


#Thay giá trị potass < 0 bằng 0
for x in cereal_df.index:
    if cereal_df.loc[x, 'potass'] <0:
        cereal_df.loc[x, 'potass']=0
#xem min của potass:
cereal_df['potass'].min()


# In[34]:


cereal_df.info()
# cereal_df có 77 hàng, không có giá trị null, không có cột nào cần thay đổi kiểu dữ liệu


# In[45]:


# vẽ biểu đồ phân phối cho 9 loại dưỡng chất: calories, protein, fat, sodium, fiber, carbo, sugars, potass, vitamins

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = plt.subplots(figsize=(12, 12), nrows=3, ncols=3)

ax1.hist(cereal_df.calories, rwidth=0.95)
ax1.set(title='calories')

ax2.hist(cereal_df.protein, rwidth=0.95)
ax2.set(title='protein')

ax3.hist(cereal_df.fat, rwidth=0.95)
ax3.set(title='fat')

ax4.hist(cereal_df.sodium, rwidth=0.95)
ax4.set(title='sodium')

ax5.hist(cereal_df.fiber, rwidth=0.95)
ax5.set(title='fiber')

ax6.hist(cereal_df.carbo, rwidth=0.95)
ax6.set(title='carbo')

ax7.hist(cereal_df.sugars, rwidth=0.95)
ax7.set(title='sugars')

ax8.hist(cereal_df.potass, rwidth=0.95)
ax8.set(title='potass')

ax9.hist(cereal_df.vitamins, rwidth=0.95)
ax9.set(title='vitamins')


# In[47]:


#Vẽ biểu đồ heatmap thể hiện mối tương quan giữa các chất dinh dưỡng

#tính hệ số tương quan
cereal_corr = cereal_df.corr()

cereal_corr


# In[54]:


#sử dụng seaborn để vẽ biểu đồ tương quan
fig, (ax)=plt.subplots(figsize=(12,8))
sns.heatmap(cereal_corr, cmap='Blues', annot=True, fmt='.2f', vmin=-1, vmax=1, linecolor='white', linewidth= 0.5)
ax.set_title('Biểu đồ tương quan các chất dinh dưỡng trong ngũ cốc', fontsize=20);


# In[ ]:




