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

# In[13]:


import medical_data_visualizer as mdv
mdv.df.head()


# ## Overweight indicator

# In[14]:


# Sanity check: overweight column should exist and contain only 0/1
mdv.df["overweight"].value_counts(dropna=False)


# In[15]:


# Spot-check BMI calculations vs overweight flag
tmp = mdv.df.assign(
    height_m = mdv.df.height / 100,
    bmi = mdv.df.weight / ( (mdv.df.height/100) ** 2 )
)[["height", "weight", "bmi", "overweight"]]

tmp.head(10)


# In[16]:


# Quick statistical summary of BMI and overweight
mdv.df.assign(
    bmi = mdv.df.weight / ( (mdv.df.height/100) ** 2 )
)[["height", "weight", "bmi", "overweight"]].describe(include="all")


# ## Normalize cholesterol and gluc

# In[17]:


# Quick schema + dtype checks
mdv.df[["cholesterol","gluc","overweight"]].dtypes


# In[18]:


# Domain checks (0/1 only)
mdv.df[["cholesterol","gluc"]].agg(["min","max","nunique"])


# In[19]:


# Distribution sanity
mdv.df["cholesterol"].value_counts(normalize=True).sort_index(), \
mdv.df["gluc"].value_counts(normalize=True).sort_index()


# In[20]:


# Spot-check mapping against raw values
import pandas as pd
raw = pd.read_csv("medical_examination.csv")[["cholesterol","gluc"]].rename(columns={"cholesterol":"chol_raw","gluc":"gluc_raw"})
check = mdv.df[["cholesterol","gluc"]].rename(columns={"cholesterol":"chol_norm","gluc":"gluc_norm"}).join(raw)
check.assign(
    chol_expected = (check["chol_raw"] > 1).astype(int),
    gluc_expected = (check["gluc_raw"] > 1).astype(int),
).head(10)


# ## Categorical Plot

# In[21]:


# Call draw_cat_plot and show the figure
from IPython.display import display
import matplotlib.pyplot as plt

fig = mdv.draw_cat_plot()
display(fig)
plt.close(fig)


# In[22]:


# Inspect axes labels
ax = fig.axes[0]
ax.get_xlabel(), ax.get_ylabel()

# Inspect x-axis tick labels (should match expected order)
[label.get_text() for label in ax.get_xticklabels()]

# Count number of bars drawn
import matplotlib as mpl
len([rect for rect in ax.get_children() if isinstance(rect, mpl.patches.Rectangle)])


# ## Heat Map

# In[23]:


import pandas as pd, numpy as np, importlib, medical_data_visualizer as mdv
mdv = importlib.reload(mdv)

# Recompute cleaning inline for inspection (mirrors mdv.draw_heat_map)
df_heat = mdv.df[mdv.df["ap_lo"] <= mdv.df["ap_hi"]].copy()
h_low, h_high = df_heat["height"].quantile([0.025, 0.975])
w_low, w_high = df_heat["weight"].quantile([0.025, 0.975])
df_heat = df_heat[
    df_heat["height"].between(h_low, h_high) & df_heat["weight"].between(w_low, w_high)
].copy()

df_shape_before = mdv.df.shape
df_shape_after  = df_heat.shape
bad_bp          = (~(df_heat["ap_lo"] <= df_heat["ap_hi"])).sum()
(df_shape_before, df_shape_after, bad_bp, (h_low, h_high), (w_low, w_high))


# In[24]:


# Corr & mask
corr = df_heat.corr(numeric_only=True)
mask = np.triu(np.ones_like(corr, dtype=bool))
corr.shape, mask.shape, mask.dtype, int(mask.sum())


# In[25]:


# Render once
from IPython.display import display
import matplotlib.pyplot as plt

fig = mdv.draw_heat_map()
display(fig)
plt.close(fig)


# In[26]:


# Label & annotation sanity
ax = fig.axes[0]
xticks = [t.get_text() for t in ax.get_xticklabels()]
yticks = [t.get_text() for t in ax.get_yticklabels()]
has_text = any(hasattr(artist, "get_text") and artist.get_text() for artist in ax.get_children())

xticks, yticks[:5], has_text


# In[27]:


# Check label matching FCC’s expected order
expected_labels = ['id','age','sex','height','weight','ap_hi','ap_lo','cholesterol','gluc','smoke','alco','active','cardio','overweight']
xticks == expected_labels

