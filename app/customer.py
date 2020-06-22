from datetime import datetime
from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from .models import Customer
from . import db


bp = Blueprint('customer', __name__, url_prefix='/customer')


@bp.route('/create', methods=['GET'])
def create_init():
    errors = []
    init_form = {'cusID': '', 'cusname': '', 'bank': '', 'cusphone': '', 'address': '',
        'contact_phone': '', 'contact_name': '', 'contact_email': '', 'relation': ''}
    return render_template('customer/create.html', errors=errors, init_form=init_form)


@bp.route('/create', methods=['POST'])
def create():
    errors = []
    cusID = request.form['cusID']
    bank = request.form['bank']
    cusname = request.form['cusname']
    cusphone = request.form['cusphone']
    address = request.form['address']
    contact_phone = request.form['contact_phone']
    contact_name = request.form['contact_name']
    contact_email = request.form['contact_email']
    relation = request.form['relation']
    if len(cusID) != 18:
        errors.append('cusID')
    if len(bank) == 0 or len(bank) > 20:
        errors.append('bank')
    if len(cusname) == 0 or len(cusname) > 10:
        errors.append('cusname')
    if len(cusphone) != 11:
        errors.append('cusphone')
    if len(address) > 50:
        errors.append('address')
    if len(contact_phone) != 11:
        errors.append('contact_phone')
    if len(contact_name) == 0 or len(contact_name) > 10:
        errors.append('contact_name')
    if len(contact_email) > 0 and '@' not in contact_email:
        errors.append('contact_email')
    if len(relation) == 0 or len(relation) > 10:
        errors.append('relation')
    if Customer.query.filter_by(cusID=cusID).first():
        errors.append('cusID')
    if not errors:
        new_customer = Customer(cusID=cusID, settime=datetime.now(), bank=bank, cusname=cusname, cusphone=cusphone, 
            address=address, contact_name=contact_name, contact_phone=contact_phone, 
            contact_email=contact_email, relation=relation)
        db.session.add(new_customer)
        db.session.commit()
        init_form = {'cusID': '', 'cusname': '', 'bank': '', 'cusphone': '', 'address': '',
            'contact_phone': '', 'contact_name': '', 'contact_email': '', 'relation': ''}
        flash('Create new customer ' + cusID + ' successfully!')
        return render_template('customer/create.html', errors=errors, init_form=init_form)
    else:
        return render_template('customer/create.html', errors=errors, init_form=request.form)


@bp.route('/search', methods=['GET'])
def search_init():
    init_form = {'cusID': '', 'cusname': '', 'cusphone': ''}
    customers = Customer.query.all()
    return render_template('customer/search.html', customers=customers, init_form=init_form)


@bp.route('/search', methods=['POST'])
def search():
    cusID = request.form['cusID']
    cusname = request.form['cusname']
    cusphone = request.form['cusphone']
    customers = Customer.query.filter_by()
    if 'and' in request.form:
        if cusID:
            customers = customers.filter_by(cusID=cusID)
        if cusname:
            customers = customers.filter_by(cusname=cusname)
        if cusphone:
            customers = customers.filter_by(cusphone=cusphone)
    else:
        if cusID or cusname or cusphone:
            customers = customers.filter((Customer.cusID == cusID) | (Customer.cusname == cusname) | 
                (Customer.cusphone == cusphone))
    return render_template('customer/search.html', customers=customers.all(), init_form=request.form)


@bp.route('/delete/<cusID>', methods=['GET'])
def delete(cusID):
    cus = Customer.query.filter_by(cusID=cusID)
    if cus.first().cusforacc or cus.first().cusforloan:
        flash('Delete customer ' + cusID + ' unsuccessfully!')
        return redirect(url_for('customer.search'))
    cus.delete()
    db.session.commit()
    flash('Delete customer ' + cusID + ' successfully!')
    return redirect(url_for('customer.search'))


@bp.route('/update', methods=['POST'])
def update():
    errors = []
    cusID = request.form['cusID']
    bank = request.form['bank']
    cusname = request.form['cusname']
    cusphone = request.form['cusphone']
    address = request.form['address']
    contact_phone = request.form['contact_phone']
    contact_name = request.form['contact_name']
    contact_email = request.form['contact_email']
    relation = request.form['relation']
    if len(cusID) != 18:
        errors.append('cusID')
    if len(bank) == 0 or len(bank) > 20:
        errors.append('bank')
    if len(cusname) == 0 or len(cusname) > 10:
        errors.append('cusname')
    if len(cusphone) != 11:
        errors.append('cusphone')
    if len(address) > 50:
        errors.append('address')
    if len(contact_phone) != 11:
        errors.append('contact_phone')
    if len(contact_name) == 0 or len(contact_name) > 10:
        errors.append('contact_name')
    if len(contact_email) > 0 and '@' not in contact_email:
        errors.append('contact_email')
    if len(relation) == 0 or len(relation) > 10:
        errors.append('relation')
    if not errors:
        Customer.query.filter_by(cusID=cusID).update(dict(cusID=cusID, bank=bank, cusname=cusname, cusphone=cusphone, 
            address=address, contact_name=contact_name, contact_phone=contact_phone, 
            contact_email=contact_email, relation=relation))
        db.session.commit()
        init_form = {'cusID': '', 'cusname': '', 'bank': '', 'cusphone': '', 'address': '',
            'contact_phone': '', 'contact_name': '', 'contact_email': '', 'relation': ''}
        flash('Update customer ' + cusID + ' successfully!')
        return redirect(url_for('customer.search'))
    else:
        flash('Update customer ' + cusID + ' unsuccessfully!')
        return redirect(url_for('customer.search'))
