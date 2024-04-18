import pandas as pd
import numpy as np
import xlsxwriter
import statistics as st

#media data
data1 = pd.read_csv("../Code_files/SIA_media_content_5_months.csv")
#flight data
data_load1 = pd.read_csv("../Code_files/media_use_master_f_ttl.csv", low_memory=False)

#we remove the media that we don't want to consider in both dataset
rm = np.where(data_load1.loc[:,'genre'] == "Highlights")
data1_load = data_load1.drop(data_load1.index[rm])
rm = np.where(data_load1.loc[:,'genre'] == "Singapore Airlines")
data1_load = data_load1.drop(data_load1.index[rm])
rm = np.where(data_load1.loc[:,'genre'].isnull())
data1_load = data_load1.drop(data_load1.index[rm]).reset_index(drop=True)

rm = np.where(data1.loc[:,'genre'] == "Highlights")
data1= data1.drop(data1.index[rm]).reset_index(drop=True)
rm = np.where(data1.loc[:,'genre'] == "Singapore Airlines")
data1= data1.drop(data1.index[rm]).reset_index(drop=True)
rm = np.where(data1.loc[:,'genre'].isnull())
data1 = data1.drop(data1.index[rm]).reset_index(drop=True)

#we assign the corresponding cycles (# months loaded on planes) for each media
n_cycles = []
for m in data1.loc[:,'uniqueID']:
	c_temp = len(np.where(data1.loc[:,'uniqueID']==m)[0])
	n_cycles.append(c_temp)

data1.insert(len(data1.columns), 'n_cycles', n_cycles)

data1_unique = data1
data1_unique = data1_unique.drop_duplicates(subset ="uniqueID", keep = 'first', inplace = False).reset_index(drop=True)

#if play durationis larger than the media duration, we just set the play duration to be equal the media duration
change = np.where(data_load1.loc[:,'play_duration_total_minutes']>data_load1.loc[:,'duration_total_minutes'])
data_load1.loc[data_load1.index[change], 'play_duration_total_minutes'] = data_load1.loc[data_load1.index[change],'duration_total_minutes']

n_media_load = data_load1.shape[0]

#computing prop_usage for each media
prop_usage = []
for i in range(n_media_load):

	if data_load1.loc[i, 'duration_total_minutes'] == 0:
		prop_usage.append(0)
	else: 
		prop_usage.append(data_load1.loc[i, 'play_duration_total_minutes']/data_load1.loc[i, 'duration_total_minutes'])

data_load1.insert(len(data_load1.columns), 'prop_usage', prop_usage)

#creating year categories
currentYear = 2018
year_category = []
for year in data1_unique.loc[:,'year']:
	if year == currentYear:
		year_category.append("new release")
	elif year>=(currentYear-1):
		year_category.append("1 year old")
	elif year>=(currentYear-4):
		year_category.append("2-4 years old")
	elif year>=(currentYear-8):
		year_category.append("5-8 years old")
	elif year>=(currentYear-14):
		year_category.append("9-14 years old")
	elif year>=(currentYear-20):
		year_category.append("14-20 years old")
	else:
		year_category.append("more than 20 years old")

data1_unique.insert(len(data1_unique.columns), 'year_category', year_category)

#creating country_zones
North_america = ['USA', 'CAN']
South_america = ['MEX', 'ARG','BRA','URY']
Europe = ['GBR', 'FRA', 'DEU', 'ITA', 'ESP', 'SWE','SPA','BEL','FIN', 
	'DNK','IRL','ISL', 'RUS', 'POL', 'NLD', 'NOR', 'CZE', 'SVK', 'CHE']
Asia = ['CHN', 'HKG', 'JPN', 'PHL', 'IND', 'TWN', 'LKA', 'KOR', 'VNM','SGP', 'IDN',
	'TAI','SIN', 'THA', 'MYS', 'MNG']
Africa = ['EGY', 'MAR', 'ISR', 'TUN']
Oceania = ['AUS']
Middle_east = ['PAK', 'LBN', 'TUR', 'IRN']

