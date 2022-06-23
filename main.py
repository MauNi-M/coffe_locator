import logging
import random
from datetime import datetime
from pprint import pp

from static.degrees_of_difficulty import dod_dict

from markupsafe import Markup

from coffee_facts import get_coffee_facts

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from os import environ
from google_lat_lot_getter import get_lat_lon_location_page, get_lat_lon_location_no_page
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, RadioField
from wtforms.validators import DataRequired, Length, Email, URL, Optional

# google_maps_api_key = environ["GOOGLE_MAPS_API_KEY"]
mapbox_api_key = environ["MAPBOX_API"]


app = Flask(__name__)

# connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Database/cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
# secret key for csfr protection
app.config["SECRET_KEY"] = "fCVgFuWK2eG6HCPnjB8i"
handler = logging.FileHandler("cafes.log")
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)
# database constructor 
db = SQLAlchemy(app)


# table configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    map_url = db.Column(db.String(250))
    img_url = db.Column(db.String(250))
    location = db.Column(db.String(250))
    how_easy_to_find_sockets = db.Column(db.String(15))
    how_comfortably_restroom = db.Column(db.String(15))
    how_good_wifi = db.Column(db.String(15))
    how_comfortably_take_calls = db.Column(db.String(15))
    how_easy_to_find_seats = db.Column(db.String(15))
    coffee_price = db.Column(db.String(10))

    def __repr__(self):
        return f"CafeObject: {self.name}"


degrees_of_difficulty = ["vsimple", "fsimple", "ntrivial", "intermediate", "difficult"]
dod_labels = ["Very Simple", "Fairly Simple", "Non-Trivial", "Had Some challenges", "Difficult or non-existent"]
choices = [(value, Markup(dod_dict[label])) for value, label in zip(degrees_of_difficulty, dod_labels)]


# edit cafe form
class CafeParametersEditForm(FlaskForm):
    new_name = StringField("Name of the coffeeshop", validators=[Optional(), Length(min=4)])
    new_map_url = StringField("Paste a Google Maps url please",
                              validators=[Optional(), URL(message="Something went wrong with url")])
    new_how_easy_to_find_sockets = RadioField("How easy is to find a socket?", choices=choices)
    new_how_comfortably_restroom = RadioField("Can you comfortably use the restroom?", choices=choices)
    new_how_comfortably_to_take_calls = RadioField("How comfortable is to take calls?", choices=choices)
    new_how_good_wifi = RadioField("How good is the internet connection?", choices=choices)
    new_how_easy_to_find_seats = RadioField("How many seats would you say it has?", choices=choices)
    new_coffee_price = DecimalField("How much does the coffee cost (pounds)?", places=2, rounding=None,
                                    validators=[Optional()])

    # todo: add upload images field


def get_coffee_object_data(cafe_object):
    cafe_attrs = cafe_object.__dict__.copy()
    del cafe_attrs["_sa_instance_state"]
    # print(cafe_attrs)
    return cafe_attrs


# new_old relation
def get_new_to_old() -> dict:
    return {key: key.replace("new_", "") for key in CafeParametersEditForm.__dict__.keys() if not key.startswith("_")}


def get_coffee_data() -> list:
    return [key for key in Cafe.__dict__.keys() if not key.startswith("_")]


def displayed_attributes():
    x = get_coffee_data()
    del x[2:4]
    return x


def cafe_list():
    return [get_coffee_object_data(coffee) for coffee in Cafe.query.all()]


def attribute_icon_dict(attributes, icons):
    return dict(zip(attributes[1:], icons))


# global variables
# footer variables
@app.context_processor
def inject_current_date():
    current_date = datetime.now()
    return dict(current_date=current_date, mapbox_key=mapbox_api_key)


# name of icons variables
@app.context_processor
def inject_iconnames():
    iconnames = ["home", "plug", "restroom", "wifi", "chair", "dollar-sign"]
    return dict(iconnames=iconnames)


@app.context_processor
def inject_attribute_icon_dict():
    iconnames = ["home", "map-marked-alt", "plug", "restroom", "wifi", "mobile", "chair", "dollar-sign"]
    attr_icon = attribute_icon_dict(displayed_attributes(), iconnames)
    return dict(attr_icon=attr_icon)




