from flask import Blueprint, jsonify, request, render_template
from .models import Customer
from . import db


bp = Blueprint('customer', __name__, url_prefix='/customer')


@bp.route('/add', methods=['POST'])
def add():
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


@bp.route('/getall', methods=['GET'])
def getall():
    customers = Customer.query.filter_by()
    return render_template('customer/index.html')
