#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'


# This route returns a list of JSON objects for all bakeries in the DB
@app.route('/bakeries')
def bakeries():
    # bakeries = []
    # for bakery in Bakery.query.all():
    #     bakery_dict = bakery.to_dict()
    #     bakeries.append(bakery_dict)

    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]

    response = make_response(
        bakeries,
        200
    )

    return response


# This route returns a single bakery as JSON w/ its baked goods nested in a list. 
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_dict = bakery.to_dict()
    response = make_response(
        bakery_dict,
        200
    )
    return response

# This route returns a list of baked goods as JSON, sorted by price in desc. order
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [baked_good.to_dict() for baked_good in baked_goods]
    response = make_response(
        baked_goods_list,
        200
    )
    return response


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    priciest_baked_goods = baked_goods.to_dict()
    response = make_response(
        priciest_baked_goods,
        200
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
