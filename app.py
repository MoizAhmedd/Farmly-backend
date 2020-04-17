from flask import Flask,Blueprint, flash, g, redirect, render_template, request, session, url_for, Response,send_file
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from helpers import schedule_delivery
import requests
import json

app = Flask(__name__)

CORS(app)

#Homepage
@app.route('/',methods=['GET'])
def index():
	return '<h1>Farmly Backend</h1>'

#Order Routes
@app.route('/add-order',methods=['POST'])
def add_order():
	#Adds order to DB after payment is processed
	try:
		order = request.get_json()
		order['deliveryStatus'] = 'scheduled'
		order_inserted = db.orders.insert(order)
		#add order to delivery
		delivery_scheduled = schedule_delivery(order)
		if delivery_scheduled:
			return Response(json.dumps({"message":"Delivery Scheduled","orderId":order_inserted['_id'],"deliveryDate":delivery_scheduled}),status=200,mimetype='application/json')
	except Exception as e:
		return Response(json.dumps({"message":"Couldn't add order","error":e}),status=404,mimetype='application/json')

@app.route('/cancel-order/<orderid>',methods=['PATCH'])
def cancel_order(orderid):
	#Cancels order, may need to issue refund
	pass 

#Truck Routes
@app.route('/add-truck',methods=['POST'])
def add_truck():
	#Adds a truck that will deal with deliveries
	try:
		truck = request.get_json()
		truck_inserted = db.trucks.insert(truck)
		if truck_inserted:
			return Response(json.dumps({"message":"Truck Added"}),status=200,mimetype='application/json')
		return Response(json.dumps({"message":"Couldn't add truck, try again"}),status=400,mimetype='application/json')
	except Exception as e:
		return Response(json.dumps({"message":"Couldn't add order","error":e}),status=404,mimetype='application/json')

