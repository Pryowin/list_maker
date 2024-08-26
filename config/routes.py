from flask import jsonify, Blueprint

from config.regions import regions
from application.constants import NOT_FOUND

config_api = Blueprint('config_api', __name__)

@config_api.route('/get_countries')
def get_countries():
    countries = list(regions)
    return jsonify(countries)

@config_api.route('/get_regions/<string:country>')
def get_regions(country: str):
    if country in regions:
        region_list = list(regions[country])
        return jsonify(region_list)
    else:
        return jsonify(message=f"Country '{country}' is not supported."),NOT_FOUND
    