import config
import requests
from sqlalchemy import create_engine
from io import BytesIO
from PIL import Image

# api parameters
url = "https://maps.googleapis.com/maps/api/staticmap?"
api_key = config.api_key
centre = 'HP13 6HP'
maptype='satellite'
zoom = 17

# MySQL connection

engine = config.engine

# get postcodes

postcode_qry = 'SELECT DISTINCT postcode FROM lr_price WHERE left(postcode, 4) in ' \
                '("HP10", "HP11", "HP12", "HP13", "HP15");'

with engine.connect() as conn:
    res = conn.execute(postcode_qry)

postcodes = [x[0] for x in res.fetchall()]

# get images

box = (20,20,620,620) # left, upper, right, lower pixel boundaries for cropping
failed_areas = []
for p in postcodes:
    try:
        print('Getting image for {}...'.format(p), end=' ')
        req = "{}center={}&zoom={}&size=640x640&maptype={}&key={}&sensor=false" \
            .format(url, p, zoom, maptype, api_key)
        img = requests.get(req)
        b = BytesIO(img.content)
        with Image.open(b) as im:
            cropped = im.crop(box)
            cropped.save('images/zoom18/{}.png'.format(p))
        print('done.')
    except:
        print('FAILED.')
        failed_areas.append(p)
        continue