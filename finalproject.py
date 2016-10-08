from flask import Flask, render_template, request, redirect, url_for,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#JSON End Points Start here
@app.route('/restaurant/JSON')
def showRestaurantsJSON():
	restaurants=session.query(Restaurant).all()
	return jsonify(Restaurants=[restaurant.serialize for restaurant in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):
	restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
	items=session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
	return jsonify(MenuItems=[item.serialize for item in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def showMenuDetailsJSON(restaurant_id,menu_id):
	restaurant= session.query(Restaurant).filter_by(id=restaurant_id).first()
	item = session.query(MenuItem).filter_by(restaurant_id=restaurant.id,id=menu_id).one()

	return jsonify(MenuItem=item.serialize)

#JSON End Points Start here


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
	restaurantToDelete=session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method=='POST':

		session.delete(restaurantToDelete)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
	    return render_template('deleterestaurant.html',restaurant=restaurantToDelete)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
	items=session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
	return render_template('menu.html',restaurant=restaurant,restaurant_id=restaurant_id,items=items)

@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):

    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
			editedItem.name = request.form['name']
			editedItem.description=request.form['description']
			editedItem.price=request.form['price']
			editedItem.course=request.form['course']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=itemToDelete)

if __name__=='__main__':
    app.debug=True
    app.run(host='0.0.0.0',port=5001)
