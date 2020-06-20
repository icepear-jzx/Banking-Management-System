from sqlalchemy import Column, String, Integer, Float, Date, DateTime, CHAR, Enum, ForeignKey
from sqlalchemy.orm import relationship, backref
from . import db


class Cusforloan(db.Model):
    loanID = Column(CHAR(4), ForeignKey('loan.loanID', ondelete='CASCADE'), primary_key=True)
    cusID = Column(CHAR(18), ForeignKey('customer.cusID'), primary_key=True)


class Payinfo(db.Model):
    loanID = Column(CHAR(4), ForeignKey('loan.loanID', ondelete='CASCADE'), primary_key=True)
    cusID = Column(CHAR(18), ForeignKey('customer.cusID'), primary_key=True)
    money = Column(Float, primary_key=True)
    paytime = Column(DateTime, primary_key=True)


class Loan(db.Model):
    loanID = Column(CHAR(4), primary_key=True)
    settime = Column(DateTime)
    money = Column(Float, nullable=False)
    rest_money = Column(Float, nullable=False)
    bank = Column(String(20), ForeignKey('bank.bankname'), nullable=False)
    state = Column(Enum('waiting', 'going', 'finished'), nullable=False)
    cusforloan = relationship(Cusforloan, foreign_keys=[Cusforloan.loanID, Cusforloan.cusID])
    payinfo = relationship(Payinfo, foreign_keys=[Payinfo.loanID, Payinfo.cusID, Payinfo.money, Payinfo.paytime])


class Cusforacc(db.Model):
    accountID = Column(CHAR(6), ForeignKey('account.accountID'), primary_key=True)
    cusID = Column(CHAR(18), ForeignKey('customer.cusID'), primary_key=True)
    bank = Column(String(20), ForeignKey('bank.bankname'))
    visit = Column(DateTime)


class Customer(db.Model):
    cusID = Column(CHAR(18), primary_key=True)
    settime = Column(DateTime)
    bank = Column(String(20), ForeignKey('bank.bankname'), nullable=False)
    cusname = Column(String(10), nullable=False)
    cusphone = Column(CHAR(11), nullable=False)
    address = Column(String(50))
    contact_phone = Column(CHAR(11), nullable=False)
    contact_name = Column(String(10), nullable=False)
    contact_email = Column(String(20))
    relation = Column(String(10), nullable=False)
    loanres = Column(CHAR(18), ForeignKey('employee.empID'))
    accres = Column(CHAR(18), ForeignKey('employee.empID'))
    cusforacc = relationship(Cusforacc, foreign_keys=[Cusforacc.accountID, Cusforacc.cusID])
    cusforloan = relationship(Cusforloan, foreign_keys=[Cusforloan.loanID, Cusforloan.cusID])
    payinfo = relationship(Payinfo, foreign_keys=[Payinfo.loanID, Payinfo.cusID, Payinfo.money, Payinfo.paytime])


class Employee(db.Model):
    empID = Column(CHAR(18), primary_key=True)
    empname = Column(String(20), nullable=False)
    empphone = Column(CHAR(11))
    empaddr = Column(String(50))
    emptype = Column(Enum('staff', 'manager'))
    empstart = Column(Date, nullable=False)
    depart = Column(CHAR(4), ForeignKey('department.departID'))
    loanres = relationship(Customer, foreign_keys=[Customer.loanres])
    accres = relationship(Customer, foreign_keys=[Customer.accres])


class Department(db.Model):
    departID = Column(CHAR(4), primary_key=True)
    departname = Column(String(20), nullable=False)
    departtype = Column(String(15))
    manager = Column(CHAR(18), nullable=False)
    bank = Column(String(20), ForeignKey('bank.bankname'), nullable=False)
    employees = relationship(Employee, foreign_keys=[Employee.depart])


class Bank(db.Model):
    bankname = Column(String(20), primary_key=True)
    city = Column(String(20), nullable=False)
    money = Column(Float, nullable=False)
    departments = relationship(Department, foreign_keys=[Department.bank])
    cusforacc = relationship(Cusforacc, foreign_keys=[Cusforacc.bank])
    loans = relationship(Loan, foreign_keys=[Loan.bank])
    customers = relationship(Customer, foreign_keys=[Customer.bank])


class Saveacc(db.Model):
    accountID = Column(CHAR(6), ForeignKey('account.accountID', 
        ondelete='CASCADE'), primary_key=True)
    interestrate = Column(Float)
    savetype = Column(Enum('RMB', 'USD', 'EUR', 'JPY', 'GBP'))


class Checkacc(db.Model):
    accountID = Column(CHAR(6), ForeignKey('account.accountID', 
        ondelete='CASCADE'), primary_key=True)
    overdraft = Column(Float)


class Account(db.Model):
    accountID = Column(CHAR(6), primary_key=True)
    money = Column(Float, nullable=False)
    settime = Column(DateTime)
    accounttype = Column(Enum('saveacc', 'checkacc'))
    saveacc = relationship(Saveacc, foreign_keys=[Saveacc.accountID], 
        uselist=False, passive_deletes=True)
    checkacc = relationship(Checkacc, foreign_keys=[Checkacc.accountID], 
        uselist=False, passive_deletes=True)
    cusforacc = relationship(Cusforacc, foreign_keys=[Cusforacc.accountID, Cusforacc.cusID], 
        uselist=False, passive_deletes=True)
