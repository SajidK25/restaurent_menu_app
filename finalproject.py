from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app.route('/')
app.route('/restaurant')
def showRestaurants():
	retrun "This page will show all my restaurants"

app.route('/restaurant/new')
def newRestaurant():
	retrun "This page will be for making a new restaurant"



app.route('/restaurant/restaurant_id/edit')
def editRestaurant():
	retrun "This page will be for editing restaurant %s” % restaurant_id"

app.route('/restaurant/restaurant_id/delete')
def deleteRestaurant():
	retrun "This page will be for deleting restaurant %s” % restaurant_id"

app.route('/restaurant/restaurant_id')
app.route('/restaurant/restaurant_id/menu')
def showMenu():
	retrun "This page is the menu for restaurant %s” restaurant_id"

app.route('/restaurant/restaurant_id/menu/new)
def newMenuItem():
	retrun "This page is for making a new menu item for restaurant %s” %r estaurant_id"

app.route('/restaurant/restaurant_id/menu/menu_id/ edit')
def editMenuItem():
	retrun "This page is for editing menu item %s “ menu_id"

app.route('/restaurant/restaurant_id/menu/menu_id/ delete)
def deleteMenuItem():
	retrun "This page is for deleting menu item %s” menu_id"




if __name__=='__main__':
	app.debug=True
	app.run(host=0.0.0.0,port=5000)
