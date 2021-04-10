#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Load the dataset
data = pd.read_csv("ABtest_actions.csv")
# print(data)

# 2. summary stats about the dataset
# how many records：8188
size = len(data)
# print("e：", size)
# users (unique)：6328
user_size = len(data['id'].drop_duplicates())
# print("Users：", user_size)
# Test time：115（4 months）
days = pd.to_datetime(data['timestamp'].tail(1).values) \
       - pd.to_datetime(data['timestamp'].head(1).values)
# print("Test time(days)", days)

# 3. CTR(Click-through rate) = click users / total impressions）

# Model A：（control group）
control_group = data.query('group=="control"')
# print(control_group)
control_click = control_group.query('action=="click"')['id'].nunique()
control_view = control_group.query('action=="view"')['id'].nunique()
control_ctr = control_click / control_view

# Model B：（experiment)
experiment_group = data.query('group=="experiment"')
# print(control_group)
experiment_click = experiment_group.query('action=="click"')['id'].nunique()
experiment_view = experiment_group.query('action=="view"')['id'].nunique()
experiment_ctr = experiment_click / experiment_view

# Model A CTR vs Model B CTR
# print("control group-CTR：", control_ctr)
# print("experiment-CTR：", experiment_ctr)
diff_ctr = experiment_ctr - control_ctr
# print("CTR difference：",diff_ctr )  # H1-H0>0，reject H0

# 4. p-value < 0.05
# 4.1 random sampling, perform 10,000 AB test
diffs = []
for _ in range(10000):
    sample = data.sample(size, replace=True)

    control_group = sample.query('group=="control"')
    control_click = control_group.query('action=="click"')['id'].nunique()
    control_view = control_group.query('action=="view"')['id'].nunique()
    control_ctr = control_click / control_view

    experiment_group = sample.query('group=="experiment"')
    experiment_click = experiment_group.query('action=="click"')['id'].nunique()
    experiment_view = experiment_group.query('action=="view"')['id'].nunique()
    experiment_ctr = experiment_click / experiment_view

    diff = experiment_ctr - control_ctr
    diffs.append(diff)

# print(diffs)
diffs = np.array(diffs)
# plt.hist(diffs)
# plt.show()

# 4.2 diffs -> Normal Distribution
normalize_list = np.random.normal(0, diffs.std(), size)
# plt.hist(normalize_list)
# plt.axvline(x=diff_ctr, color="red")
# plt.show()

# 4.3 p value<0.05
p_value = (normalize_list > diff_ctr).mean()
print("p-value：", p_value)
print("p <0.05?:", p_value < 0.05)
