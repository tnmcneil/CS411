# REFERENCE: https://github.com/bitpixdigital/forecastiopy3
#pip install forecastiopy 

from forecastiopy import *
import datetime

apikey = "a3dcd9207fb67780ae8dddd92d9be3f8"

Lisbon = [38.7252993, -9.1500364]

fio = ForecastIO.ForecastIO(apikey,units=ForecastIO.ForecastIO.UNITS_SI,lang=ForecastIO.ForecastIO.LANG_ENGLISH,latitude=Lisbon[0], longitude=Lisbon[1],time='1448234556')

print('Latitude', fio.latitude, 'Longitude', fio.longitude)
print('Timezone', fio.timezone, 'Offset', fio.offset)
print(fio.get_url()) # You might want to see the request url

if fio.has_currently() is True:
	currently = FIOCurrently.FIOCurrently(fio)
	print('Currently')
	for item in currently.get().keys():
		print(item + ' : ' + str(currently.get()[item]))
	# Or access attributes directly
	print(currently.temperature)
	print(currently.humidity)
else:
	print('No Currently data')