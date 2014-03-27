from django.views.decorators.csrf import csrf_exempt
import json
from django.db import connection
import sys
from keyczar.keyczar import Encrypter, Crypter
import logging
from django.http import HttpResponse
from django.shortcuts import render_to_response

logger = logging.getLogger(__name__)

@csrf_exempt
def get_wifi_hotspot(req):
	if req.method == 'POST' and 'lat' in req.POST and 'lon' in req.POST and 'range' in req.POST:
		if lat and lon and r:
			crypter = Crypter.Read("/home/hunglv/Desktop/rsa-privatekeys")

			cur = connection.cursor()
			cur.execute("select ssid, encode(pwd, 'escape'), ST_X(coordinate::geometry), ST_Y(coordinate::geometry), last_updated from wifi_hotspot where ST_Distance(coordinate, ST_GeographyFromText('SRID=4326;POINT({0} {1})')) < {2}".format(lon, lat, r))
			rows = cur.fetchall()
			
			result = []
			hotspot = {}
			for row in rows:
				hotspot['ssid'] = str(row[0])
				hotspot['pwd'] = crypter.Decrypt(row[1])
				hotspot['lat'] = str(row[2])
				hotspot['long'] = str(row[3])
				hotspot['last_updated'] = str(row[4])
				result.append(hotspot)
				
			return HttpResponse(json.dumps([dict(hotspot=pn) for pn in result]), content_type="application/json")
	elif req.method == 'GET':
		return render_to_response('index.html')

	return HttpResponse(status=204)

