from flask import Blueprint, jsonify, request, render_template
from .models import Customer
from . import db


bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route('/create', methods=['GET'])
def create_init():
    return render_template('customer/create.html')


@bp.route('/create', methods=['POST'])
def create():
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


@bp.route('/search', methods=['GET'])
def search_init():
    customers = Customer.query.all()
    return render_template('customer/search.html', customers=customers)


@bp.route('/search', methods=['POST'])
def search():
    customers = Customer.query.filter_by()
    return render_template('customer/search.html')