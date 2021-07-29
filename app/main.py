import flask 
from geopy.geocoders import Nominatim
import folium
from flask import request, jsonify
import json
from flask_cors import CORS, cross_origin, logging

###
# This microservice takes an address in Street, City, 2 Letter State Code (GET/POST)
# and returns both an HTML map to the location and a Google Maps link to their map.
# The HTML map is provided by Nominatim, an open source map provider.
# If you're wondering why it doesn't use Google Maps, it's because I didn't want to have to stick
# an API key in here and then have my teammate swap it out for his own and all that, too much work.
# Instead, this map functions perfectly fine, and there is a link to Google Maps that can be
# applied to a button or an overlay to take you to Google Maps.
#
# Example address:
# https://127.0.0.1:5000/api?address=750%20Wall%20Street,%20Fairfield,%20CA
# for "750 Wall Street, Fairfield, CA"
# (post requests should also function through a form submission)
###

app = flask.Flask(__name__)
app.config["DEBUG"] = False
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
logging.getLogger('flask_cors').level = logging.DEBUG

@app.route('/', methods=['GET'])
def home():
    # this is more for debug than anything else
    return "This is a prototype API for returning maps. If you need a map, go to /map | If you need a link, go to /link"

@app.route('/map', methods=['GET', 'POST'])
@cross_origin()
def map():
    # get the address variable filled in
    if request.method == "POST":
        address = request.form.get('address')
    else:
        address = request.args.get('address')

    # just in case it's None for some reason, display an error
    if address == None:
        return "Address not found. (Try format /map?address=YOUR_ADDRESS_HERE)"
    print(f"Address found. Address = {address}")
    
    # GeoPy using Nominatim to return a map to the lat/lon in the query
    geolocator = Nominatim(user_agent="Monduli's Microservice Map Making API")
    data = geolocator.geocode(address)

    # One final check to make sure the data isn't empty
    if data != None:

        # take lat/lon from the pulled information
        latitude = data.latitude
        longitude = data.longitude

        # use folium to create the physical map (zoom_start can be adjusted to how close you want the map to be)
        m = folium.Map(location=[latitude, longitude], zoom_start=18)

        # add a marker in the middle of the map to where you intend to point at
        folium.Marker(
            [latitude, longitude], popup=f"<i>{address}</i>"
        ).add_to(m)

        #img_data = m._to_png(5)
        #img = Image.open(io.BytesIO(img_data))

        x = json.dumps(m._repr_html_())

        return x

    else:
        # if data is None then something messed up
        return "If you are seeing this, your address was likely invalid."

@app.route('/link', methods=['GET', 'POST'])
@cross_origin()
def link():
    # get the address variable filled in
    if request.method == "POST":
        address = request.form.get('address')
    else:
        address = request.args.get('address')

    # just in case it's None for some reason, display an error
    if address == None:
        return "Address not found. (Try format /link?address=YOUR_ADDRESS_HERE)"
    print(f"Address found. Address = {address}")
    
    # GeoPy using Nominatim to return a map to the lat/lon in the query
    geolocator = Nominatim(user_agent="Monduli's Microservice Map Making API")
    data = geolocator.geocode(address)

    # One final check to make sure the data isn't empty
    if data != None:

        # take lat/lon from the pulled information
        latitude = data.latitude
        longitude = data.longitude
        packet = []

        # here's a link to the google map you can use, since it doesn't require the API
        link_to = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
        x = json.dumps(link_to)

        return x

    else:
        # if data is None then something messed up
        return "If you are seeing this, your address was likely invalid."

@app.route('/both', methods=['GET', 'POST'])
def both():
    # get the address variable filled in
    if request.method == "POST":
        address = request.form.get('address')
    else:
        address = request.args.get('address')

    # just in case it's None for some reason, display an error
    if address == None:
        return "Address not found. (Try format /both?address=YOUR_ADDRESS_HERE)"
    print(f"Address found. Address = {address}")
    
    # GeoPy using Nominatim to return a map to the lat/lon in the query
    geolocator = Nominatim(user_agent="Monduli's Microservice Map Making API")
    data = geolocator.geocode(address)

    # One final check to make sure the data isn't empty
    if data != None:

        # take lat/lon from the pulled information
        latitude = data.latitude
        longitude = data.longitude

        # use folium to create the physical map (zoom_start can be adjusted to how close you want the map to be)
        m = folium.Map(location=[latitude, longitude], zoom_start=18)

        # add a marker in the middle of the map to where you intend to point at
        folium.Marker(
            [latitude, longitude], popup=f"<i>{address}</i>"
        ).add_to(m)

        # here's a link to the google map you can use, since it doesn't require the API
        link_to = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"

        to_dump = [None, None]
        to_dump[0] = m._repr_html_()
        to_dump[1] = link_to

        #img_data = m._to_png(5)
        #img = Image.open(io.BytesIO(img_data))

        return json.dumps(to_dump)

if __name__ == "main":
    app.run()
