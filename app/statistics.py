from datetime import date, datetime
import calendar
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

    # start_year = db.session.query(func.min(Customer.settime)).scalar().year
    end_year = db.session.query(func.max(Customer.settime)).scalar().year

    banks = [bank.bankname for bank in Bank.query.all()]
    colors = ["rgb(255, 99, 132)", "rgb(54, 162, 235)", "rgb(255, 205, 86)"]

    for y in range(end_year - 5, end_year + 1):
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
    
    for stat in money_stat:
        for bank in banks:
            if stat['acc'][bank] == None:
                stat['acc'][bank] = 0
            if stat['loan'][bank] == None:
                stat['loan'][bank] = 0

    return render_template('statistics/index.html', title=title, span="年份", banks=banks, colors=colors,
        money_stat=money_stat, cus_stat=cus_stat)


@bp.route('/quarter', methods=['GET'])
def quarter():
    title = "季度数据"
    money_stat = []
    cus_stat = []

    end_date = db.session.query(func.max(Customer.settime)).scalar()
    end_year = end_date.year
    end_quarter = (end_date.month - 1) // 3 + 1
    quarters = [str(end_year + (end_quarter - i - 1) // 4) + 
        'Q' + str((end_quarter + 7 - i) % 4 + 1) for i in range(5, -1, -1)]

    banks = [bank.bankname for bank in Bank.query.all()]
    colors = ["rgb(255, 99, 132)", "rgb(54, 162, 235)", "rgb(255, 205, 86)"]

    for q in quarters:
        y = int(q[:4])
        m_start = (int(q[-1]) - 1) * 3 + 1
        m_end = (int(q[-1]) - 1) * 3 + 3
        print(y, m_start, m_end)
        money_stat.append({
            'period': q, 
            'acc': {bank: db.session.query(func.sum(Account.money)).filter(
                    Account.cusforacc.has(Cusforacc.bank == bank)
                ).filter(
                    Account.settime.between(date(y, m_start, 1), date(y, m_end, calendar.monthrange(y, m_end)[1]))
                ).scalar() for bank in banks}, 
            'loan': {bank: db.session.query(func.sum(Loan.money)).filter(
                    Loan.bank == bank
                ).filter(
                    Loan.settime.between(date(y, m_start, 1), date(y, m_end, calendar.monthrange(y, m_end)[1]))
                ).scalar() for bank in banks}, 
        })
        cus_stat.append({
            'period': q,
            'number': {bank: db.session.query(func.count(Customer.cusID)).filter(
                    Customer.bank == bank
                ).filter(
                    Customer.settime.between(date(y, m_start, 1), date(y, m_end, calendar.monthrange(y, m_end)[1]))
                ).scalar() for bank in banks}, 
        })
    
    for stat in money_stat:
        for bank in banks:
            if stat['acc'][bank] == None:
                stat['acc'][bank] = 0
            if stat['loan'][bank] == None:
                stat['loan'][bank] = 0

    return render_template('statistics/index.html', title=title, span="季度", banks=banks, colors=colors,
        money_stat=money_stat, cus_stat=cus_stat)


@bp.route('/month', methods=['GET'])
def month():
    title = "月度数据"
    money_stat = []
    cus_stat = []

    end_date = db.session.query(func.max(Customer.settime)).scalar()
    end_year = end_date.year
    end_month = end_date.month
    months = [str(end_year + (end_month - i - 1) // 12) + 
        'M' + str((end_month + 11 - i) % 12 + 1) for i in range(5, -1, -1)]

    banks = [bank.bankname for bank in Bank.query.all()]
    colors = ["rgb(255, 99, 132)", "rgb(54, 162, 235)", "rgb(255, 205, 86)"]

    for month in months:
        y = int(month[:4])
        m = int(month.split('M')[-1])
        print(y, m)
        money_stat.append({
            'period': month, 
            'acc': {bank: db.session.query(func.sum(Account.money)).filter(
                    Account.cusforacc.has(Cusforacc.bank == bank)
                ).filter(
                    Account.settime.between(date(y, m, 1), date(y, m, calendar.monthrange(y, m)[1]))
                ).scalar() for bank in banks}, 
            'loan': {bank: db.session.query(func.sum(Loan.money)).filter(
                    Loan.bank == bank
                ).filter(
                    Loan.settime.between(date(y, m, 1), date(y, m, calendar.monthrange(y, m)[1]))
                ).scalar() for bank in banks}, 
        })
        cus_stat.append({
            'period': month,
            'number': {bank: db.session.query(func.count(Customer.cusID)).filter(
                    Customer.bank == bank
                ).filter(
                    Customer.settime.between(date(y, m, 1), date(y, m, calendar.monthrange(y, m)[1]))
                ).scalar() for bank in banks}, 
        })
    
    for stat in money_stat:
        for bank in banks:
            if stat['acc'][bank] == None:
                stat['acc'][bank] = 0
            if stat['loan'][bank] == None:
                stat['loan'][bank] = 0

    return render_template('statistics/index.html', title=title, span="月份", banks=banks, colors=colors,
        money_stat=money_stat, cus_stat=cus_stat)