def coffees_with_location():
    cafes = []
    for cafe in Cafe.query.all():
        sub_cafe = []
        if "page" in cafe.map_url:
            sub_cafe.append(get_lat_lon_location_page(cafe.name))
        else:
            sub_cafe.append(get_lat_lon_location_no_page(cafe.map_url))
        sub_cafe.append(cafe.name)
        sub_cafe.append(cafe.location)
        sub_cafe.append(cafe.img_url)
        cafes.append(sub_cafe)
    return cafes


@app.context_processor
# first attempt to create a coffee filter
def list_of_coffees():
    # all_coffees = [get_coffee_object_data(coffee) for coffee in Cafe.query.all()]
    # coffee_sock = [get_coffee_object_data(coffee) for coffee in Cafe.query.order_by(Cafe.how_easy_to_find_sockets).all()]
    # bathroom_qual = [get_coffee_object_data(coffee) for coffee in Cafe.query.order_by(Cafe.how_comfortably_restroom).all()]
    # internet_qual = [get_coffee_object_data(coffee) for coffee in Cafe.query.order_by(Cafe.how_good_wifi).all()]
    # space = [get_coffee_object_data(coffee) for coffee in Cafe.query.order_by(Cafe.how_easy_to_find_seats).all()]
    # price = [get_coffee_object_data(coffee) for coffee in Cafe.query.order_by(Cafe.coffee_price)]
    return dict(coffee_list=cafe_list())


@app.route("/")
def homepage():
    return render_template("main_page/home_page.html", cafes_with_loc=coffees_with_location())


@app.route("/cafe_list/")
def coffee_list_page():
    return render_template('coffee_list_page/coffee_list_page.html',
                           coffee_facts_dict=get_coffee_facts(),
                           cafes_with_loc=coffees_with_location())


@app.route("/more_info", methods=["GET", "POST"])
def more_info():
    requested_coffee_id = request.args.get("id")

    current_coffee_object = Cafe.query.get(requested_coffee_id)

    return render_template('coffee_info_page/coffee_info.html',
                           current_coffee=current_coffee_object)


@app.context_processor
def inject_latitude_longitude():
    def get_lat_lon(coffee_object):
        map_url = coffee_object.map_url
        if "page" in map_url:
            return get_lat_lon_location_page(coffee_object.name)
        else:
            return get_lat_lon_location_no_page(map_url)
    return dict(lat_lon=get_lat_lon)


@app.route("/more_info/<incoming_coffee>/<coffee_id>", methods=["GET", "POST"])
def edit_page(incoming_coffee, coffee_id):
    edit_cafe_form = CafeParametersEditForm()
    # pp(edit_cafe_form.__dict__)
    # print(edit_cafe_form.meta.__dict__)
    coffee_to_edit = Cafe.query.get(coffee_id)

# validate cafe edit form
    if edit_cafe_form.validate_on_submit():
        # check incoming values
        # print(f"old coffee_object: {get_coffee_object_data(coffee_to_edit)}")
        for key in request.form.to_dict():
            # if value is filled, replace it in old value
            current_value = request.form.to_dict()[key]
            # print(f"current key: {key}")
            # print(f"current value: {current_value}")
            # print(f"{get_new_to_old().keys()}")
            if current_value and key in get_new_to_old().keys():
                # print(f"valid key")
                # print(f"replacing: {get_new_to_old()[key]} to -> {current_value}")
                setattr(coffee_to_edit, get_new_to_old()[key], request.form.to_dict()[key])
            # else go to next value
            else:
                continue
        # print(f"new coffee_to_edit: {get_coffee_object_data(coffee_to_edit)}")
        db.session.commit()
        return redirect(url_for("edit_page", incoming_coffee=coffee_to_edit.name, coffee_id=coffee_to_edit.id))

    return render_template('coffee_info_page/edit_coffee_info.html', form=edit_cafe_form, coffee_to_edit=coffee_to_edit,
                           emotions=["super-happy", "happy", "neutral", "sad", "super-sad"])


def get_random_cafe():
    random_cafe = Cafe.query.all()
    return random.choice(random_cafe)


# print(get_coffee_object_data(get_random_cafe()))
# print((get_lat_lon_location(get_random_cafe())))
# print(get_latitude_longitude_from_google_address(get_lat_lon_location(get_random_cafe())))

if __name__ == "__main__":
    app.run(debug=True)
