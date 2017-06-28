from flask import Blueprint, jsonify
from models.restaurants import Restaurant
from models.menu_items import MenuItem
from controllers import auth

api = Blueprint("api", __name__)


@api.route("/restaurants/json")
@auth.login_required
def restaurants_json():
    restaurants = Restaurant.query.all()
    return jsonify(restaurants=[r.serialize_menu_items() for r in restaurants])

