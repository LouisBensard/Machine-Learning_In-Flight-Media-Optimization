import random as rand
import pandas as pd
from pandas import Timestamp
import plotnine as p9 #allows you to use ggplot2 commands
import ggplot
from ggplot import *
from plotnine import *
from python_functions.prop_media_scenarios import *

#this function outputs 4 plots. 1 For the general accuracy of the model for scenario 1 and 3 for the data example. 
#one csv file is also create for the data example
def scenario1(t_vect, best_g_view, data_val, y_view_val, y_view_pred):

	results_vect = [0]*len(t_vect)
	for i in range(len(t_vect)):
		results_vect[i] = prop_media1(t_vect[i], y_view_val, y_view_pred)

	x1 = [int(i * 100) for i in t_vect]
	y1 = [round(i*100,1) for i in results_vect]
	df = pd.DataFrame({'t':x1,'y1':y1})

	#baseline in orange, accuracy of the algorithm in purple
	g1 = ggplot() +\
	geom_line(df, aes(x=x1, y=y1), colour='purple',linetype="solid")+\
	geom_line(df, aes(x=x1, y=x1), colour='orange',linetype = "dashed") +\
	xlab('Top (%) of the New Media List') +\
	ylab('Accuracy (%)')+\
	ggtitle('Prediction Accuracy - Scenario 1') +\
	theme(plot_title = element_text(hjust = 0.5))

	###example
	t_final = 0.2 ; result_final = results_vect[int(t_final*100)-1]
	n_ex = 200; ind_example = rand.sample(list(range(data_val.shape[0])), n_ex)
	data_example = data_val.loc[ind_example,:].reset_index(drop=True)

	pred_view_ex = best_g_view.predict(data_example)
	data_example.insert(len(data_example.columns), 'prop_view_pred', pred_view_ex)
	data_example = data_example.sort_values('prop_view_pred', axis=0, ascending=False, inplace=False).reset_index(drop=True)
	top_ind = int(t_final*n_ex)
	#those are the selected media
	top_movies = data_example.loc[1:top_ind,:].reset_index(drop=True)
	#we export those media into a csv file
	top_movies.to_csv('Top_media_scenario1.csv', header=True, index=False)

	#plots of prop_view
	x2 = list(range(1,n_ex+1))
	y2 = list(data_example.loc[:,'prop_view_pred'])
	df = pd.DataFrame({'x2':x2,'y2':y2})
	g2 = ggplot(df, aes(x=x2, y=y2))+\
	geom_point(size=2)+\
	labs(title='Media Selection Example - Scenario 1', x = 'Number of Media from the New List', y='Predicted Proportion Views')+\
	theme(plot_title = element_text(hjust = 0.5))+\
	geom_text(top_movies.loc[0:3,:], aes(x=list(np.arange(1, 5, 1)+20), y=y2[0:4], label=list(top_movies.loc[0:3,'title'])), size=5)

	#visualization of the accuracy
	d = result_final*n_ex
	df1 = pd.DataFrame(['Bottom', 'Top'])

	g3 = ggplot(df1, aes(x=['Bottom', 'Top'], y=[int(n_ex*(1-t_final))*t_final, int(n_ex*t_final)*t_final],fill=['Bottom', 'Top']))+\
	geom_bar(stat="identity")+\
	labs(title='Top '+ str(int(t_final*100))+'% Without Algorithm',\
		x="Correct Selection Rate = "+ str(round(t_final,2)), y = "Number of Media")+\
	theme(plot_title = element_text(hjust = 0.5),axis_text_x = element_blank())

	g4 = ggplot(df1, aes(x=['Bottom', 'Top'], y=[int(n_ex-d)*t_final, int(d)*t_final],fill=['Bottom', 'Top']))+\
	geom_bar(stat="identity")+\
	labs(title='Top '+ str(int(t_final*100))+'% With Algorithm',\
		x="Correct Selection Rate = "+str(round(result_final,2)), y = "Number of Media")+\
	theme(plot_title = element_text(hjust = 0.5),axis_text_x = element_blank())

	return(g1,g2,g3,g4)

