import pandas as pd
import numpy as np
import statsmodels.api as sm


df =


# Perform logistic regression


df['version'] = df['version'].astype('category')
df['test_number'] = df['test_number'].astype('category')

print(df)


df['count_undesired_action'] = df['sample_size'] - df['count_desired_action']


y = df[['count_desired_action','count_undesired_action']]
X = pd.get_dummies(df[['test_number','version']], drop_first=True).astype(float)
X = sm.add_constant(X)


model = sm.GLM(
    endog=y, 
    exog=X, 
    family=sm.families.Binomial()
)
results = model.fit()
print(results.summary())


coef = results.params['B']
