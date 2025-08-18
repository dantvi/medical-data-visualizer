#!/usr/bin/env python
# coding: utf-8

# # Medical Data Visualizer
# 
# This notebook demonstrates step by step how the data from **`medical_examination.csv`** is processed and visualized. The goal is to explore the relationships between cardiovascular disease and different health/lifestyle factors using **pandas**, **matplotlib** and **seaborn**.
# 
# We will:
# - Import and inspect the dataset
# - Prepare and normalize the data (BMI, cholesterol, glucose, etc.)
# - Create categorical plots to compare risk factors
# - Generate a heatmap to show correlations between measurements

# In[10]:


import medical_data_visualizer as mdv
mdv.df.head()


# ## Overweight indicator

# In[11]:


# Sanity check: overweight column should exist and contain only 0/1
mdv.df["overweight"].value_counts(dropna=False)


# In[12]:


# Spot-check BMI calculations vs overweight flag
tmp = mdv.df.assign(
    height_m = mdv.df.height / 100,
    bmi = mdv.df.weight / ( (mdv.df.height/100) ** 2 )
)[["height", "weight", "bmi", "overweight"]]

tmp.head(10)


# In[13]:


# Quick statistical summary of BMI and overweight
mdv.df.assign(
    bmi = mdv.df.weight / ( (mdv.df.height/100) ** 2 )
)[["height", "weight", "bmi", "overweight"]].describe(include="all")


# ## Normalize cholesterol and gluc

# In[14]:


# Quick schema + dtype checks
mdv.df[["cholesterol","gluc","overweight"]].dtypes


# In[15]:


# Domain checks (0/1 only)
mdv.df[["cholesterol","gluc"]].agg(["min","max","nunique"])


# In[16]:


# Distribution sanity
mdv.df["cholesterol"].value_counts(normalize=True).sort_index(), \
mdv.df["gluc"].value_counts(normalize=True).sort_index()


# In[17]:


# Spot-check mapping against raw values
import pandas as pd
raw = pd.read_csv("medical_examination.csv")[["cholesterol","gluc"]].rename(columns={"cholesterol":"chol_raw","gluc":"gluc_raw"})
check = mdv.df[["cholesterol","gluc"]].rename(columns={"cholesterol":"chol_norm","gluc":"gluc_norm"}).join(raw)
check.assign(
    chol_expected = (check["chol_raw"] > 1).astype(int),
    gluc_expected = (check["gluc_raw"] > 1).astype(int),
).head(10)


# ## Categorical Plot

# In[20]:


# Call draw_cat_plot and show the figure
from IPython.display import display
fig = mdv.draw_cat_plot()
display(fig)


# In[ ]:


# Inspect axes labels
ax = fig.axes[0]
ax.get_xlabel(), ax.get_ylabel()

# Inspect x-axis tick labels (should match expected order)
[label.get_text() for label in ax.get_xticklabels()]

# Count number of bars drawn
import matplotlib as mpl
len([rect for rect in ax.get_children() if isinstance(rect, mpl.patches.Rectangle)])


# In[ ]:




