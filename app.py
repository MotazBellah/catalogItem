from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from database_setup import Catalog, Base, Item

engine = create_engine('sqlite:///catalogitem.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
@app.route('/catalogs')
def showCatalog():
    '''This page will sho all my catalogs'''
    catalogs = session.query(Catalog).all()
    return render_template('catalogs.html', catalogs = sorted(catalogs))


@app.route('/catalog/<catalog_name>')
@app.route('/catalog/<catalog_name>/items')
def showItem(catalog_name):
    '''show catalog's items %s''' % catalog_name
    catalog_id = session.query(Catalog).filter_by(name = catalog_name).first().id
    catalog = session.query(Catalog).filter_by(name = catalog_name).one()
    items = session.query(Item).filter_by(catalog_id = catalog.id).all()
    return render_template('items.html', items = items, catalog = catalog, catalog_name=catalog_name)

@app.route('/catalog/<catalog_name>/<item_name>')
def showItemInfo(catalog_name, item_name):
    '''edit catalog's items %s''' % item_name
    items = session.query(Item).filter_by(name = item_name).first()
    catalog = session.query(Catalog).filter_by(id = items.catalog_id).first()
    return render_template('itemInfo.html', items = items)

@app.route('/catalog/<catalog_name>/items/new', methods = ['GET', 'POST'])
def newItem(catalog_name):
    '''create new catalog's items %s''' % catalog_name
    catalog_id = session.query(Catalog).filter_by(name = catalog_name).first().id
    if request.method == 'POST':
        newItem = Item(name = request.form['name'], catalog_id = catalog_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showItem', catalog_name=catalog_name))
    else:
        return render_template('newItem.html', catalog_name=catalog_name)

@app.route('/catalog/<catalog_name>/<item_name>/edit', methods = ['GET', 'POST'])
def editItem(catalog_name, item_name):
    '''edit catalog's items %s''' % item_name
    editedItem = session.query(Item).filter_by(name = item_name).first()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showItem', catalog_name=catalog_name))
    else:
        return render_template('editItem.html', item_name = item_name, catalog_name=catalog_name, item = editedItem)

@app.route('/catalog/<catalog_name>/<item_name>/delete', methods = ['GET', 'POST'])
def deleteItem(catalog_name, item_name):
    '''delete catalog's items %s''' % item_name
    item = session.query(Item).filter_by(name = item_name).first()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('showItem', catalog_name=catalog_name))
    else:
        return render_template('deleteItem.html', item_name = item_name, catalog_name=catalog_name, item = item)

# @app.route('/catalog/<int:catalog_id>/items/<int:item_id>/delete', methods = ['GET', 'POST'])
# def deleteItem(catalog_id, item_id):
#     '''delete catalog's items %s''' % item_id
#     item = session.query(Item).filter_by(id = item_id).first()
#     if request.method == 'POST':
#         session.delete(item)
#         session.commit()
#         return redirect(url_for('showItem', catalog_id=catalog_id))
#     else:
#         return render_template('deleteItem.html', item_id = item_id, catalog_id=catalog_id, item = item)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