#creating price tag for each media (ad-hoc): needs to be replaced by real cost of each media
price_tag = []
country_zone = []
for i in range(data1_unique.shape[0]):

	year = data1_unique.loc[i,'year_category']
	score = data1_unique.loc[i,'peopleScore']

	if (year == "new release") and (score > 8):
		price_tag.append("$$$$")
	elif (year == "new release" or year=="1 year old" or year=="2-4 years old") and (score > 7):
		price_tag.append("$$$")
	elif (year == "new release" or year=="1 year old" or year=="2-4 years old" or year=="5-8 years old" or year=="9-14 years old") and (score > 5):
		price_tag.append("$$")
	else:
		price_tag.append("$")

	country = data1_unique.loc[i,'countryOrigin']
	if country in Europe:
		country_zone.append('Europe')
	elif country in Asia:
		country_zone.append('Asia')
	elif country in North_america:
		country_zone.append('North_america')
	elif country in South_america:
		country_zone.append('South_america')
	elif country in Africa:
		country_zone.append('Africa')
	elif country in Middle_east:
		country_zone.append('Middle_east')
	elif country in Oceania:
		country_zone.append('Oceania')
	else:
		country_zone.append("")

	genre = data1_unique.loc[i,'genre']

	if genre == 'Adventure':
		data1_unique.loc[i,'genre'] = 'Action & Adventure'
	elif genre == 'Food Culture':
		data1_unique.loc[i,'genre'] = 'Food'
	elif genre in ['Mystery', 'Epic', 'Drama/Horror', 'Martial Arts', 'Musical', 'Lifestyle', 'Romance']:
		data1_unique.loc[i,'genre'] = 'Other'


data1_unique.insert(len(data1_unique.columns), 'price_tag', price_tag)
data1_unique.insert(len(data1_unique.columns), 'country_zone', country_zone)

#we do not aggregate by route, but below is the code to do so. The code is extremely slow because it needs to loop (3M rows X  # routes) times!
aggregate_by_route = False

#WE AGGREAGTE BY ROUTE
if aggregate_by_route:

	data2 = data1_unique
	unique_flight_route = np.unique(data_load1.loc[:,'routeid'])

	for i in range(len(unique_flight_route)-1):
		data2 = np.vstack((data2, data1_unique))

	#data 2 is contains the media info x the number of routes
	data2 = pd.DataFrame(data2)
	data2.columns = data1_unique.columns
	
	#we add the corresponding route to each media 
	col_route = []
	for r in unique_flight_route:
		col_route = col_route + [r]*data1_unique.shape[0]

	data2.insert(len(data2.columns), 'route', col_route)

	# for i in data2.shape[0]:

	load_routes = data_load1.loc[:,'routeid']
	load_ids = data_load1.loc[:,'uniqueID']

	prop_usage_vect = []
	prop_view = []
	for r in unique_flight_route:
		print(r)

		n_media_load_r = len(np.where(data_load1.loc[:,'routeid']==r)[0])

		for i in range(data2.shape[0]):
			if i%100==0:
				print(i)

			r_i = data2.loc[i,'route']
			id_i = data2.loc[i,'uniqueID']

			if r == unique_flight_route[0]:		
				ind_temp = np.where((load_routes == r_i) & (load_ids == id_i))
				p = sum(data_load1.loc[data_load1.index[ind_temp], 'prop_usage'])

				if p>0:
					prop_usage_vect.append(p/len(ind_temp[0]))
				else:
					prop_usage_vect.append(0)

			n_media_r = len(np.where((load_routes==r) & (load_ids==id_i))[0])
			prop_view.append(n_media_r/(n_media_load_r*data1_unique.loc[i,'n_cycles']))

	data2.insert(len(data2.columns), 'prop_usage', prop_usage_vect)
	data2.insert(len(data2.columns), 'prop_view', prop_view)
	data2.to_csv('agreg_by_media_final_new.csv', header=True, index=False)

else:
	#IF WE DON"T AGGREAGTE BY ROUTE
	data3 = data1_unique
	prop_usage_vect = []
	load_ids = data_load1.loc[:,'uniqueID']
	load_class = data_load1.loc[:,'seat_class_name']

	for i in range(data3.shape[0]):
		ind_temp = np.where(load_ids == data3.loc[i,'uniqueID'])
		p = sum(data_load1.loc[data_load1.index[ind_temp], 'prop_usage'])
		if p>0:
			prop_usage_vect.append(p/len(ind_temp[0]))
		else:
			prop_usage_vect.append(0)

	data3.insert(len(data3.columns), 'prop_usage', prop_usage_vect)

	prop_view = []
	business_weight = 1.5
		
	for i, m in enumerate(data3.loc[:,'uniqueID'], start=0):
		n_media_business = len(np.where((load_ids==m) & (load_class == 'Business'))[0])
		n_media_economy = len(np.where((load_ids==m) & (load_class == 'Economy'))[0])
		p_temp = (n_media_economy + n_media_business*business_weight)/(n_media_load*data1_unique.loc[i,'n_cycles'])
		prop_view.append(p_temp)

	data3.insert(len(data3.columns), 'prop_view', prop_view)
	data3.to_csv('agreg_by_media.csv', header=True, index=False)
