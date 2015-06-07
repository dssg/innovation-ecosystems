from googleplaces import GooglePlaces, types, lang
import json
import csv
import pandas as pd

YOUR_API_KEY = 'AIzaSyC_vbziHvd_TY1i4qknEFHGaWOYheAdRUA'
google_places = GooglePlaces(YOUR_API_KEY)

df = pd.read_csv('../googleDS_chicago.csv')
interesting = ['library','university','school','park','museum','church']
interesting_types = [types.TYPE_LIBRARY, types.TYPE_UNIVERSITY, 
										types.TYPE_SCHOOL, types.TYPE_PARK,
										types.TYPE_MUSEUM, types.TYPE_CHURCH]
places_to_find = df[df.category.isin(interesting)]
del df

with open('test.csv', 'wb') as fp:

	a = csv.writer(fp, delimiter=',')
	rows = []
	#rows.append(['name','kind','address',
	#		'phone','website','rating','lat','lng','latlng'])

	a.writerow(['name','kind','address',
			'phone','website','rating','lat','lng','latlng'])

	for idx, ofInterest in places_to_find.iterrows():

		coord = {'lat': ofInterest.y, 'lng': ofInterest.x}

		query_result = google_places.nearby_search(
			lat_lng=coord, types=[types.TYPE_LIBRARY, types.TYPE_UNIVERSITY, 
										types.TYPE_SCHOOL, types.TYPE_PARK,
										types.TYPE_MUSEUM, types.TYPE_CHURCH], radius = 10)

		for place in query_result.places[:1]:
			place.get_details()
		#    print json.dumps(place.details, sort_keys=True, indent=4, separators=(',', ': '))

			row = [] 

				# the below is a disgusting and terrible process called...
				# converting json to csv

			if "name" in place.details:
				row.append(place.details[u'name'])
			else:
					row.append('')

			if "types" in place.details:
				row.append(place.details[u'types'][0])
			else:
				row.append('')

			if "formatted_address" in place.details:
				row.append(place.details[u'formatted_address'])
			else:
				row.append('')

			if "formatted_phone_number" in place.details:
				row.append(place.details[u'formatted_phone_number'])
			else:
				row.append('')

			if "website" in place.details:
				row.append(place.details[u'website'])
			else:
				row.append('')

			if "rating" in place.details:
				row.append(place.details[u'rating'])
			else:
				row.append('')

			if "geometry" in place.details:
				if "location" in place.details[u'geometry']:
					if "lat" in place.details[u'geometry'][u'location'] and "lng" in place.details[u'geometry'][u'location']:
						row.append(place.details[u'geometry'][u'location'][u'lat'])
						row.append(place.details[u'geometry'][u'location'][u'lng'])
						row.append('(' + str(place.details[u'geometry'][u'location'][u'lng']) +
							',' + str(place.details[u'geometry'][u'location'][u'lng']) + ')') 
					else:
						row.append('')
				else:
					row.append('')
			else:
				row.append('')

			#rows.append(row)

			a.writerow(row)
			fp.flush()


'''
if "opening_hours" in place.details:
if "periods" in place.details[u'opening_hours']: 
print place.details[u'opening_hours'][u'periods']
if len(place.details[u'opening_hours'][u'periods']) == 7:
for period in place.details[u'opening_hours'][u'periods']:
row.append(period['open'][u'time'] 

if "open" in place.details[u'opening_hours']:
'''          



