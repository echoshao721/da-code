#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
from sklearn.ensemble import IsolationForest

# display all cols (console settings)
pd.set_option('display.max_columns', None)
# display all rows
pd.set_option('display.max_rows', None)

# 1. load dataset：detection.cvs
df = pd.read_csv('UserSessions.csv')
# print(df.head())

# 2. summary
print(df.describe())

# 3. isolation forest
model = IsolationForest()

# 4.model.fit()
model.fit(df[['visitNumber']])
# print(model.fit(df[['visitNumber']]))

# 5. scores of each data points
df['scores'] = model.decision_function(df[['visitNumber']])
df['is_inlier'] = model.predict(df[['visitNumber']])  # 1-normal 2-outlier
df = df[['visitNumber', 'scores', 'is_inlier']]

# 6. Detect outlier
outliers = df[df['is_inlier'] == -1]
print('Total Data：', len(df))
print('outlier：', len(outliers))
print('percentage of outliers', len(outliers) / len(df))
