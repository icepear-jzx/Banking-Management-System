from datetime import datetime
from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from .models import Loan, Cusforloan, Payinfo, Customer, Account, Saveacc, Checkacc, Cusforacc
from . import db


bp = Blueprint('loan', __name__, url_prefix='/loan')


@bp.route('/create', methods=['GET'])
def create_init():
    errors = []
    init_form = {'loanID': '', 'cusID': '', 'money': '', 'bank': '', 'state': ''}
    return render_template('loan/create.html', errors=errors, init_form=init_form)


@bp.route('/create', methods=['POST'])
def create():
    errors = []
    loanID = request.form['loanID']
    cusID = request.form['cusID']
    money = request.form['money']
    bank = request.form['bank']
    state = 'waiting'
    if len(loanID) != 4:
        errors.append('loanID')
    try:
        money = float(money)
    except:
        errors.append('money')
    if len(bank) == 0 or len(bank) > 20:
        errors.append('bank')
    if Loan.query.filter_by(loanID=loanID).first():
        errors.append('loanID')
    if not Customer.query.filter_by(cusID=cusID).first():
        errors.append('cusID')
    if not errors:
        new_loan = Loan(loanID=loanID, money=money, rest_money=money, bank=bank, state=state)
        db.session.add(new_loan)
        new_cusforloan = Cusforloan(loanID=loanID, cusID=cusID)
        db.session.add(new_cusforloan)
        db.session.commit()
        init_form = {'loanID': '', 'cusID': '', 'money': '', 'bank': '', 'state': ''}
        flash('Create new loan ' + loanID + ' successfully!')
        return render_template('loan/create.html', errors=errors, init_form=init_form)
    else:
        return render_template('loan/create.html', errors=errors, init_form=request.form)


@bp.route('/search', methods=['GET'])
def search_init():
    init_form = {'loanID': '', 'cusID': '', 'money': '', 'bank': '', 'state': ''}
    loans = Loan.query.all()
    for loan in loans:
        setattr(loan, 'cusID', loan.cusforloan[0].cusID)
    return render_template('loan/search.html', loans=loans, init_form=init_form)


@bp.route('/search', methods=['POST'])
def search():
    cusID = request.form['cusID']
    loanID = request.form['loanID']
    state = request.form['state']
    loans = Loan.query.filter_by()
    if 'and' in request.form:
        if cusID:
            loans = loans.filter(Loan.cusforloan.any(Cusforloan.cusID == cusID))
        if loanID:
            loans = loans.filter_by(loanID=loanID)
        if state:
            loans = loans.filter_by(state=state)
    else:
        if cusID or loanID or state:
            loans = loans.filter(Loan.cusforloan.any(Cusforloan.cusID == cusID) | 
                (Loan.loanID == loanID) | (Loan.state == state))
    loans = loans.all()
    for loan in loans:
        setattr(loan, 'cusID', loan.cusforloan[0].cusID)
    return render_template('loan/search.html', loans=loans, init_form=request.form)


@bp.route('/delete/<loanID>', methods=['GET'])
def delete(loanID):
    Cusforloan.query.filter_by(loanID=loanID).delete()
    Loan.query.filter_by(loanID=loanID).delete()
    db.session.commit()
    flash('Delete loan ' + loanID + ' successfully!')
    return redirect(url_for('loan.search'))


@bp.route('/update', methods=['POST'])
def update():
    errors = []
    loanID = request.form['loanID']
    cusID = request.form['cusID']
    money = request.form['money']
    if len(loanID) != 4:
        errors.append('loanID')
    try:
        money = float(money)
    except:
        errors.append('money')
    if money < 0:
        errors.append('money')
    loan = Loan.query.filter_by(loanID=loanID).first()
    if not loan:
        errors.append('loanID')
    elif loan.state == 'finished':
        errors.append('loanID')
    elif loan.rest_money < money:
        errors.append('loanID')
    if loan.rest_money - money != 0:
        state = 'going'
    else:
        state = 'finished'
    if not errors:
        Loan.query.filter_by(loanID=loanID).update(dict(state=state, rest_money=loan.rest_money-money))
        new_payinfo = Payinfo(loanID=loanID, cusID=cusID, money=money, paytime=datetime.now())
        db.session.add(new_payinfo)
        db.session.commit()
        flash('Update new loan ' + loanID + ' successfully!')
        return redirect(url_for('loan.search'))
    else:
        flash('Update new loan ' + loanID + ' unsuccessfully!')
        return redirect(url_for('loan.search'))
