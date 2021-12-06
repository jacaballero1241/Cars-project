import pandas as pd 
import numpy as np
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
multicollinearity_limit = 7.5
import seaborn as sns


def vif_calculation(table, dependent):
    vif = pd.DataFrame()
    vif['variables'] = table.loc[:, table.columns != dependent].columns
    vif[dependent] = [variance_inflation_factor(table.loc[:, table.columns != dependent].values, i)\
                  for i in range(table.loc[:, table.columns != dependent].shape[1])]
    vif.append({dependent: np.nan}, ignore_index=True)
    vif = vif.set_index(['variables'])
    vif = vif.reindex(table.columns)
    vif = vif.reset_index().rename(columns={'index':'independent',
                                             dependent:'vif'})
    vif['dependent']=dependent
    vif = vif.reindex(sorted(vif.columns), axis=1)
    return vif


def strength_and_relevance_calculation(table,dependent):
    results = sm.OLS(table[dependent],table.loc[:, table.columns != dependent]).fit()
    means = table.mean()
    relevance = pd.concat([results.params,means], axis=1)
    relevance.columns = ['coef','means']
    relevance['relevance_amount']=relevance['coef']*relevance['means']
    relevance['relevance_amount_abs']=relevance['relevance_amount'].abs()
    relevance['relevance']=relevance['relevance_amount_abs']/relevance['relevance_amount_abs'].sum()
    relevance['coef'][relevance['coef'] >= 0] = 1
    relevance['coef'][relevance['coef'] < 0] = 0
    strength_relevance = pd.concat([relevance,results.pvalues], axis=1).rename(columns={0:'pvalues',
                                                                            'coef':'positive_direction'})
    strength_relevance = strength_relevance[['positive_direction','relevance','pvalues']]
    strength_relevance = strength_relevance.reindex(table.columns)
    strength_relevance = strength_relevance.reset_index().rename(columns={'index':'independent'})
    strength_relevance['dependent']=dependent
    strength_relevance = strength_relevance.reindex(sorted(strength_relevance.columns), axis=1)
    return strength_relevance


def find_final_model_variables(table,dependent):
    max_pvalue=1
    independent_variables=list(table.loc[:,table.columns != dependent].columns)
    while max_pvalue>0.01:
        results = sm.OLS(table[dependent],table.loc[:,independent_variables]).fit()
        d_pvalues=dict(results.pvalues)
        max_pvalue_key = max(d_pvalues, key=d_pvalues.get)
        max_pvalue=d_pvalues.get(max(d_pvalues, key=d_pvalues.get))
        independent_variables.remove(max_pvalue_key)
    results = sm.OLS(table[dependent],table.loc[:,independent_variables]).fit()
    rsquared_adj = results.rsquared_adj
    final_model_variables = pd.DataFrame(independent_variables)
    final_model_variables['dependent']=dependent
    final_model_variables['final_model_variable']=True
    final_model_variables['rsquared_adj'] = rsquared_adj
    final_model_variables.rename(columns={0:'independent'},inplace=True)
    final_model_variables = final_model_variables.reindex(columns=\
                                        ['dependent','independent','final_model_variable','rsquared_adj'])
    return final_model_variables


df = pd.read_csv(r'C:\Users\Usuario\Desktop\cars_ds_final_2021_tidy.csv').iloc[: , 1:]
final_table = pd.DataFrame()

for column in df.columns:
    final_table = pd.concat([final_table,vif_calculation(df, column)])
final_table.reset_index(drop=True,inplace=True)

strength_relevance_final = pd.DataFrame()
for column in df.columns:
    strength_relevance_final = pd.concat([strength_relevance_final,\
                                          strength_and_relevance_calculation(df, column)])
strength_relevance_final.reset_index(drop=True,inplace=True)
final_table = final_table.merge(strength_relevance_final,on=['dependent','independent'])

final_model_variables_grouped=pd.DataFrame()
for column in df.columns:
    final_model_variables_grouped = pd.concat([final_model_variables_grouped,\
                                               find_final_model_variables(df,column)])
final_model_variables_grouped.reset_index(drop=True,inplace=True)
final_table = final_table.merge(final_model_variables_grouped,how='left',on=['dependent','independent'])

#final_table.to_excel(r'C:\Users\Usuario\Desktop\cars_power_bi_db.xlsx')
