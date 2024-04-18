import numpy as np

#this function computes the proportion of media accurately classified in the top prop%
def prop_media1(t, y_view_val, y_view_pred):

	n_media = int(t*len(y_view_val))

	a_view = list(np.argsort(-y_view_val)[:n_media])
	b_view = list(np.argsort(-y_view_pred)[:n_media])

	count_view = 0
	for i in range(n_media):
		if b_view[i] in a_view:
			count_view = count_view+1

	prop_predicted_view = count_view/n_media

	return(prop_predicted_view)

#this function computes the proportion of media prdicted to fall within the top p_star%
#that are in fact in the top p_star% of the current load
def prop_media2(p_star, y_view_val, y_view_pred):

	n_media_val = len(np.where(y_view_val>p_star)[0])
	n_media_pred = len(np.where(y_view_pred>p_star)[0])

	if min(n_media_val,n_media_pred)==0:
		return(0)

	a_view = list(np.argsort(-y_view_val)[:n_media_val])
	b_view = list(np.argsort(-y_view_pred)[:n_media_pred])

	count_view = 0

	for i in range(n_media_pred):
		if b_view[i] in a_view:
			count_view = count_view+1

	prop_predicted_view = count_view/n_media_val

	return(prop_predicted_view)