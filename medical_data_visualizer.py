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

# 4 Draw the Categorical Plot
def draw_cat_plot():
    # 5 Create long-form dataframe for selected categorical variables
    cat_features = ["cholesterol", "gluc", "smoke", "alco", "active", "overweight"]
    df_cat = pd.melt(
        df,
        id_vars=["cardio"],
        value_vars=cat_features,
        var_name="variable",
        value_name="value",
    )

    # 6 Group and reformat to counts per cardio/variable/value
    df_cat = (
        df_cat.groupby(["cardio", "variable", "value"])
        .size()
        .reset_index(name="total")
    )
    
    # 7 Enforce deterministic variable order to match unit tests
    variable_order = ["active", "alco", "cholesterol", "gluc", "overweight", "smoke"]
    df_cat["variable"] = pd.Categorical(
        df_cat["variable"], categories=variable_order, ordered=True
    )

    # Create the categorical bar plot faceted by cardio
    g = sns.catplot(
        data=df_cat,
        x="variable",
        y="total",
        hue="value",
        col="cardio",
        kind="bar"
    )
    g.set_axis_labels("variable", "total")

    # 8 Grab the figure handle
    fig = g.fig

    # 9 Persist plot and return figure
    fig.savefig("catplot.png")
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