#this function outputs 4 plots. 1 For the general accuracy of the model for scenario 2 and 3 for the data example. 
#one csv file is also create for the data example
def scenario2(q_vect, best_g_view, data_big_cv, data_val, y_view_val, y_view_pred):

	p_star_vect = np.quantile(data_big_cv.loc[:,'prop_view'], 1-q_vect)

	results_vect = [0]*len(p_star_vect)
	for i in range(len(p_star_vect)):
		results_vect[i] = prop_media2(p_star_vect[i], y_view_val, y_view_pred)

	x1 = [int(i * 100) for i in q_vect]
	y1 = [round(i*100,1) for i in results_vect]
	df = pd.DataFrame({'x1':x1,'y1':y1})

	#baseline in orange, accuracy of the algorithm in purple
	g1 = ggplot() +\
	geom_line(df, aes(x=x1, y=y1), colour='purple',linetype="solid")+\
	geom_line(df, aes(x=x1, y=x1), colour='orange',linetype = "dashed") +\
	xlab('Top (%) of the New Media List') +\
	ylab('Accuracy (%)')+\
	ggtitle('Prediction Accuracy - Scenario 2') +\
	theme(plot_title = element_text(hjust = 0.5))

	###example
	q_final = 0.2 ; p_star_final = p_star_vect[int(q_final*100)-1]
	result_final = results_vect[int(q_final*100)-1]
	n_ex = 200; ind_example = rand.sample(list(range(data_val.shape[0])), n_ex)
	data_example = data_val.loc[ind_example,:].reset_index(drop=True)

	pred_view_ex = best_g_view.predict(data_example)
	data_example.insert(len(data_example.columns), 'prop_view_pred', pred_view_ex)
	data_example = data_example.sort_values('prop_view_pred', axis=0, ascending=False, inplace=False).reset_index(drop=True)
	n_media_select = len(np.where(pred_view_ex>p_star_final)[0])
	#those are the selected media
	top_movies = data_example.loc[1:n_media_select,:].reset_index(drop=True)
	#we export those media into a csv file
	top_movies.to_csv('Top_media_scenario2.csv', header=True, index=False)

	#plots of prop_view
	x2 = list(range(1,n_ex+1))
	y2 = list(data_example.loc[:,'prop_view_pred'])
	df = pd.DataFrame({'x2':x2,'y2':y2})
	g2 = ggplot(df, aes(x=x2, y=y2))+\
	geom_point(size=2)+\
	labs(title='Media Selection Example - Scenario 2', x = 'Number of Media from the New List', y='Predicted Proportion Views')+\
	theme(plot_title = element_text(hjust = 0.5))+\
	geom_text(top_movies.loc[0:3,:], aes(x=list(np.arange(1, 5, 1)+20), y=y2[0:4], label=list(top_movies.loc[0:3,'title'])), size=5)

	#visualization of the accuracy
	df1 = pd.DataFrame(['Bottom', 'Top'])

	g3 = ggplot(df1, aes(x=['Bottom', 'Top'], y=[int(n_ex*(1-q_final))*q_final, int(n_ex*q_final)*q_final],fill=['Bottom', 'Top']))+\
	geom_bar(stat="identity")+\
	labs(title='Best '+ str(round(q_final*100))+'% Without Algorithm',\
		x="Correct Selection Rate = "+ str(round(q_final,2)), y = "Number of Media")+\
	theme(plot_title = element_text(hjust = 0.5),axis_text_x = element_blank())

	g4 = ggplot(df1, aes(x=['Bottom', 'Top'], y=[int(n_media_select*(1-result_final)), int(n_media_select*result_final)],fill=['Bottom', 'Top']))+\
	geom_bar(stat="identity")+\
	labs(title='Best '+ str(round(q_final*100))+'% With Algorithm',\
		x="Correct Selection Rate = "+ str(round(result_final,2)), y = "Number of Media")+\
	theme(plot_title = element_text(hjust = 0.5),axis_text_x = element_blank())

	return(g1,g2,g3,g4)

