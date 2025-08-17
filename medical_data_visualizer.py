import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv("medical_examination.csv")

# 2 Add a binary overweight indicator based on BMI (>25 considered overweight)
#   BMI uses metric units: kg / (m^2); height is provided in centimeters in the dataset.
_height_m = df["height"] / 100
_bmi = df["weight"] / (_height_m ** 2)
df["overweight"] = (_bmi > 25).astype(int)

# 3 Normalize markers so 0=good, 1=bad (1->0, >1->1)
for _col in ["cholesterol", "gluc"]:
    df[_col] = (df[_col] > 1).astype(int)

# 4
def draw_cat_plot():
    # 5
    df_cat = None

    # 6
    df_cat = None
    
    # 7

    # 8
    fig = None

    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    df_heat = None

    # 12
    corr = None

    # 13
    mask = None

    # 14
    fig, ax = None

    # 15

    # 16
    fig.savefig('heatmap.png')
    return fig
