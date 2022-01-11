import random
from datetime import datetime
from coffee_facts import get_coffee_facts


from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from os import environ
from google_lat_lot_getter import get_lat_lon_location, get_latitude_longitude_from_google_address

# google_maps_api_key = environ["GOOGLE_MAPS_API_KEY"]

app = Flask(__name__)

# connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Database/cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

# database constructor 
db = SQLAlchemy(app)


# table configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    map_url = db.Column(db.String(250))
    img_url = db.Column(db.String(250))
    location = db.Column(db.String(250))
    has_sockets = db.Column(db.BOOLEAN())
    has_toilet = db.Column(db.BOOLEAN())
    has_wifi = db.Column(db.BOOLEAN())
    can_take_calls = db.Column(db.BOOLEAN())
    seats = db.Column(db.String(200))
    coffee_price = db.Column(db.String(10))

    def __repr__(self):
        return f"CafeObject: {self.name}"


def get_coffee_object_data(cafe_object: Cafe):
    cafe_attrs = cafe_object.__dict__
    del cafe_attrs["_sa_instance_state"]
    return cafe_attrs


def get_coffee_attributes():
    return [key for key in Cafe.__dict__.keys() if not key.startswith("_")]


def displayed_attributes():
    x = get_coffee_attributes()
    del x[2:4]
    return x


def attribute_icons():
    return ["home", "map-marked-alt", "plug", "restroom", "wifi", "mobile", "chair", "dollar-sign"]


def cafe_info_list():
    return [get_coffee_object_data(coffee) for coffee in Cafe.query.all()]


def attribute_icon_dict(attributes, icons):
    return dict(zip(attributes[1:], icons))


@app.route("/")
def homepage():
    # all but id
    iconnames = attribute_icons()
    attributes = displayed_attributes()
    cafes = [[get_latitude_longitude_from_google_address(get_lat_lon_location(cafe)), cafe.name,
                                   cafe.location, cafe.img_url] for cafe in Cafe.query.all() if
                                  get_latitude_longitude_from_google_address(get_lat_lon_location(cafe)) is not None]
    print(f"cafes: {cafes}")
    attr_icon = attribute_icon_dict(attributes, iconnames)
    return render_template("main_page/home_page.html",
                           attributes=attr_icon,
                           icons=iconnames,
                           cafes=cafes,
                           cafe_info=cafe_info_list(),
                           coffee_params=attributes,
                           current_date=datetime.now(),
                           )


@app.route("/cafe_list/")
def coffee_list_page():
    return render_template('coffee_list_page/coffee_list_page.html', cafe_info=cafe_info_list(), coffee_params=displayed_attributes(),
                           attributes=attribute_icon_dict(displayed_attributes(), attribute_icons()),
                           iconnames=attribute_icons(),
                           current_date=datetime.now().year,
                           coffee_facts_dict=get_coffee_facts())


@app.route("/more_info", methods=["GET", "POST"])
def more_info():
    requested_coffee_id = request.args.get("id")
    print(requested_coffee_id)
    current_coffee_object = Cafe.get(requested_coffee_id)
    return render_template('coffee_info.html', coffee=current_coffee_object)



def get_random_cafe():
    random_cafe = Cafe.query.all()
    return random.choice(random_cafe)


print(get_coffee_object_data(get_random_cafe()))
# print((get_lat_lon_location(get_random_cafe())))
# print(get_latitude_longitude_from_google_address(get_lat_lon_location(get_random_cafe())))
if __name__ == "__main__":
    app.run(debug=True)
