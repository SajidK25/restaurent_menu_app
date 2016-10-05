from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurant')
def showRestaurants():
	restaurants=session.query(Restaurant).all()
	return render_template('restaurants.html',restaurants=restaurants)

@app.route('/restaurant/new',methods=['GET','POST'])
def newRestaurant():
	if request.method=='POST':
		newRestaurant=Restaurant(name=request.form['name'])
		session.add(newRestaurant)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newrestaurant.html')



@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
	editRestaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method=='POST':
		if request.form['name']:
			editRestaurant.name=request.form['name']
		session.add(editRestaurant)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('editrestaurant.html',restaurant_id=restaurant_id,editRestaurant=editRestaurant)

@app.route('/restaurant/<int:restaurant_id>/delete',methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
	if request.method=='POST':
		restaurantToDelete=session.query(Restaurant).filter_by(id=restaurant_id).one()
		session.delete(restaurantToDelete)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
	    return render_template('deleterestaurant.html',restaurant=restaurantToDelete)

# @app.route('/restaurant/restaurant_id')
# @app.route('/restaurant/restaurant_id/menu')
# def showMenu(restaurant_id):
# 	return render_template('menu.html',restaurant_id=restaurant_id,items=items)
#
# @app.route('/restaurant/restaurant_id/menu/new')
# def newMenuItem(restaurant_id):
# 	return render_template('menu.html',restaurant_id=restaurant_id)
#
# @app.route('/restaurant/restaurant_id/menu/menu_id/ edit')
# def editMenuItem(restaurant_id,menu_id):
# 	return render_template('newmenuitem.html',restaurant_id=restaurant_id,menu_id,items=items)
#
# @app.route('/restaurant/restaurant_id/menu/menu_id/delete')
# def deleteMenuItem(restaurant_id,menu_id):
# 	return render_template('newmenuitem.html',restaurant_id=restaurant_id,menu_id,items=items)

if __name__=='__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=5001)
