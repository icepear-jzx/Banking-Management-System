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
    state = request.form['state']
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
        new_loan = Loan(loanID=loanID, money=money, bank=bank, state=state)
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
    init_form = {'accountID': '', 'accounttype': '', 'cusID': ''}
    accounts = Account.query.all()
    for acc in accounts:
        setattr(acc, 'bank', acc.cusforacc.bank)
        setattr(acc, 'cusID', acc.cusforacc.cusID)
        if acc.accounttype == 'saveacc':
            setattr(acc, 'interestrate', acc.saveacc.interestrate)
            setattr(acc, 'savetype', acc.saveacc.savetype)
        else:
            setattr(acc, 'overdraft', acc.checkacc.overdraft)
    return render_template('account/search.html', accounts=accounts, init_form=init_form)


@bp.route('/search', methods=['POST'])
def search():
    cusID = request.form['cusID']
    accountID = request.form['accountID']
    accounttype = request.form['accounttype']
    accounts = Account.query.filter_by()
    if 'and' in request.form:
        if cusID:
            accounts = accounts.filter(Account.cusforacc.has(Cusforacc.cusID == cusID))
        if accountID:
            accounts = accounts.filter_by(accountID=accountID)
        if accounttype:
            accounts = accounts.filter_by(accounttype=accounttype)
    else:
        if cusID or accountID or accounttype:
            accounts = accounts.filter(Account.cusforacc.has(Cusforacc.cusID == cusID) | 
                (Account.accountID == accountID) | (Account.accounttype == accounttype))
    accounts = accounts.all()
    for acc in accounts:
        setattr(acc, 'bank', acc.cusforacc.bank)
        setattr(acc, 'cusID', acc.cusforacc.cusID)
        if acc.accounttype == 'saveacc':
            setattr(acc, 'interestrate', acc.saveacc.interestrate)
            setattr(acc, 'savetype', acc.saveacc.savetype)
        else:
            setattr(acc, 'overdraft', acc.checkacc.overdraft)
    return render_template('account/search.html', accounts=accounts, init_form=request.form)


@bp.route('/delete/<accountID>', methods=['GET'])
def delete(accountID):
    Saveacc.query.filter_by(accountID=accountID).delete()
    Checkacc.query.filter_by(accountID=accountID).delete()
    Cusforacc.query.filter_by(accountID=accountID).delete()
    Account.query.filter_by(accountID=accountID).delete()
    db.session.commit()
    flash('Delete account ' + accountID + ' successfully!')
    return redirect(url_for('account.search'))


@bp.route('/update', methods=['POST'])
def update():
    errors = []
    accountID = request.form['accountID']
    cusID = request.form['cusID']
    money = request.form['money']
    bank = request.form['bank']
    accounttype = request.form['accounttype']
    if accounttype == 'saveacc':
        savetype = request.form['savetype']
        interestrate = request.form['interestrate']
    else:
        overdraft = request.form['overdraft']
    if len(accountID) != 6:
        errors.append('accountID')
    try:
        money = float(money)
    except:
        errors.append('money')
    if len(bank) == 0 or len(bank) > 20:
        errors.append('bank')
    if accounttype == 'saveacc':
        try:
            interestrate = float(interestrate)
        except:
            errors.append('interestrate')
    else:
        try:
            overdraft = float(overdraft)
        except:
            errors.append('overdraft')
    if not Customer.query.filter_by(cusID=cusID).first():
        errors.append('cusID')
    if not errors:
        Account.query.filter_by(accountID=accountID).update(
            dict(accountID=accountID, money=money, settime=datetime.now(), accounttype=accounttype))
        if accounttype == 'saveacc':
            Saveacc.query.filter_by(accountID=accountID).update(
                dict(accountID=accountID, interestrate=interestrate, savetype=savetype))
        else:
            Checkacc.query.filter_by(accountID=accountID).update(
                dict(accountID=accountID, overdraft=overdraft))
        Cusforacc.query.filter_by(accountID=accountID).update(
            dict(accountID=accountID, cusID=cusID, bank=bank, visit=datetime.now()))
        db.session.commit()
        flash('Update new account ' + accountID + ' successfully!')
        return redirect(url_for('account.search'))
    else:
        flash('Update new account ' + accountID + ' unsuccessfully!')
        return redirect(url_for('account.search'))
