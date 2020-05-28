from flask import Blueprint, jsonify, request, render_template
from .models import Customer
from . import db


bp = Blueprint('statistics', __name__, url_prefix='/statistics')


@bp.route('/money', methods=['GET'])
def money_init():
    return render_template('customer/create.html')


@bp.route('/money', methods=['POST'])
def money():
    cusID = request.form['cusID']
    cusname = request.form['cusname']
    cusphone = request.form['cusphone']
    address = request.form['address']
    # contact_phone = request.form['contact_phone']
    # contact_name = request.form['contact_name']
    # contact_email = request.form['contact_email']
    new_customer = Customer(cusID=cusID, cusname=cusname, cusphone=cusphone, address=address)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'status': 'success'})


@bp.route('/customers', methods=['GET'])
def customers():
    customers = Customer.query.all()
    return render_template('customer/search.html', customers=customers)


@bp.route('/customers', methods=['POST'])
def search():
    customers = Customer.query.filter_by()
    return render_template('customer/search.html')