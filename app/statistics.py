from datetime import date, datetime
from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from sqlalchemy import func
from .models import Customer, Loan, Account, Bank, Cusforacc, Cusforloan
from . import db


bp = Blueprint('statistics', __name__, url_prefix='/statistics')


@bp.route('/year', methods=['GET'])
def year():
    title = "年度数据"
    money_stat = []
    cus_stat = []

    start_year = db.session.query(func.min(Customer.settime)).scalar().year
    end_year = datetime.now().year

    banks = [bank.bankname for bank in Bank.query.all()]
    colors = ["rgb(255, 99, 132)", "rgb(54, 162, 235)", "rgb(255, 205, 86)"]

    for y in range(start_year, end_year + 1):
        money_stat.append({
            'period': y, 
            'acc': {bank: db.session.query(func.sum(Account.money)).filter(
                    Account.cusforacc.has(Cusforacc.bank == bank)
                ).filter(
                    Account.settime.between(date(y, 1, 1), date(y, 12, 31))
                ).scalar() for bank in banks}, 
            'loan': {bank: db.session.query(func.sum(Loan.money)).filter(
                    Loan.bank == bank
                ).filter(
                    Loan.settime.between(date(y, 1, 1), date(y, 12, 31))
                ).scalar() for bank in banks}, 
        })
        cus_stat.append({
            'period': y,
            'number': {bank: db.session.query(func.count(Customer.cusID)).filter(
                    Customer.bank == bank
                ).filter(
                    Customer.settime.between(date(y, 1, 1), date(y, 12, 31))
                ).scalar() for bank in banks}, 
        })

    return render_template('statistics/index.html', title=title, span="年份", banks=banks, colors=colors,
        money_stat=money_stat, cus_stat=cus_stat)


@bp.route('/quarter', methods=['GET'])
def quarter():
    money_stat = [{'year': '2019', 'check': 1234, 'loan': 4321}, {'year': '2020', 'check': 5432, 'loan': 5678}]
    return render_template('statistics/index.html', money_stat=money_stat)


@bp.route('/month', methods=['GET'])
def month():
    money_stat = [{'year': '2019', 'check': 1234, 'loan': 4321}, {'year': '2020', 'check': 5432, 'loan': 5678}]
    return render_template('statistics/index.html', money_stat=money_stat)