#this function outputs 4 plots. 1 For the general accuracy of the model for scenario 3 and 3 for the data example. 
#one csv file is also create for the data example
def scenario3(money_vect, best_g_view, data_val, y_view_val, y_view_pred):

	prop_vect = [0]*len(money_vect)
	ord_y_view_pred = list(np.argsort(-y_view_pred))

	for m in range(len(money_vect)):
		s = 0; i=0
		while s<money_vect[m]:
			ord_i = ord_y_view_pred[i]
			s = s+data_val.loc[ord_i, 'price_tag']
			i = i+1

		prop_vect[m] = i/data_val.shape[0]


	results_vect = [0]*len(prop_vect)
	for i in range(len(prop_vect)):
		results_vect[i] = prop_media1(prop_vect[i], y_view_val, y_view_pred)

	x1 = [int(i * 100) for i in prop_vect]
	y1 = [round(i*100,1) for i in results_vect]
	df = pd.DataFrame({'m':money_vect,'y1':y1})

	#baseline in orange, accuracy of the algorithm in purple
	g1 = ggplot() +\
	geom_line(df, aes(x=money_vect, y=y1), colour='purple',linetype="solid")+\
	geom_line(df, aes(x=money_vect, y=x1), colour='orange',linetype = "dashed") +\
	xlab('Money Index spent on Media') +\
	ylab('Accuracy (%)')+\
	ggtitle('Prediction Accuracy - Scenario 3') +\
	theme(plot_title = element_text(hjust = 0.5))

	###example
	money_final=300

	s = 0; i=0
	while s<money_final:
		ord_i = ord_y_view_pred[i]
		s = s+data_val.loc[ord_i, 'price_tag']
		i = i+1

	prop_final = i/data_val.shape[0]

	n_ex = 200; ind_example = rand.sample(list(range(data_val.shape[0])), n_ex)
	data_example = data_val.loc[ind_example,:].reset_index(drop=True)

	pred_view_ex = best_g_view.predict(data_example)
	data_example.insert(len(data_example.columns), 'prop_view_pred', pred_view_ex)
	data_example = data_example.sort_values('prop_view_pred', axis=0, ascending=False, inplace=False).reset_index(drop=True)
	result_final = prop_media1(prop_final, data_example.loc[:,'prop_view'], data_example.loc[:,'prop_view_pred'])
	top_ind = int(prop_final*n_ex)
	#those are the selected media
	top_movies = data_example.loc[1:top_ind,:].reset_index(drop=True)
	#we export those media into a csv file
	top_movies.to_csv('Top_media_scenario3.csv', header=True, index=False)

	#plots of prop_view
	x2 = list(range(1,n_ex+1))
	y2 = list(data_example.loc[:,'prop_view_pred'])
	df = pd.DataFrame({'x2':x2,'y2':y2})
	g2 = ggplot(df, aes(x=x2, y=y2))+\
	geom_point(size=2)+\
	labs(title='Media Selection Example - Scenario 3', x = 'Number of Media from the New List', y='Predicted Proportion Views')+\
	theme(plot_title = element_text(hjust = 0.5))+\
	geom_text(top_movies.loc[0:3,:], aes(x=list(np.arange(1, 5, 1)+20), y=y2[0:4], label=list(top_movies.loc[0:3,'title'])), size=5)

	#visualization of the accuracy
	d = result_final*n_ex
	df1 = pd.DataFrame(['Bottom', 'Top'])

	g3 = ggplot(df1, aes(x=['Bottom', 'Top'], y=[int(n_ex*(1-prop_final))*prop_final, int(n_ex*prop_final)*prop_final],fill=['Bottom', 'Top']))+\
	geom_bar(stat="identity")+\
	labs(title='Best $'+ str(money_final)+' Without Algorithm',\
		x="Correct Selection Rate = "+ str(round(prop_final,2)), y = "Number of Media")+\
	theme(plot_title = element_text(hjust = 0.5),axis_text_x = element_blank())

	g4 = ggplot(df1, aes(x=['Bottom', 'Top'], y=[int(n_ex-d)*prop_final, int(d)*prop_final],fill=['Bottom', 'Top']))+\
	geom_bar(stat="identity")+\
	labs(title='Best $'+ str(money_final)+' With Algorithm',\
		x="Correct Selection Rate = "+ str(round(result_final,2)), y = "Number of Media")+\
	theme(plot_title = element_text(hjust = 0.5),axis_text_x = element_blank())

	return(g1,g2,g3,g4)
