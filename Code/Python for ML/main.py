import numpy as np
import random as rand
import pandas as pd
from python_functions.scenarios import *
from python_functions.CV_glm import *

data1 = pd.read_csv('../Code_files/agreg_by_media.csv')
data2 = data1.loc[:,['title', 'genre', 'country_zone', 'contenttype', 
	'peopleScore', 'ratingDes', 'nom_idx', 'win_idx', 'a_list_qty', 
	'year_category', 'price_tag', 'prop_view', 'prop_usage']]

data2 = data2.dropna(inplace=False).reset_index(drop=True)

temp = np.where(data2.loc[:'price_tag'] == '$')
data2.loc[temp[0], 'price_tag'] = 1
temp = np.where(data2.loc[:'price_tag'] == '$$')
data2.loc[temp[0], 'price_tag'] = 2
temp = np.where(data2.loc[:'price_tag'] == '$$$')
data2.loc[temp[0], 'price_tag'] = 3
temp = np.where(data2.loc[:'price_tag'] == '$$$$')
data2.loc[temp[0], 'price_tag'] = 4

data_big = data2
n = data_big.shape[0]

#RECOMMENDATION I
total_views = sum(data_big.prop_view)

#Conservative option
q = 0.15 #we remove 15% of the current load
r1 = np.quantile(data_big.prop_view, q)
r2 = np.where(data_big.prop_view>r1)[0].tolist()
rem = sum(data_big.prop_view[r2])/total_views
print('After removing',int(q*100),'% of the media,', round(rem*100,1), '% of the total views are still remaining\n') #99%

#Moderate option
q = 0.35 #we remove 15% of the current load
r1 = np.quantile(data_big.prop_view, q)
r2 = np.where(data_big.prop_view>r1)[0].tolist()
rem = sum(data_big.prop_view[r2])/total_views
print('After removing',int(q*100),'% of the media,', round(rem*100,1), '% of the total views are still remaining\n') #95%

#Aggressive option
q = 0.80 #we remove 15% of the current load
r1 = np.quantile(data_big.prop_view, q)
r2 = np.where(data_big.prop_view>r1)[0].tolist()
rem = sum(data_big.prop_view[r2])/total_views
print('After removing',int(q*100),'% of the media,', round(rem*100,1), '% of the total views are still remaining\n') #68%

#Mad Max option
q = 0.95 #we remove 15% of the current load
r1 = np.quantile(data_big.prop_view, q)
r2 = np.where(data_big.prop_view>r1)[0].tolist()
rem = sum(data_big.prop_view[r2])/total_views
print('After removing',int(q*100),'% of the media,', round(rem*100,1), '% of the total views are still remaining\n') #38%

#RECOMMENDATION II
#we randomly select the validation set (20% of the dataset)
ind_val = rand.sample(list(range(n)), int(0.2*n))

#we split the dataset into validation set and cv_set
data_val = data_big.loc[ind_val,:].reset_index(drop=True)
not_ind_val = [x for x in range(n) if x not in ind_val]
data_big_cv = data_big.loc[not_ind_val,:].reset_index(drop=True)


k = 10 # number of folds for the CV in the algorithm
#we run the algorithm
best_g_view = CV_glm(data_big_cv, k)

#we use the best model obtained to predcit prop_view for the validation set
pred_view_val = best_g_view.predict(data_val)

y_view_val = data_val.loc[:,'prop_view']
y_view_pred = pred_view_val
#this is the correlation squared between the predicted proportion_view and the real values
c_view = np.corrcoef(y_view_val, y_view_pred)[0,1]**2

#scenario 1: give me the top x% of the media list
t_vect = np.arange(0.01,1.01, 0.01)
res1 = scenario1(t_vect, best_g_view, data_val, y_view_val, y_view_pred)
#run res1 to see the plots

#scenario 2: Give me the media that would be in the top x%
q_vect = np.arange(0.01,1.01, 0.01)
res2 = scenario2(q_vect, best_g_view, data_big_cv, data_val, y_view_val, y_view_pred)
#run res2 to see the plots

#scenario 3: give me how much money you can spend I tell you what to buy
money_vect = list(range(10, sum(data_val.loc[:, 'price_tag']), 10))
res3 = scenario3(money_vect, best_g_view, data_val, y_view_val, y_view_pred)
#run res3 to see the plots

