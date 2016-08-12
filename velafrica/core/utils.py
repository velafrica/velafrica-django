import googlemaps

# initialize client
gmaps = googlemaps.Client(key='AIzaSyAzdwjRWqj_TTq-jW30NpLWK3La6_i2yRM')

def get_geolocation(address):
	"""
	Returns a dict of latitude (lat) and longitude (lng), which represents the first result received by Google Geocoding
	"""
	geocode_result = gmaps.geocode(address)
	if geocode_result:
		return geocode_result[0]['geometry']['location']
	else:
		return None


def get_googlemaps_url_place(address):
	"""
	"""
	return u"https://maps.google.ch/maps/place/{}".format(address)

def get_distance(origin, destination):
	"""
	Returns the distance in metres between two destinations.
	"""
	distance_result = gmaps.distance_matrix(origin, destination, mode="driving")
	print distance_result
	if distance_result:
		return distance_result['rows'][0]['elements'][0]['distance']['value']
	else:
		return None


def get_googlemaps_url_distance(origin, destination):
	"""
	"""
	return u"https://maps.google.ch/maps/dir/{}/{}".format(origin, destination)