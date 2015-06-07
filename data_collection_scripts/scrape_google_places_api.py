from googleplaces import GooglePlaces, types, lang
import json
import csv

YOUR_API_KEY = 'AIzaSyC_vbziHvd_TY1i4qknEFHGaWOYheAdRUA'

with open('test.csv', 'wb') as fp:
  a = csv.writer(fp, delimiter=',')
  rows = []

  google_places = GooglePlaces(YOUR_API_KEY)

  # You may prefer to use the text_search API, instead.
  query_result = google_places.nearby_search(
          location='Chicago',
          radius=200000)

  rows.append(['name','kind','address','phone','website','lat','lng','latlng'])

  for place in query_result.places:
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

    rows.append(row)

  a.writerows(rows)


'''
    if "opening_hours" in place.details:
      if "periods" in place.details[u'opening_hours']: 
        print place.details[u'opening_hours'][u'periods']
        if len(place.details[u'opening_hours'][u'periods']) == 7:
        for period in place.details[u'opening_hours'][u'periods']:
          row.append(period['open'][u'time'] 

        if "open" in place.details[u'opening_hours']:
'''          



