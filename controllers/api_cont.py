from flask import Blueprint, jsonify, g
from models.restaurants import Restaurant
from models.users import User
from models.menu_items import MenuItem
from controllers import auth


@auth.verify_password
def verify_pw(username_or_token, password):
    """ verifies either a username / password combo, or an auth token """
    print("verifying password for {}".format(username_or_token))
    # first check to see if we got a user by querying the db
    user = User.query.filter_by(username=username_or_token).first()
    if user:
        print("found a user")
        # we are authorizing a username / password
        if user.verify_password(password):
            print("password is verified")
            g.user = user
            return True
    else:
        # we are authorizing a token
        print("no user so check for token")
        user_id = User.verify_token(username_or_token)
        user = User.query.get(user_id)

        # check to see if the user is valid. if so it's ok to proceed
        if user:
            print("found a user from the token")
            g.user = user
            return True
        else:
            print("No User found from token :(")

api = Blueprint("api", __name__)


# send a valid user an access token if requested
@api.route("/restaurants/token")
@auth.login_required
def send_token():
    # generate an auth token for the verified user in flask.g
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@api.route("/restaurants/json")
@auth.login_required
def restaurants_json():
    restaurants = Restaurant.query.all()
    return jsonify(restaurants=[r.serialize_menu_items() for r in restaurants])

