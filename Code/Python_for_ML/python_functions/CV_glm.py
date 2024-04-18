import numpy as np
import random as rand
import statsmodels.api as sm

def CV_glm(data_big_cv, k):

	n_cv = data_big_cv.shape[0]

	#we randomly assign each datapoint to be one of the k fold
	r = list(range(n_cv))
	rand.shuffle(r)
	folds = np.array_split(r,k)
	c_view0 = 0 #initialize correlation squared

	#Perform k fold cross validation
	for i in range(k):
		#dividing the dataset into training set and test set
		test_ind = tuple(folds[i].tolist())
		not_test_ind = [x for x in range(n_cv) if x not in test_ind]
		data_test = data_big_cv.loc[test_ind,:].reset_index(drop=True)
		data_train = data_big_cv.loc[not_test_ind,:].reset_index(drop=True)

		#training the glm with the training set
		g_view = sm.formula.glm("prop_view ~ a_list_qty + win_idx +nom_idx+genre\
				+country_zone + year_category + price_tag + peopleScore +\
				ratingDes +contenttype", 
				data=data_train, family = sm.families.Binomial(), missing='drop').fit()

		#we test it with the test set
		pred_view = g_view.predict(data_test)

		#computing the correlation squred between the real and the precited prop_view
		y_test_view = data_test.loc[:,'prop_view']
		c_view = np.corrcoef(y_test_view, pred_view)[0,1]**2

		#store the model that maximizes the correlation squared
		if c_view>c_view0:
			best_g_view = g_view
			c_view0 = c_view

	return(best_g_view)